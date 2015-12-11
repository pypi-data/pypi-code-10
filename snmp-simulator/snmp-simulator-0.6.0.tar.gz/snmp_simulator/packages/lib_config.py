# -*- coding: utf-8 -*-
"""
    lib_config
    ~~~~~~~~~~
    CLI utility
    :copyright: (c) 2014-2015 Dmitry Korobitsin <https://github.com/korobitsin>
    :license: BSD, see LICENSE
"""

__version__ = '1.2.0'
__description__ = 'Unified config (default, .ini file, arguments), log file, pid file, locking'

import os
import sys
import codecs
import logging
import logging.handlers

log = logging.getLogger('config')
configs = {}


def getConfig(name, *args):
    global configs
    config = configs.get(name, None)
    if config is None:
        config = Config(name)
    for arg in args:
        configs[arg] = config
    configs[name] = config
    return config


class ConfigOption(object):
    def __init__(self, name, default=None, precedence=0, shortcut=None, otype=str, possible_values=None, description=None, order=0):
        self.name = name
        self.order = order
        self.value = default
        self.precedence = precedence
        self.shortcut = shortcut
        self.otype = otype
        self.possible_values = possible_values
        self.default = default
        self.description = description

    def set_value(self, value, precedence=0):
        if precedence >= self.precedence:
            self.value = value
            self.precedence = precedence

    def get_value(self, config):
        value = self.value
        if self.otype == str:
            value %= config
        elif self.otype == list:
            value = list(self.value)
            for i in xrange(len(value)):
                if isinstance(value[i], str) or isinstance(value[i], unicode):
                    value[i] %= config
        return value

    def validate(self):
        if self.value is None:
            sys.stderr.write('Missing option, name=%s, shortcut="%s", description="%s", possible_values=%s\n' % \
                  (self.name, self.shortcut, self.description, self.possible_values))
            return False
        if not isinstance(self.value, self.otype):
            sys.stderr.write('Value=%s not accepted, name=%s, type=%s, otype=%s\n' % \
                  (self.value.__repr__(), self.name, self.value.__class__, self.otype))
            return False
        if self.possible_values:
            if self.otype == list:
                for value in self.value:
                    if not value in self.possible_values:
                        sys.stderr.write('Value=%s not accepted, value_list=%s, name=%s, description="%s", possible values=%s\n' % \
                              (value.__repr__(), self.value.__repr__(), self.name, self.description, self.possible_values.__repr__()))
                        return False
            else:
                if not self.value in self.possible_values:
                    sys.stderr.write('Value=%s not accepted, name=%s, description="%s", possible values=%s\n' % \
                          (self.value.__repr__(), self.name, self.description, self.possible_values.__repr__()))
                    return False
        return True

    def __str__(self):
        if self.value == self.default:
            return '%s = %s' % (self.name, self.value.__repr__())
        return '*%s = %s (%s)' % (self.name, self.value.__repr__(), self.default.__repr__())

    def __repr__(self):
        return '%s = %s' % (self.name, self.value.__repr__())


