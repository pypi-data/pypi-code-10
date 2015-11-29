# Released under GPL3 terms (see LICENSE file)

from . import i3barproto
from . import validation
from . import constants
from . import config
import subprocess #from subprocess import (Popen, PIPE, TimeoutExpired)
import shlex
import json
import logging
import select
import fcntl
import os
import logging
import time


class Readpool():
    """Read from multiple file descriptors at once"""

    def __init__(self):
        self._fds = {}  # Map fd -> callback
        self._log = logging.getLogger('IO')

    def add(self, fd, callback):
        """
        Add `fd` to file descriptors to read from

        Lines that appear on `fd` are forwarded as a list to `callback`.
        """
        flags = fcntl.fcntl(fd, fcntl.F_GETFL, 0)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        self._fds[fd] = callback
        # self._log.debug('Registered FD#%s for %s', fd.name, repr(callback))

    def remove(self, fd):
        """Stop reading from `fd`"""
        if fd in self._fds:
            # self._log.debug('Unregistering FD#%s of %s', fd.name, repr(self._fds[fd]))
            del(self._fds[fd])

    def read(self, fd='all', timeout=-1, delay=0):
        """
        Wait for input to appear and call callbacks accordingly

        If `fd` is 'all' or not specified, process all registered file
        descriptors.

        If `timeout` is >= 0, stop waiting for input after that many
        seconds. Otherwise, block indefinitely until there is something to
        read.

        IF `delay` is > 0, if there is something to read, wait `delay` seconds
        and then check all file descriptors again.
        """
        if fd == 'all':
            fds = list(self._fds)
        else:
            fds = [fd]

        if not fds:
            if timeout > 0:
                time.sleep(timeout)
            return

        # self._log.debug('Waiting to read from: %s', ', '.join('FD#'+str(fd.name) for fd in fds))
        if timeout >= 0:
            rlist, _, _ = select.select(fds, [], [], timeout)
        else:
            rlist, _, _ = select.select(fds, [], [])

        if delay > 0:
            # Once there's output available, wait a few msecs before taking
            # action to bundle multiple outputs into one update.
            time.sleep(delay)
            self.read(delay=0, timeout=0)
        else:
            for fd in rlist:
                callback = self._fds[fd]
                lines = [line.rstrip('\n') for line in fd.readlines()]
                if len(lines) < 1:
                    # fd is readable but returns not even an empty line ("\n")
                    # means has been process terminated
                    fd.close()
                    self.remove(fd=fd)
                    # self._log.debug('Reporting dead FD#%s to %s', fd.name, repr(callback))
                    callback([])  # Report dead fd
                else:
                    # self._log.debug('Sending %d line(s) from FD#%s to %s',
                    #                 len(lines), fd.name, repr(callback))
                    callback(lines)


