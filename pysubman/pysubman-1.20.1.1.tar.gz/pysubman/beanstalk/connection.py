#!/usr/bin/env python

import logging
import socket
import sys
from .constants import CRLF, DEFAULT_PRIORITY, DEFAULT_TTR


class BJob(object):
    def __init__(self, jid, body, reserved):
        self.jid = jid
        self.body = body
        self.reserved = reserved

    def bury(self, connection, priority=None):
        if self.reserved:
            connection.bury(self.jid, priority or DEFAULT_PRIORITY)
            self.reserved = False


class UnexpectedResponse(Exception):
    pass


class CommandFailed(Exception):
    pass


class DeadlineSoon(Exception):
    pass


class SocketError(Exception):
    @staticmethod
    def wrap(wrapped_function, *args, **kwargs):
        try:
            return wrapped_function(*args, **kwargs)
        except socket.error:
            err = sys.exc_info()[1]
            raise SocketError(err)


class Connection(object):
    def __init__(self, address, parse_yaml=True,
                 connect_timeout=socket.getdefaulttimeout()):

        if parse_yaml is True:
            try:
                parse_yaml = __import__('yaml').load
            except ImportError:
                logging.error('Failed to load PyYAML, will not parse YAML')
                parse_yaml = False

        self.host, self.port = address.split(":")
        self.port = int(self.port)

        self._connect_timeout = connect_timeout
        self._parse_yaml = parse_yaml or (lambda x: x)
        self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        """Connect to beanstalkd server."""

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(self._connect_timeout)
        SocketError.wrap(self._socket.connect, (self.host, self.port))
        self._socket.settimeout(None)
        self._socket_file = self._socket.makefile('rb')

    def close(self):
        """Close connection to server."""

        try:
            self._socket.sendall('quit\r\n')
        except socket.error:
            pass

        try:
            self._socket.close()
        except socket.error:
            pass

    def reconnect(self):
        """Re-connect to server."""

        self.close()
        self.connect()

    def _interact(self, command, expected_ok, expected_err=[]):
        SocketError.wrap(self._socket.sendall, command)
        status, results = self._read_response()
        import logging
        logging.warn(("**", command, status, results))
        if status in expected_ok:
            return results

        command_n = command.split(" ")[0]
        if status in expected_err:
            raise CommandFailed(command_n, status, results)
        raise UnexpectedResponse(command_n, status, results)

    def _read_response(self):
        line = SocketError.wrap(self._socket_file.readline)
        if not line:
            raise SocketError()
        response = line.split()
        return response[0], response[1:]

    def _read_body(self, size):
        body = SocketError.wrap(self._socket_file.read, size)
        if size > 0 and not body:
            raise SocketError()

        suffix = SocketError.wrap(self._socket_file.read, 2)  # trailing crlf
        if not suffix or suffix != CRLF:
            raise SocketError()
        return body

    def _interact_value(self, command, expected_ok, expected_err=[]):
        return self._interact(command, expected_ok, expected_err)[0]

    def _interact_job(self, command, expected_ok, expected_err, reserved=True):
        jid, size = self._interact(command, expected_ok, expected_err)
        body = self._read_body(int(size))
        return BJob(int(jid), body, reserved)

    def _interact_yaml(self, command, expected_ok, expected_err=[]):
        size, = self._interact(command, expected_ok, expected_err)
        body = self._read_body(int(size))
        return self._parse_yaml(body)

    def _interact_peek(self, command):
        try:
            return self._interact_job(command, ['FOUND'], ['NOT_FOUND'], False)
        except CommandFailed:
            return None

    # -- public interface --
    def put(self, body, priority=2 ** 31, delay=0, ttr=DEFAULT_TTR):
        """Put a job into the current tube. Returns job id."""

        assert isinstance(body, str), 'Job body must be a str instance'
        jid = self._interact_value(
            'put %d %d %d %d\r\n%s\r\n' % (priority, delay, ttr, len(body), body),
            ['INSERTED'], ['JOB_TOO_BIG', 'BURIED', 'DRAINING'])
        return int(jid)

    def reserve(self, timeout=None):
        """Reserve a job from one of the watched tubes, with optional timeout
        in seconds. Returns a Job object, or None if the request times out."""
        command = 'reserve\r\n'
        if timeout is not None:
            command = 'reserve-with-timeout %d\r\n' % timeout

        try:
            return self._interact_job(
                command,
                ['RESERVED'],
                ['DEADLINE_SOON', 'TIMED_OUT'])
        except CommandFailed:
            exc = sys.exc_info()[1]
            _, status, results = exc.args
            if status == 'TIMED_OUT':
                return None

            if status == 'DEADLINE_SOON':
                raise DeadlineSoon(results)

    def kick(self, bound=1):
        """Kick at most bound jobs into the ready queue."""

        return int(self._interact_value('kick %d\r\n' % bound, ['KICKED']))

    def kick_job(self, jid):
        """Kick a specific job into the ready queue."""

        self._interact('kick-job %d\r\n' % jid, ['KICKED'], ['NOT_FOUND'])

    def peek(self, jid):
        """Peek at a job. Returns a Job, or None."""

        return self._interact_peek('peek %d\r\n' % jid)

    def peek_ready(self):
        """Peek at next ready job. Returns a Job, or None."""

        return self._interact_peek('peek-ready\r\n')

    def peek_delayed(self):
        """Peek at next delayed job. Returns a Job, or None."""

        return self._interact_peek('peek-delayed\r\n')

    def peek_buried(self):
        """Peek at next buried job. Returns a Job, or None."""

        return self._interact_peek('peek-buried\r\n')

    def tubes(self):
        """Return a list of all existing tubes."""

        return self._interact_yaml('list-tubes\r\n', ['OK'])

    def using(self):
        """Return the tube currently being used."""

        return self._interact_value('list-tube-used\r\n', ['USING'])

    def use(self, name):
        """Use a given tube."""

        return self._interact_value('use %s\r\n' % name, ['USING'])

    def watching(self):
        """Return a list of all tubes being watched."""

        return self._interact_yaml('list-tubes-watched\r\n', ['OK'])

    def watch(self, name):
        """Watch a given tube."""

        return int(self._interact_value('watch %s\r\n' % name, ['WATCHING']))

    def ignore(self, name):
        """Stop watching a given tube."""

        try:
            return int(self._interact_value('ignore %s\r\n' % name,
                                            ['WATCHING'],
                                            ['NOT_IGNORED']))
        except CommandFailed:
            return 1

    def stats(self):
        """Return a dict of beanstalkd statistics."""

        return self._interact_yaml('stats\r\n', ['OK'])

    def stats_tube(self, name):
        """Return a dict of stats about a given tube."""

        return self._interact_yaml('stats-tube %s\r\n' % name,
                                   ['OK'],
                                   ['NOT_FOUND'])

    def pause_tube(self, name, delay):
        """Pause a tube for a given delay time, in seconds."""
        self._interact('pause-tube %s %d\r\n' % (name, delay),
                       ['PAUSED'],
                       ['NOT_FOUND'])

    # -- job interactors --
    def delete(self, jid):
        """Delete a job, by job id."""
        self._interact('delete %d\r\n' % jid, ['DELETED'], ['NOT_FOUND'])

    def release(self, jid, priority=DEFAULT_PRIORITY, delay=0):
        """Release a reserved job back into the ready queue."""
        self._interact('release %d %d %d\r\n' % (jid, priority, delay),
                       ['RELEASED', 'BURIED'],
                       ['NOT_FOUND'])

    def bury(self, jid, priority=DEFAULT_PRIORITY):
        """Bury a job, by job id."""
        self._interact('bury %d %d\r\n' % (jid, priority),
                       ['BURIED'],
                       ['NOT_FOUND'])

    def touch(self, jid):
        """Touch a job, by job id, requesting more time to work on a reserved
        job before it expires."""
        self._interact('touch %d\r\n' % jid, ['TOUCHED'], ['NOT_FOUND'])

    def stats_job(self, jid):
        """Return a dict of stats about a job, by job id."""
        return self._interact_yaml('stats-job %d\r\n' % jid,
                                   ['OK'],
                                   ['NOT_FOUND'])