class Config(object):
    def __init__(self, name):
        self._name = name
        self._initialized = False
        self._options = {}
        self._localization = {}
        self._pidfile = None
        self._locks = {}
        _setup_default_options(self)

    def __getattr__(self, name):
        if not name in self._options:
            raise Exception('No such attribute in the config, name=%s' % name)
        return self._options[name].get_value(self)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            return object.__setattr__(self, name, value)
        if not name in self._options:
            raise Exception('No such attribute in the config, name=%s' % name)
        self._options[name].set_value(value, precedence=10)

    def __getitem__(self, key):
        return self._options[key].get_value(self)

    def add_option(self, name, shortcut=None, otype=str, possible_values=None, default=None, desc=''):
        self._options[name] = ConfigOption(name=name, shortcut=shortcut, otype=otype, possible_values=possible_values, default=default, description=desc)

    def setup(self, parse_cli=True, parse_cfg=True, verify=True, log=True, pid=True):
        if self._initialized:
            return
        parse_cli and self._parse_command_line()
        parse_cfg and self._parse_config_file()
        verify and self._verify_options()
        log and self._create_log_file()
        pid and self._create_pid_file()
        self._initialized = True

    def touch_pid_file(self):
        try:
            os.utime(self._pidfile.filename, None)
            log.debug('Pid file touched: "%s"' % self._pidfile.filename)
        except Exception, e:
            log.exception('Cannot touch the pid file: %s' % str(e))

    def remove_pid_file(self):
        self._pidfile.remove()

    def obtain_lock(self, lock_target, block=True):
        return self._lock(lock_target=lock_target, block=block, action='obtain')

    def release_lock(self, lock_target):
        return self._lock(lock_target=lock_target, action='release')

    def _parse_command_line(self):
        import optparse
        parser = optparse.OptionParser(usage='usage: %prog [options]')

        for option in self._options.itervalues():
            args = ['--%s' % option.name]
            kwargs = dict(action='store', type='string', dest=option.name, help=option.description)
            if option.shortcut:
                args.append(option.shortcut)
            if option.otype == bool:
                kwargs['action'] = 'store_true'
                kwargs['type'] = None
                parser.add_option('--no_%s' % option.name, action='store_false', dest=option.name, help='Disable %s' % option.description)
            elif option.otype == int:
                kwargs['type'] = 'int'
            parser.add_option(*args, **kwargs)

        cli_options, args = parser.parse_args()
        for option in self._options.itervalues():
            cli_value = getattr(cli_options, option.name)
            if option.otype == list:
                cli_value = _string_list(cli_value)
            if cli_value is not None:
                option.set_value(cli_value, precedence=2)

    def _parse_config_file(self):
        import ConfigParser
        if not self.config_file:
            self._options['config_file'].validate()
        parser = ConfigParser.RawConfigParser()
        try:
            parser.readfp(codecs.open(self.config_file, 'r', 'utf-8'))
        except IOError, e:
            sys.stderr.write('Cannot open config file: %s\n' % e)
            sys.exit(1)

        for section in parser.sections():
            for option_name in parser.options(section):
                if section == 'global':
                    if option_name in self._options:
                        option = self._options[option_name]
                        value = None
                        if option.otype == str:
                            value = str(parser.get(section, option_name))
                        elif option.otype == bool:
                            value = parser.getboolean(section, option_name)
                        elif option.otype == int:
                            value = parser.getint(section, option_name)
                        elif option.otype == float:
                            value = parser.getfloat(section, option_name)
                        elif option.otype == list:
                            value = _string_list(parser.get(section, option_name))
                        if value is not None:
                            option.set_value(value, precedence=1)
                elif section == 'localization':
                    self._localization[option_name] = parser.get(section, option_name)

    def _verify_options(self):
        valid = True
        for option in self._options.itervalues():
            valid &= option.validate()
        self.dump_config and self._dump_config()
        if not valid:
            sys.stderr.write('Config not valid\n')
            sys.exit(1)

    def _dump_config(self):
        for option in self._options.itervalues():
            sys.stderr.write('%s' % option)
        sys.exit(0)

    def _create_log_file(self):
        root_log = logging.getLogger(self.log_root)
        log_filename = os.path.join(self.logdir, self.log_filename)
        formatter = logging.Formatter('%(asctime)s %(process)5d %(name)s %(levelname)-5s %(message)s')

        if self.log_stdout:
            stdout = logging.StreamHandler(sys.stdout)
            stdout.setFormatter(formatter)
            root_log.addHandler(stdout)

        if self.log_type in ('file', 'rotating_file') and not os.path.isdir(self.logdir):
            log.info('Creating folders for path %s' % self.logdir)
            os.makedirs(self.logdir)

        if self.log_type == 'file':
            plain_file = logging.FileHandler(filename=log_filename, mode=self.log_mode)
            plain_file.setFormatter(formatter)
            root_log.addHandler(plain_file)

        if self.log_type == 'rotating_file':
            rotating_file = logging.handlers.RotatingFileHandler(filename=log_filename, mode=self.log_mode, maxBytes=self.log_max_size,
                                                                 backupCount=self.log_max_files)
            rotating_file.setFormatter(formatter)
            root_log.addHandler(rotating_file)
            if self.log_rollover:
                rotating_file.doRollover()

        root_log.setLevel(getattr(logging, self.log_level.upper()))

    def _create_pid_file(self):
        if not os.path.isdir(self.vardir):
            log.info('Creating folders for path %s' % self.vardir)
            os.makedirs(self.vardir)
        self._pidfile = PidFile(os.path.join(self.vardir, '%s.pid' % self.script))

    def _lock(self, lock_target, block=True, action='obtain'):
        try:
            import fcntl
        except ImportError:
            raise Exception('Locking not supported by platform')
        if action == 'obtain':
            log.debug('obtaining a lock target=%s block=%s' % (lock_target, block))
            lock_file = '%s/%s.lock' % (self.vardir, lock_target)
            if not os.path.exists(lock_file):
                open(lock_file, 'w').close()
            fd = open(lock_file, 'w')
            if block:
                fcntl.flock(fd, fcntl.LOCK_EX)
            else:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except IOError:
                    log.warning('failed to obtain a lock target=%s block=%s' % (lock_target, block))
                    fd.close()
                    return False
            log.debug('lock obtained target=%s block=%s' % (lock_target, block))
            self._locks[lock_target] = fd
            return True
        elif action == 'release':
            if lock_target in self._locks:
                fd = self._locks[lock_target]
                fcntl.flock(fd, fcntl.LOCK_UN)
                fd.close()
                log.info('lock released target=%s' % lock_target)
        return False


