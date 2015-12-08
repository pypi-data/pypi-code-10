#!/usr/bin/env python
import argparse
import itertools
import logging
import re
import select
import socket
import sys
from threading import Event, Thread


_global_kill = Event()


class UdpRelay(Thread):
    '''
    A threaded (i.e. subclass of :class:`~python:threading.Thread`) worker
    which listens on two UDP sockets, one bound to :attr:`host_a` and
    :attr:`port_a`, another bound to :attr:`host_b` and :attr:`port_b`. When a
    message is received on one socket, destined for that socket, it is sent to
    the other using the other socket.

    For example, say we create the following :class:`UdpRelay` where "host A"
    is at `192.168.56.1`, "host B" is at `192.168.56.3`, and the machine the
    relay is running on, which we call the "local machine", is at
    `192.168.56.2`:

    .. code-block:: python

       r = UdpRelay('192.168.56.1', 5600, '192.168.56.3', 5602)

    The relay will create two UDP sockets, one bound to *any* interface but to
    port 5600 and another bound to *any* interface but to port 5602. We'll call
    these sockets "socket A" and "socket B" respectively.

    When "host A" sends a message to the "local machine" to port 5600 the local
    machine will receive that on "socket A". When it receives the message it
    checks to see if it came from "host A". Since it did it will then send the
    same message to "host B" but using "socket B" as the outgoing socket. The
    same happens in reverse if "host B" send a message to the local machine to
    port 5602.

    The effect is that "host A" and "host B" think they are talking to each
    other even though they are actually both talking to "local machine".
    '''

    @property
    def host_a(self):
        '''
        Gets the address for host A.
        '''
        return self._host_a

    @property
    def port_a(self):
        '''
        Gets the port for host A.
        '''
        return self._port_a

    @property
    def host_b(self):
        '''
        Gets the address for host B.
        '''
        return self._host_b

    @property
    def port_b(self):
        '''
        Gets the port for host B.
        '''
        return self._port_b

    @property
    def max_message_size(self):
        '''
        Gets or sets the max message size (in bytes) when messages are received
        (see :meth:`python:socket.socket.recv`).
        '''
        return self._max_message_size

    @max_message_size.setter
    def max_message_size(self, value):
        self._max_message_size = value

    @property
    def timeout(self):
        '''
        Gets the timeout, in seconds, for both sockets. Note that having a
        non-infinite timeout is important because the global kill signal is
        checked in between receive timeouts. The global kill signal is used to
        shut down listening threads.
        '''
        return self._timeout

    @property
    def message_middleware(self):
        '''
        Gets or sets the middleware function that is applied to messages before
        they are sent out. It can read or manipulate the message and is
        expected to return the message to be sent as a bytes object. Signature
        is as follows:

        .. code-block:: python

           def middleware(
                   msg: bytes,
                   src_name: str, src_host: str, src_port: int,
                   dst_name: str, dst_host: str, dst_port: int) -> bytes:
               return msg
        '''
        return self._message_middleware

    @message_middleware.setter
    def message_middleware(self, value):
        self._message_middleware = value

    @property
    def socket_a(self):
        '''
        Get the socket listening for host A messages.
        '''
        return self._socket_a

    @property
    def socket_b(self):
        '''
        Get the socket listening for host B messages.
        '''
        return self._socket_b

    def __init__(
            self,
            host_a, port_a,
            host_b, port_b,
            max_message_size=16384,
            timeout=1.0,
            message_middleware=None):
        global _global_kill

        super(UdpRelay, self).__init__()

        self._host_a, self._port_a = host_a, port_a
        self._host_b, self._port_b = host_b, port_b

        self._logger = logging.getLogger(
            'relay.UdpRelay({_host_a}:{_port_a} <-> {_host_b}:{_port_b})'
            .format(**self.__dict__))

        self._max_message_size = max_message_size
        self._logger.debug(
            'max_message_size={_max_message_size}'
            .format(**self.__dict__))

        self._timeout = timeout
        self._logger.debug(
            'timeout={_timeout}'
            .format(**self.__dict__))

        self._message_middleware = message_middleware
        self._logger.debug(
            'message_middleware={_message_middleware}'
            .format(**self.__dict__))

        self._socket_a, self._socket_b = None, None
        try:
            if self._port_a == self._port_b:
                self._logger.info(
                    'Ports are the same so setting up just one socket')
                self._socket_a = self._createSocket(self._port_a)
                self._socket_b = self._socket_a
                self._sockets = [self._socket_a]
            else:
                self._logger.info(
                    'Ports are different so setting up two sockets')
                self._socket_a = self._createSocket(self._port_a)
                self._socket_b = self._createSocket(self._port_b)
                self._sockets = [self._socket_a, self._socket_b]
        except Exception as e:
            self._logger.error('Error while creating sockets: {:}'.format(e))
            self._logger.warning('Killing program')
            _global_kill.set()

    def _createSocket(self, port):
        '''
        Creates a UDP socket bound to any interface (empty string host address)
        but to the specified port.
        '''
        self._logger.info(
            'Setting up UDP socket to listen to port {:}'.format(port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.settimeout(self._timeout)
        self._logger.info(
            'Successfully set socket timeout to {_timeout}'
            .format(**self.__dict__))

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._logger.info('Successfully set socket option to SO_REUSEADDR')

        sock.bind(('', port))
        self._logger.info(
            'Successfully bound socket to ("", {port})'
            .format(port=port, **self.__dict__))

        return sock

    def __del__(self):
        if self._socket_a is self._socket_b:
            if self._socket_a is not None:
                self._logger.info('Closing socket')
                self._socket_a.close()
        else:
            if self._socket_a is not None:
                self._logger.info('Closing socket A')
                self._socket_a.close()
            if self._socket_b is not None:
                self._logger.info('Closing socket B')
                self._socket_b.close()

    def run(self):
        global _global_kill

        self._logger.info('Starting receive loop...')
        while True:
            try:
                if _global_kill.isSet():
                    self._logger.info('Received global kill')
                    break

                readable, writable, exceptable = select.select(
                    self._sockets, [], [], self._timeout)

                for sock in readable:
                    self._handleReadableSocket(sock)

            except Exception as e:
                self._logger.error(
                    'Caught exception while waiting for message: {:}'
                    .format(e))
                break

        self._logger.info('Terminating')

    def _handleReadableSocket(self, src_socket):
        msg, (src_host, src_port) = src_socket.recvfrom(self._max_message_size)

        if src_socket is self._socket_a:
            target_port = self._port_a
        elif src_socket is self._socket_b:
            target_port = self._port_b
        else:
            self._logger.warn(
                'Handling an unknown listening socket. Ignoring.')
            return

        self._handleMessage(msg, src_host, src_port, target_port)

    def _handleMessage(self, msg, src_host, src_port, target_port):
        self._logger.debug('Message received: {!r}'.format(msg))

        if src_host == self._host_a and target_port == self._port_a:
            src_name, src_host = 'A', self._host_a
            dst_name, dst_host, dst_port = 'B', self._host_b, self._port_b
            dst_socket = self._socket_b
        elif src_host == self._host_b and target_port == self._port_b:
            src_name, src_host = 'B', self._host_b
            dst_name, dst_host, dst_port = 'A', self._host_a, self._port_a
            dst_socket = self._socket_a
        else:
            self._logger.warning(
                'Message received from unknown host ({!s}:{!s} to port {!s}). '
                'Ignoring.'
                .format(src_host, src_port, target_port))
            return

        self._logger.debug(
            'Message received from host {:} ({!s}:{!s} to port {!s}), routing '
            'to host {:} ({!s}:{!s})'
            .format(
                src_name, src_host, src_port, target_port,
                dst_name, dst_host, dst_port))

        if self._message_middleware is not None:
            msg = self._message_middleware(
                msg,
                src_name, src_host, src_port,
                dst_name, dst_host, dst_port)

        dst_socket.sendto(msg, (dst_host, dst_port))


class TcpRelay(Thread):
    '''
    A threaded (i.e. subclass of :class:`~python:threading.Thread`) worker
    which listens on two TCP sockets, one connected to :attr:`host_a` and
    :attr:`port_a`, another connected to :attr:`host_b` and :attr:`port_b`.
    When a message is received on one socket, from one host, it is sent to the
    other host using the other socket.
    '''

    @property
    def socket_a(self):
        '''
        Get the socket listening for host A messages.
        '''
        return self._socket_a

    @property
    def socket_b(self):
        '''
        Get the socket listening for host B messages.
        '''
        return self._socket_b

    @property
    def host_a(self):
        '''
        Gets the address for host A.
        '''
        return self._host_a

    @property
    def port_a(self):
        '''
        Gets the port for host A.
        '''
        return self._port_a

    @property
    def host_b(self):
        '''
        Gets the address for host B.
        '''
        return self._host_b

    @property
    def port_b(self):
        '''
        Gets the port for host B.
        '''
        return self._port_b

    @property
    def max_message_size(self):
        '''
        Gets or sets the max message size (in bytes) when messages are received
        (see :meth:`python:socket.socket.recv`).
        '''
        return self._max_message_size

    @max_message_size.setter
    def max_message_size(self, value):
        self._max_message_size = value

    @property
    def timeout(self):
        '''
        Gets the timeout, in seconds, for both sockets. Note that having a
        non-infinite timeout is important because the global kill signal is
        checked in between receive timeouts. The global kill signal is used to
        shut down listening threads.
        '''
        return self._timeout

    @property
    def message_middleware(self):
        '''
        Gets or sets the middleware function that is applied to messages before
        they are sent out. It can read or manipulate the message and is
        expected to return the message to be sent as a bytes object. Signature
        is as follows:

        .. code-block:: python

           def middleware(
                   msg: bytes,
                   src_name: str, src_host: str, src_port: int,
                   dst_name: str, dst_host: str, dst_port: int) -> bytes:
               return msg
        '''
        return self._message_middleware

    @message_middleware.setter
    def message_middleware(self, value):
        self._message_middleware = value

    def __init__(
            self,
            socket_a, host_a, port_a,
            socket_b, host_b, port_b,
            max_message_size=16384,
            timeout=1.0,
            message_middleware=None):

        super(TcpRelay, self).__init__()

        self._socket_a, self._host_a, self._port_a = socket_a, host_a, port_a
        self._socket_b, self._host_b, self._port_b = socket_b, host_b, port_b
        self._max_message_size = max_message_size
        self._timeout = timeout
        self._message_middleware = message_middleware

        self._sockets = [self._socket_a, self._socket_b]

        self._logger = logging.getLogger(
            'relay.TcpRelay({_host_a}:{_port_a} <-> {_host_b}:{_port_b})'
            .format(**self.__dict__))

    def __del__(self):
        self._logger.info('Closing sockets')
        self._socket_a.close()
        self._socket_b.close()

    def run(self):
        global _global_kill

        self._logger.info('Starting receive loop...')
        while True:
            try:
                if _global_kill.isSet():
                    self._logger.info('Received global kill')
                    break

                readable, writable, exceptable = select.select(
                    self._sockets, [], [], self._timeout)

                disconnect = False
                for sock in readable:
                    disconnect = disconnect or self._handleReadableSocket(sock)

                if disconnect:
                    self._logger.info(
                        'One of the connections closed, closing entire relay')
                    break

            except Exception as e:
                self._logger.error(
                    'Caught exception while waiting for "recv": {:}'
                    .format(e))
                break

        self._logger.info('Terminating')

    def _handleReadableSocket(self, src_socket):
        '''
        :returns: :data:`python:True` if the connect has been disconnected and
                  :data:`python:False` if the connection is still alive and
                  everything was processed normally
        '''
        msg = src_socket.recv(self._max_message_size)
        return self._handleMessage(src_socket, msg)

    def _handleMessage(self, src_socket, msg):
        self._logger.debug('Message received: {!r}'.format(msg))

        if src_socket is self._socket_a:
            src_name, src_host, src_port = 'A', self._host_a, self._port_a
            dst_name, dst_host, dst_port = 'B', self._host_b, self._port_b
            dst_socket = self._socket_b
        elif src_socket is self._socket_b:
            src_name, src_host, src_port = 'B', self._host_b, self._port_b
            dst_name, dst_host, dst_port = 'A', self._host_a, self._port_a
            dst_socket = self._socket_a
        else:
            self._logger.warning(
                'Message received from unknown socket! How is '
                'this possible?! Ignoring.')
            return False

        self._logger.debug(
            'Message received from host {:} ({!s}:{!s}), routing to host {:} '
            '({!s}:{!s})'
            .format(
                src_name, src_host, src_port,
                dst_name, dst_host, dst_port))

        if not msg or msg == '':
            self._logger.info(
                'Connection to host {:} closed'.format(src_name))
            return True

        if self._message_middleware is not None:
            msg = self._message_middleware(
                msg,
                src_name, src_host, src_port,
                dst_name, dst_host, dst_port)

        dst_socket.send(msg)

        return False


class TcpRelayServer(Thread):
    '''
    A threaded (i.e. subclass of :class:`~python:threading.Thread`) worker
    which listens for connections from :attr:`host_a` and :attr:`port_a` or
    from :attr:`host_b` and :attr:`port_b`. When a connection is received from
    one host a forwarding connection is made to the other host and a
    :class:`TcpRelay` is created to facilitate forwarding.
    '''

    @property
    def host_a(self):
        '''
        Gets the address for host A.
        '''
        return self._host_a

    @property
    def port_a(self):
        '''
        Gets the port for host A.
        '''
        return self._port_a

    @property
    def host_b(self):
        '''
        Gets the address for host B.
        '''
        return self._host_b

    @property
    def port_b(self):
        '''
        Gets the port for host B.
        '''
        return self._port_b

    @property
    def max_message_size(self):
        '''
        Gets or sets the max message size (in bytes) when messages are received
        (see :meth:`python:socket.socket.recv`).
        '''
        return self._max_message_size

    @max_message_size.setter
    def max_message_size(self, value):
        self._max_message_size = value

    @property
    def timeout(self):
        '''
        Gets the timeout, in seconds, for both sockets. Note that having a
        non-infinite timeout is important because the global kill signal is
        checked in between receive timeouts. The global kill signal is used to
        shut down listening threads.
        '''
        return self._timeout

    @property
    def backlog(self):
        '''
        Gets the number of backlog connections allowed. See
        :meth:`python:socket.socket.backlog`.
        '''
        return self._backlog

    @property
    def message_middleware(self):
        '''
        Gets or sets the middleware function that is applied to messages before
        they are sent out. It can read or manipulate the message and is
        expected to return the message to be sent as a bytes object. Signature
        is as follows:

        .. code-block:: python

           def middleware(
                   msg: bytes,
                   src_name: str, src_host: str, src_port: int,
                   dst_name: str, dst_host: str, dst_port: int) -> bytes:
               return msg
        '''
        return self._message_middleware

    @message_middleware.setter
    def message_middleware(self, value):
        self._message_middleware = value

    @property
    def socket_a(self):
        '''
        Get the socket listening for host A connections.
        '''
        return self._socket_a

    @property
    def socket_b(self):
        '''
        Get the socket listening for host B connections.
        '''
        return self._socket_b

    def __init__(
            self,
            host_a, port_a,
            host_b, port_b,
            max_message_size=16384,
            timeout=1.0,
            backlog=5,
            message_middleware=None):

        super(TcpRelayServer, self).__init__()

        self._host_a, self._port_a = host_a, port_a
        self._host_b, self._port_b = host_b, port_b
        self._max_message_size = max_message_size
        self._timeout = timeout
        self._backlog = backlog
        self._message_middleware = message_middleware

        self._logger = logging.getLogger(
            'relay.TcpRelayServer({_host_a}:{_port_a} <-> {_host_b}:{_port_b})'
            .format(**self.__dict__))

        self._socket_a, self._socket_b = None, None
        try:
            if self._port_a == self._port_b:
                self._logger.info(
                    'Ports are the same so setting up just one listening '
                    'socket')
                self._socket_a = self._createSocket(self._port_a)
                self._socket_b = self._socket_a
                self._sockets = [self._socket_a]
            else:
                self._logger.info(
                    'Ports are different so setting up two listening sockets')
                self._socket_a = self._createSocket(self._port_a)
                self._socket_b = self._createSocket(self._port_b)
                self._sockets = [self._socket_a, self._socket_b]
        except Exception as e:
            self._logger.error('Error while creating sockets: {:}'.format(e))
            self._logger.warning('Killing program')
            _global_kill.set()

    def _createSocket(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.settimeout(self._timeout)
        self._logger.info(
            'Successfully set socket timeout to {_timeout}'
            .format(**self.__dict__))

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._logger.info('Successfully set socket option to SO_REUSEADDR')

        self._logger.info(
            'Trying to bind socket to ("", {port})'
            .format(port=port, **self.__dict__))
        sock.bind(('', port))
        self._logger.info(
            'Successfully bound socket to ("", {port})'
            .format(port=port, **self.__dict__))

        self._logger.info(
            'Trying to start listenining to socket'
            .format(**self.__dict__))
        sock.listen(self._backlog)
        self._logger.info(
            'Successfully started listening to socket (backlog={_backlog})'
            .format(**self.__dict__))

        return sock

    def __del__(self):
        if self._socket_a is self._socket_b:
            if self._socket_a is not None:
                self._logger.info('Closing socket')
                self._socket_a.close()
        else:
            if self._socket_a is not None:
                self._logger.info('Closing socket A')
                self._socket_a.close()
            if self._socket_b is not None:
                self._logger.info('Closing socket B')
                self._socket_b.close()

    def run(self):
        global _global_kill

        self._logger.info('Starting connection accept loop...')
        while True:
            try:
                # End the accept loop and the whole thread (by breaking) if the
                # global kill signal has been set
                if _global_kill.isSet():
                    self._logger.info('Received global kill')
                    break

                readable, writable, exceptable = select.select(
                    self._sockets, [], [], self._timeout)

                for sock in readable:
                    self._handleReadableSocket(sock)

            except socket.timeout:
                pass

            except Exception as e:
                self._logger.error(
                    'Caught exception while waiting for "accept": {:}'
                    .format(e))
                break

        self._logger.info('Terminating')

    def _handleReadableSocket(self, listening_socket):
        src_socket, (src_host, src_port) = listening_socket.accept()

        if listening_socket is self._socket_a:
            target_port = self._port_a
        elif listening_socket is self._socket_b:
            target_port = self._port_b
        else:
            self._logger.warn(
                'Handling an unknown listening socket. Ignoring.')
            return

        self._handleNewConnection(src_socket, src_host, src_port, target_port)

    def _handleNewConnection(
            self, src_socket, src_host, src_port, target_port):
        global _global_kill

        # Before proceeding, check if the global kill signal has been set
        if _global_kill.isSet():
            self._logger.info(
                'Received new connection request but received global kill so '
                'closing it')
            src_socket.close()
            return

        # Check where the new connection is coming from
        if src_host == self._host_a and target_port == self._port_a:
            src_name, dst_name = 'A', 'B'
            dst_host, dst_port = self._host_b, self._port_b
        elif src_host == self._host_b and target_port == self._port_b:
            src_name, dst_name = 'B', 'A'
            dst_host, dst_port = self._host_a, self._port_a
        else:
            self._logger.warning(
                'Message received from unknown host ({!s}:{!s} to port {!s}). '
                'Ignoring and closing new connection.'
                .format(src_host, src_port, target_port))
            src_socket.close()
            return

        self._logger.info(
            'Accepted connection is from host {:} ({!s}:{!s} to port {!s}), '
            'setting up forward connection to host {:} ({!s}:{!s})'
            .format(
                src_name, src_host, src_port, target_port,
                dst_name, dst_host, dst_port))

        # Create forwarding connection
        try:
            dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dst_socket.connect((dst_host, dst_port))
        except Exception as e:
            self._logger.error(
                'Caught exception while setting up forwarding connection to '
                '({:}, {:}): {:}'
                .format(dst_host, dst_port, e))
            self._logger.info(
                'Closing new connection from ({:}, {:})'
                .format(src_host, src_port))
            src_socket.close()
            return

        self._logger.info(
            'Connection to ({!s}, {!s}) successful'
            .format(dst_host, dst_port))

        # Create and start a new TCP relay from the new connection and
        # forwarding connection
        relay = TcpRelay(
            src_socket, src_host, src_port,
            dst_socket, dst_host, dst_port,
            self._max_message_size,
            self._timeout,
            self._message_middleware)
        relay.start()


def parsePortSpec(spec, separator='-'):
    '''
    Parses a port specification in two forms into the same form.

    In the first form the specification is just an integer. In this case a
    tuple is returned containing the same integer twice.

    In the second form the specification is two numbers separated by a hyphen
    ('-' by default, specifiable with :param separator:). The two numbers are
    parsed as integers and returned in the same order as a tuple of two
    integers.

    Example:

    .. code-block: python

       parsePortSpec('12345') # -> (12345, 12345)
       parsePortSpec('12345-56789') # -> (12345, 56789)
    '''
    x = list(map(lambda x: x.strip(), spec.split(separator)))
    return tuple(map(int, x * (3 - len(x))))


class Substitution():

    def __init__(self, spec):
        self.spec = spec
        self.delim = self.spec[0]
        components = re.split(r'(?<!\\)' + self.delim, self.spec)
        if len(components) < 4:
            raise ValueError('Substitution not completely defined')
        if len(components) > 4:
            raise ValueError('Substitution overly defined')
        self.pattern, self.substitution = components[1:3]
        if sys.version_info >= (3,):
            self.pattern = self.pattern.encode('utf-8')
            self.substitution = self.substitution.encode('utf-8')

    def apply(self, string):
        return re.sub(self.pattern, self.substitution, string)

    def __repr__(self):
        return '{:}({:})'.format(self.__class__.__name__, self.spec)

    def __str__(self):
        return '{delim}{pattern}{delim}{substitution}{delim}'.format(
            **self.__dict__)


def main():
    logger = logging.getLogger('relay')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser(
        description='Acts as a TCP and UDP relay from one interface to '
                    'another. This means any message received on this machine '
                    'on one of the ports specified from one of the hosts is '
                    'relayed to the other host across the same protocol and '
                    'same port (or other port if specified). Handy for, say, '
                    'tunneling some networking out of a VM to an external '
                    'network.')
    parser.add_argument(
        'host_a',
        help='Host name or IP address for interface A.')
    parser.add_argument(
        'host_b',
        help='Host name or IP address for interface B.')
    parser.add_argument(
        '--udp', '-u',
        dest='udp_port_specs',
        metavar='udp_port_spec',
        action='append',
        type=str,
        nargs='*',
        default=[],
        help='UDP port numbers to relay. If just an integer then the same '
             'port is used on each interface. If in the format "####-####" '
             '(or a regex of "[0-9]+-[0-9]+") then it is interpreted as a '
             'port remapping where the first integer (before the dash) is the '
             'port to listen and send to for host A and the second integer '
             '(after the dash) is the port to listen and send to for host B.')
    parser.add_argument(
        '--tcp', '-t',
        dest='tcp_port_specs',
        metavar='tcp_port_spec',
        action='append',
        type=str,
        nargs='*',
        default=[],
        help='TCP port numbers to relay. If just an integer then the same '
             'port is used on each interface. If in the format "####-####" '
             '(or a regex of "[0-9]+-[0-9]+") then it is interpreted as a '
             'port remapping where the first integer (before the dash) is the '
             'port to listen and send to for host A and the second integer '
             '(after the dash) is the port to listen and send to for host B.')
    parser.add_argument(
        '--max-message-size', '-m',
        dest='max_message_size',
        type=int,
        default=16384,
        help='Sets the max message size in bytes (default=16384)')
    parser.add_argument(
        '--tcp-connection-backlog', '-b',
        dest='backlog',
        type=int,
        default=5,
        help='Sets the backlog size for TCP connections (default=5)')
    parser.add_argument(
        '--substitute', '-s',
        dest='substitutions',
        metavar='substitution',
        action='append',
        type=Substitution,
        nargs='*',
        default=[],
        help='Specify regular expression substitutions in the form '
             '-s/pattern/replace/ where / can be replaced with another '
             'delimiter.')

    args = parser.parse_args()

    ip_a = socket.gethostbyname(args.host_a)
    logger.info(
        'Host name A "{:}" interpreted as IP "{:}"'.format(args.host_a, ip_a))
    ip_b = socket.gethostbyname(args.host_b)
    logger.info(
        'Host name B "{:}" interpreted as IP "{:}"'.format(args.host_b, ip_b))

    args.substitutions = \
        list(itertools.chain.from_iterable(args.substitutions))
    args.udp_port_specs = \
        list(itertools.chain.from_iterable(args.udp_port_specs))
    args.tcp_port_specs = \
        list(itertools.chain.from_iterable(args.tcp_port_specs))

    logger.info('Substitutions: {:}'.format(args.substitutions))

    middleman = None
    if len(args.substitutions) > 0:
        def middleman(
                msg,
                src_name, src_host, src_port,
                dst_name, dst_host, dst_port):
            for substitution in args.substitutions:
                msg = substitution.apply(msg)
            return msg

    relays = []

    for udp_port_spec in args.udp_port_specs:
        port_a, port_b = parsePortSpec(udp_port_spec)
        relay = UdpRelay(
            ip_a, port_a, ip_b, port_b,
            max_message_size=args.max_message_size,
            message_middleware=middleman)
        relays.append(relay)

    for tcp_port_spec in args.tcp_port_specs:
        port_a, port_b = parsePortSpec(tcp_port_spec)
        relay = TcpRelayServer(
            ip_a, port_a, ip_b, port_b,
            max_message_size=args.max_message_size,
            backlog=args.backlog,
            message_middleware=middleman)
        relays.append(relay)

    for relay in relays:
        relay.start()

    try:
        for relay in relays:
            while relay.is_alive():
                relay.join(timeout=10.0)
    except (KeyboardInterrupt, SystemExit):
        logger.info('Killing threads')
        _global_kill.set()


if __name__ == '__main__':
    main()