# TODO: Add 'run_in' and 'run_at' fields to allow running a newly set command
# in the future.
class Worker():
    DEFAULTS = {
        'command': '',
        'shell': False,
        'trigger_updates': True,
    }

    VALIDATORS_CFG = {
        'command': lambda v: str(v),
        'shell': validation.validate_bool,
        'trigger_updates': validation.validate_bool,
    }

    LAST_BLOCK_RESET_KEYS = ('separator', 'separator_block_width')

    def __init__(self, readpool, **initial_vars):
        self._readpool = readpool
        self._name = initial_vars.get('name', 'UNNAMED')
        self._proc = None
        self._log = logging.getLogger(self.name)

        self._stdout_cache = json.dumps({'name': self.name, 'full_text': ''})
        self._stdout_pending = False

        self._stdout_timestamps = []
        self._stderr_timestamps = []

        self._cfg = validation.VDict(validators=self.VALIDATORS_CFG,
                                     valid_keys=tuple(self.DEFAULTS),
                                     **self.DEFAULTS)
        self._env = {}

        self._default_block = i3barproto.I3Block()
        self._blocks = {}
        self._blockids = []  # List of _blocks keys to maintain order

        self._rerun_command = False
        self._initialized = False
        self._update(**initial_vars)
        self._initialized = True

    def run(self):
        self._rerun_command = False
        if self.is_static:
            self._proc = None
        else:
            if self.is_running:
                self.terminate()

            if self._cfg['shell']:
                cmd_str = cmd = self._cfg['command']
            else:
                cmd_str = self._cfg['command']
                cmd = shlex.split(os.path.expanduser(self._cfg['command']))
            self._log.info('Executing%s: %s',
                           ' shell command' if self._cfg['shell'] else '', cmd_str)

            env = os.environ.copy()
            env.update(self._env)
            try:
                self._proc = subprocess.Popen(
                    cmd, env=env,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    bufsize=1,  # Line buffering
                    universal_newlines=True, shell=self._cfg['shell']
                )
            except OSError as e:
                self._croak(long='Can\'t execute {}: {}'.format(cmd_str, e.strerror),
                            short='Failed to run {}'.format(cmd_str.split()[0]))
            else:
                # self._log.debug('stdout=FD#%s stderr=FD#%s',
                #                 self._proc.stdout.name, self._proc.stderr.name)
                self._readpool.add(self._proc.stdout, self._handle_stdout)
                self._readpool.add(self._proc.stderr, self._handle_stderr)

    def _handle_stdout(self, lines):
        for line in lines:
            self._parse_command_stdout(line)
        self._check_output(lines, self._stdout_timestamps, lps_limit=15)

    def _handle_stderr(self, lines):
        for line in lines:
            self._log.info(line)
        self._check_output(lines, self._stderr_timestamps, lps_limit=100)

    def _check_output(self, lines, timestamps, lps_limit):
        # No lines means fd closed - process terminated
        if len(lines) < 1 :
            self._check_command_result()

        # Detect if there are too many lines per second on stdout or stderr.
        now = time.time()
        for line in lines:
            timestamps.append(now)
        if len(timestamps) >= 10:
            while len(timestamps) > 10:
                timestamps.pop(0)
            timerange = now - timestamps[0]
            if timerange > 0:
                lps = int(len(timestamps) / timerange)
                if lps >= lps_limit+1:
                    self._croak(long='Logorrhea detected! ({} lines per second)'.format(int(lps)),
                                short=('Terminated for exceeding '
                                       '{} lines per second limit: {}').format(lps_limit, lps))

    def _check_errors(self):
        # Check if any blocks have accumulated any errors
        errors = self._default_block.errors + \
                 [error for blockid in self._blockids
                  for error in self._blocks[blockid].errors]
        if errors:
            self._croak(long=errors, short=errors[-1])
            return True
        else:
            return False

    def _parse_command_stdout(self, line):
        try:
            line = json.loads(line)
        except ValueError:
            self._update(full_text=line)
        else:
            if isinstance(line, dict):
                self._update(**line)
            elif isinstance(line, list):
                self._update_blocks_only(*line)
            else:
                self._update(full_text=str(line))

    def _generate_json(self, **block):
        if block:
            for key in ('name', 'instance', 'separator', 'separator_block_width'):
                if key not in block and key in self._default_block:
                    block[key] = self._default_block[key]
            self._stdout_cache = i3barproto.I3Block(**block).json

        elif len(self._blockids) < 1:
            self._stdout_cache = self._default_block.json
        else:
            self._stdout_cache = ','.join(self._blocks[blockid].json
                                          for blockid in self._blockids)
        if self.triggers_updates:
            self._stdout_pending = True

        # self._log.debug('Generated json: %s', self._stdout_cache)

    def _error_on_i3bar(self, msg):
        self._generate_json(full_text='[{}: {}]'.format(self.name, msg),
                            color=constants.ERROR_COLOR)

    def _croak(self, long=None, short=None):
        if long is not None:
            if isinstance(long, (list, tuple, set)):
                for line in long:
                    self._log.error(line)
            else:
                self._log.error(long)
        if short is not None:
            self._error_on_i3bar(short)
        elif long is not None and len(long) < 78:
            self._error_on_i3bar(long)
        else:
            self._error_on_i3bar('Unknown error')
        self.terminate()

    def _update(self, **update):
        # A single block (i.e. a dict) can make changes to all blocks that
        # previously came in a list (and are cached in self._blocks), set new
        # defaults for future blocks, and also change the Worker's config
        # (e.g. 'command' or 'trigger_updates') and environment variables
        # (which will only take effect when 'command' is instantiated again).
        for key,val in update.items():
            if key in self._default_block.VALID_FIELDS:
                self._update_default_block(key, val)
            elif key in self.VALIDATORS_CFG:
                self._update_cfg(key, val)
            else:
                self._update_env(key, val)

        errors_found = self._check_errors()
        if not errors_found:
            if self._rerun_command:
                # Run command AFTER all other values are processed so changes to
                # environment variables, etc take effect.
                self.run()
            else:
                self._generate_json()

    def _update_cfg(self, key, val):
        try:
            self._cfg[key] = val
        except ValueError as e:
            self._croak('Invalid {} value: {}'.format(repr(key), e))
        else:
            if self._initialized and key == 'command':
                self._log.info('Resetting %s = %s', key, repr(val))
                self._rerun_command = True

    def _update_env(self, key, val):
        self._log.info('Setting environment variable %s = %s', key, repr(val))
        self._env[key] = val

    def _update_default_block(self, key, val):
        self._default_block[key] = val
        for blockid in self._blockids:
            self._update_block(blockid, key, val)
            # self._log.debug('Setting %s of block %s = %s', key, blockid, val)

    def _update_block(self, blockid, key=None, value=None, **values):
        block = self._blocks[blockid]
        if key is not None:
            if value is None:
                raise TypeError("Missing 'value' argument")
            else:
                block[key] = value
        block.update(**values)

    def _update_blocks_only(self, *blocks):
        # A list of blocks can only make changes to each block, not the
        # default block.

        # Preserve correct order of block ids
        new_blockids = []
        for block in blocks:
            try:
                # ID is either 'name' or 'instance'
                blockid = block['name'] if 'name' in block else block['instance']
                if blockid in new_blockids:
                    self._croak(long="'name' or 'instance' field not unique: {}".format(blockid),
                                short='Non-unique name/instance')
                    return
                else:
                    new_blockids.append(blockid)
            except KeyError:
                self._croak(long="Missing 'name' or 'instance' field: {}".format(block),
                            short='Block name/instance missing')
                return
            except TypeError as e:
                self._croak(long="Invalid block type: {}".format(block),
                            short='Block type error')
                return

        #self._log.debug('Block order: %s', new_blockids)

        # Remove blocks from cache that are not in new list
        for blockid in tuple(self._blockids):
            if blockid not in new_blockids:
                # self._log.debug('Removing #%s', blockid)
                self._remove_block(blockid)

        # Update/Add blocks
        for index,(blockid,block) in enumerate(zip(new_blockids,blocks)):
            if blockid not in self._blockids:
                # self._log.debug('Inserting new block #%s at index %s', blockid, index)
                self._blockids.insert(index, blockid)
                self._blocks[blockid] = self._default_block.copy()
            # self._log.debug('Updating #%s with %s', blockid, block)
            self._update_block(blockid, **block)

            # Move blocks if order has changed
            if blockid != self._blockids[index]:
                # self._log.debug('Moving #%s from %s to %s',
                #                 blockid, self._blockids.index(blockid), index)
                self._swap_blocks(self._blockids.index(blockid), index)

        errors_found = self._check_errors()
        if not errors_found:
            # Last (rightmost) block inherits 'separator' and
            # 'separator_block_width' from defaults.
            if self._blocks:
                last_blockid = self._blockids[-1]
                last_block = self._blocks[last_blockid]
                # self._log.info('Resetting {} of #{}'.format(self.LAST_BLOCK_RESET_KEYS, last_blockid))
                for reset_key in self.LAST_BLOCK_RESET_KEYS:
                    if reset_key in last_block:
                        if reset_key in self._default_block:
                            last_block[reset_key] = self._default_block[reset_key]
                        else:
                            del(last_block[reset_key])  # Use i3bar default

            self._generate_json()

    def _remove_block(self, blockid):
        del(self._blocks[blockid])
        self._blockids.remove(blockid)

    def _swap_blocks(self, i, j):
        blockid = self._blockids[i]
        self._blockids[i] = self._blockids[j]
        self._blockids[j] = blockid

    @property
    def json(self):
        self._stdout_pending = False
        return self._stdout_cache

    @property
    def stdout_pending(self):
        return self._stdout_pending

    @property
    def triggers_updates(self):
        return self._cfg['trigger_updates']

    @property
    def name(self):
        return self._name

    @property
    def is_static(self):
        return not bool(self._cfg['command'])

    @property
    def is_running(self):
        """Whether a command is defined and it currently is being executed"""
        return self._proc is not None and self._proc.poll() is None

    def terminate(self):
        self._rerun_command = False
        if self.is_running:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=constants.SIGTERM_TIMEOUT)
            except subprocess.TimeoutExpired:
                self._proc.kill()
                self._log.error('No reaction - Killed after %d seconds',
                                constants.SIGTERM_TIMEOUT)
        self._check_command_result()

    def _check_command_result(self):
        """If process was running, report how it ended"""
        if self._proc is not None and self._proc.poll() is not None:
            if self._proc.returncode == 0:
                self._log.info('Terminated gracefully')
            elif self._proc.returncode < 0:
                self._log.info('Terminated by %s', constants.SIGNAMES[-self._proc.returncode])
            else:
                self._log.error('Died with exit code %d', self._proc.returncode)
                self._error_on_i3bar('{} died'.format(self.name))
            self._proc = None

    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, self.name)