class PidFile(object):
    """
    Creates, removes and check for existence of a pid file for the running script.
    """

    def __init__(self, filename, force=False):
        self.filename = filename
        self.force = force
        self._detect()

    def _detect(self):
        """
        Look for existing pid file
        """
        if os.path.isfile(self.filename):
            if self.force:
                self._create()
                log.error('Existing pid file, but forced to re-create it')
            else:
                import datetime
                pid = open(self.filename).readline().strip()
                mtime = datetime.datetime.fromtimestamp(os.stat(self.filename).st_mtime)
                log.info('Existing pid file, pid: %s, modif time: %s' % (pid, mtime))
                if pid and _check_pid(int(pid)):
                    log.info('Process is still running with pid=%s, exiting application' % pid)
                    sys.exit(1)
                else:
                    log.warning('Not running, re-creating pid file pid=%s' % pid)
                    self._create()
        else:
            self._create()

    def _create(self):
        fd = open(self.filename, 'w')
        fd.write('%s\n' % os.getpid())
        fd.close()
        log.debug('Created pid file: "%s"' % self.filename)

    def remove(self):
        try:
            os.unlink(self.filename)
            log.debug('Pid file removed: "%s"' % self.filename)
        except OSError, e:
            log.exception('Cannot remove pid file: %s' % str(e))


def _check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def _string_list(string):
    if string:
        return [chunk.strip() for chunk in string.split(',')]
    return None


def _setup_default_options(conf):
    conf.add_option(name='script', default=conf._name, desc='script instance name')
    conf.add_option(name='log_root', default='', desc='root logger name')
    conf.add_option(name='log_level', default='info', possible_values=('debug', 'info', 'warning', 'error', 'exception'), desc='logging level')
    conf.add_option(name='log_type', default='rotating_file', possible_values=('rotating_file', 'file'), desc='logging type')
    conf.add_option(name='log_mode', default='a', possible_values=('a', 'w'), desc='logging file access mode')
    conf.add_option(name='log_rollover', default=False, otype=bool, desc='logging do rollover at start')
    conf.add_option(name='log_max_files', default=10, otype=int, desc='logging max files')
    conf.add_option(name='log_max_size', default=1024 * 1024 * 2, otype=int, desc='logging max file size')
    conf.add_option(name='log_stdout', default=False, shortcut='-s', otype=bool, desc='log to stdout')
    conf.add_option(name='log_filename', default='%(script)s.log')
    conf.add_option(name='debug', default=False, otype=bool, desc='development mode')
    conf.add_option(name='basedir', default=os.path.abspath('%s/../../' % sys.argv[0]))
    conf.add_option(name='logdir', default='%(basedir)s/log')
    conf.add_option(name='vardir', default='%(basedir)s/var')
    conf.add_option(name='etcdir', default='%(basedir)s/etc')
    conf.add_option(name='tmpdir', default='%(basedir)s/tmp')
    conf.add_option(name='config_file', shortcut='-c', default='%(basedir)s/etc/%(script)s.conf')
    conf.add_option(name='dump_config', default=False, otype=bool, desc='Dump conf options to screen')