class WorkerManager():
    def __init__(self, cfg):
        self._cfg = cfg
        self._workers = []
        self._readpool = Readpool()

        for name in self._cfg.order:
            worker = Worker(self._readpool, **self._cfg.sections[name])
            self._workers.append(worker)

        if not self._workers:
            raise config.ConfigError('No workers specified.')

        elif not any(worker.triggers_updates for worker in self._workers):
            raise config.ConfigError(
                'All workers have "trigger_updates" disabled. '
                'Your i3bar will never display anything with this configuration.')

    def run(self):
        """Handle output from all workers simultaneously"""

        if self._cfg['show_updates']:
            self._updates = []  # List of timestamps of each update

        for worker in self._workers:
            worker.run()

        # print('{ "version":1, "click_events": false }')
        # print('[[],')

        # # In case all workers are either static (command='') or don't trigger
        # # updates, update i3bar now, because readpool.read() will block for  and let read() block forever. We can't
        # # exit because that makes i3bar think something went wrong.
        # if all(worker.is_static or not worker.triggers_updates
        #        for worker in self._workers):

        # Update workers that are either static (no command) or don't trigger
        # updates.
        self._update_i3bar()
        while True:
            self._readpool.read(delay=self._cfg['delay'], timeout=1)
            if any(w.stdout_pending for w in self._workers):
                self._update_i3bar()

    def _update_i3bar(self):
        output = '['
        for worker in self._workers:
            output += worker.json + ','

        if hasattr(self, '_updates'):
            duration = 10  # seconds
            now = time.time()
            while self._updates and now - self._updates[0] > duration:
                self._updates.pop(0)

            if self._updates:
                real_duration = now - self._updates[0]
                ups = len(self._updates) / real_duration
                output += ('{"full_text": "%4.1f u/s"}' % ups) + ','
            else:
                output += '{"full_text": " 0.0 u/s"},'
            self._updates.append(time.time())

        output = output[:-1] + '],'
        print(output)

    def terminate(self):
        for worker in self._workers:
            worker.terminate()
