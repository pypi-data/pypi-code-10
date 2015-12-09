#!/usr/bin/env python
import argparse
import collections
import logging
import os
import os.path
try:
    from Queue import Queue, Full  # Python 2
except ImportError:
    from queue import Queue, Full  # Python 3
import re
import socket
import sys
import time
import traceback
from threading import Event, Thread


_global_kill = Event()


def globalKill():
    '''
    Triggers the global kill signal which is used to terminate the message
    loader thread.
    '''
    global _global_kill
    _global_kill.set()


class MessageLoader(Thread):

    @property
    def messages(self):
        return self._messages

    @property
    def message_count(self):
        return self._message_count

    @property
    def index(self):
        return self._index

    @property
    def queue(self):
        return self._queue

    @property
    def queue_size(self):
        return self._queue.maxsize

    def __init__(
            self,
            messages,
            queue_size):
        global _global_kill

        super(MessageLoader, self).__init__()

        self._logger = logging.getLogger('nut.replay.MessageLoader')

        self._messages = messages

        self._message_count = len(self._messages)
        self._index = 0
        self._queue = Queue(maxsize=queue_size)

    def run(self):
        global _global_kill

        while self._index < self._message_count:
            message_filename = self._messages[self._index].filename

            # Read the message contents into memory
            with open(message_filename, 'rb') as f:
                message = f.read()
            self._logger.debug(
                'Read message {:}, waiting to be put into queue'
                .format(message_filename))

            # Then repeatedly try to put the contents into the queue,
            # occasionally timing out so that we might catch the kill signal
            put_succeeded = False
            while not put_succeeded:
                if _global_kill.isSet():
                    return
                try:
                    self._queue.put(message, block=True, timeout=1.0)
                except Full:
                    pass
                else:
                    put_succeeded = True
                    self._logger.debug('Message put into queue')

            self._index += 1


class SocketWrapper():

    @property
    def protocol(self):
        return self._protocol

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def timeout(self):
        return self._timeout

    @property
    def socket(self):
        return self._socket

    def __init__(self, protocol, host, port, timeout=10):
        self._logger = logging.getLogger(
            'nut.replay.SocketWrapper({:}, {:}, {:})'
            .format(protocol, host, port))

        # Remember parameters
        self._protocol = protocol
        self._host = host
        self._port = port
        self._timeout = timeout

        # Create socket according to protocl
        if self._protocol == 'tcp':
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._logger.info('Successfully created TCP socket')
        elif self._protocol == 'udp':
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._logger.info('Successfully created UDP socket')
        else:
            raise ValueError(
                'Unknown endpoint protocol "{:}", skipping.'
                .format(self._protocol))

        # Set timeout (only really applies to TCP)
        self._socket.settimeout(self._timeout)
        self._logger.info(
            'Successfully set socket timeout to {:}'
            .format(self._timeout))

        # Set address reusability
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._logger.info('Successfully set socket option to SO_REUSEADDR')

        # Connect to destination (unnecessary for UDP but allows us to use same
        # send() API for both UDP and TCP sockets)
        self._socket.connect((self._host, self._port))
        self._logger.info(
            'Successfully connected socket to {:}:{:}...'
            .format(self._host, self._port))

    def __del__(self):
        self._logger.info('Closing socket')
        self._socket.close()

    def __repr__(self):
        return '{:}({:}, {:}, {:})'.format(
            self.__class__.__name__, self._protocol, self._host, self._port)

    def send(self, message):
        self._socket.send(message)


Message = collections.namedtuple('Message', ['time', 'filename', 'socket'])


def main():
    parser = argparse.ArgumentParser(**{
        'description':
            'Replays message dumps made by nutrelay.'})

    parser.add_argument('--host-a', '-a', **{
        'dest': 'host_a',
        'type': str,
        'default': None,
        'help':
            'Host name or IP address for interface A. If not specified then '
            'messages meant for host A are not replayed.'})

    parser.add_argument('--host-b', '-b', **{
        'dest': 'host_b',
        'type': str,
        'default': None,
        'help':
            'Host name or IP address for interface B. If not specified then '
            'messages meant for host B are not replayed.'})

    parser.add_argument('endpoints', **{
        'metavar': 'endpoint',
        'type': str,
        'nargs': '*',
        'default': [],
        'help':
            'Zero or more endpoint specifications. An endpoint specification '
            'is conveniently the same thing as the path to a specific '
            'endpoint dump when in a dump folder. The format is "{a|b}/{udp|'
            'tcp}{port}". Examples are "b/udp3251" and "a/tcp9001". Since the '
            'path to the endpoint dump is valid too a trailing slash is '
            'allowed. If no specifications are provided then all endpoints in '
            'the current working directory are used. If any specifications '
            'are provided then only those are used.'})

    parser.add_argument('--timeout', '-t', **{
        'dest': 'timeout',
        'type': float,
        'default': 10.0,
        'help':
            'Sets the socket timeout for TCP connections. Default is 10.0.'})

    parser.add_argument('--time-factor', '-f', **{
        'dest': 'time_factor',
        'type': float,
        'default': 1.0,
        'help':
            'Sets the time factor applied to delays between messages. If 0.0 '
            'then playback occurs as fast as possible. If 0.5 then playback '
            'occurs at twice as fast. If 1.0 then playback is in real time. '
            'If 2.0 then playback occurs at half speed. Default is 1.0.'})

    # TODO (vietjtnguyen): Add the ability to remap an endpoint dump to another
    # protocol and port. Perhaps use format like "-r b/udp3251 b/tcp8888".

    parser.add_argument('--logging-level', **{
        'dest': 'logging_level',
        'type': str,
        'default': 'DEBUG',
        'choices': ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
        'help':
            'Sets the logging level. Must be CRITICAL, ERROR, WARNING, INFO, '
            'DEBUG, or NOTSET. Default is DEBUG.'})

    args = parser.parse_args()

    # Set up logging
    logger = logging.getLogger('nut.replay')
    logging_level = getattr(logging, args.logging_level)
    logger.setLevel(logging_level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # If no hosts are specified then we can't replay anything
    if args.host_a is None and args.host_b is None:
        logger.error('No hosts specified.')
        return -1

    # Resolve hostnames if necessary
    ip_a, ip_b = None, None
    if args.host_a is not None:
        ip_a = socket.gethostbyname(args.host_a)
        logger.info(
            'Host name A "{:}" interpreted as IP "{:}"'
            .format(args.host_a, ip_a))
    if args.host_b is not None:
        ip_b = socket.gethostbyname(args.host_b)
        logger.info(
            'Host name B "{:}" interpreted as IP "{:}"'
            .format(args.host_b, ip_b))

    # Gather all endpoints
    local_endpoint_regex = re.compile('^(tcp|udp)\d{1,5}$')
    endpoints = []
    if len(args.endpoints) == 0:
        logger.info('No endpoints specified, searching for endpoints')
        for host in 'abAB':
            if not os.path.exists(host):
                logger.warning(
                    'Could not find folder for host "{:}"'
                    .format(host))
                continue
            valid_endpoints = [
                os.path.join(host, x)
                for x
                in os.listdir(host)
                if local_endpoint_regex.match(x) is not None]
            logger.info(
                'Found following valid endpoints for host "{:}": {:}'
                .format(host, valid_endpoints))
            endpoints.extend(valid_endpoints)
    else:
        endpoints.extend(args.endpoints)

    # Initialize list of all things
    all_messages = []

    # Process each endpoint
    endpoint_regex = re.compile(
        '^' + os.path.join('(a|b)', '(tcp|udp)(\d{1,5})', '?') + '$')
    for endpoint in endpoints:
        logger.info('Processing endpoint "{:}"'.format(endpoint))

        # Check if the formatting of the endpoint
        match = endpoint_regex.match(endpoint)
        if match is None:
            logger.error(
                'Endpoint "{:}" is not valid, skipping.'
                .format(endpoint))
            continue

        # Parse endpoint information
        host_letter, protocol, port = match.groups()
        logger.debug('host_letter={:}'.format(host_letter))
        logger.debug('protocol={:}'.format(protocol))
        logger.debug('port={:}'.format(port))

        # Determine host
        if host_letter.lower() == 'a':
            if args.host_a is None:
                logger.warning(
                    'Endpoint host is A but no host A defined for replay, '
                    'skipping.')
                continue
            else:
                host = args.host_a
        elif host_letter.lower() == 'b':
            if args.host_b is None:
                logger.warning(
                    'Endpoint host is B but no host B defined for replay, '
                    'skipping.')
                continue
            else:
                host = args.host_b
        else:
            logger.error(
                'Unknown host letter: {:} (expected a/A or b/B), skipping.'
                .format(host_letter))
            continue

        # Parse port
        try:
            port = int(port)
        except ValueError:
            logger.error(
                'Invalid port number: {:}, skipping.'
                .format(port))
            traceback.print_exc()
            continue

        # Create socket for this endpoint
        try:
            sock = SocketWrapper(protocol, host, port, args.timeout)
        except:
            logger.error(
                'Caught exception while creating SocketWrapper, skipping')
            traceback.print_exc()
            continue
        else:
            logger.info('Successfully created {:}'.format(sock))

        # Load the timestamps
        timestamps_filename = os.path.join(endpoint, 'timestamps.txt')
        try:
            with open(timestamps_filename, 'r') as f:
                timestamps = list(map(float, f.readlines()))
        except Exception:
            logger.error(
                'Caught exception while trying to read timestamps file "{:}", '
                'skipping.'
                .format(timestamps_filename))
            traceback.print_exc()
            continue

        # Collect messages into tuple that remembers the message time, file,
        # and outgoing socket
        messages = [
            Message(
                message_time,
                os.path.join(endpoint, '{:09d}'.format(index)),
                sock)
            for index, message_time
            in enumerate(timestamps)]

        # Add the messages to our list of all messages
        all_messages.extend(messages)

    # Sort messages by timestamp
    all_messages.sort(key=lambda x: x.time)

    # Start message loader
    message_loader = MessageLoader(all_messages, queue_size=10)
    message_loader.start()

    # Wait for the message loader to have a message so that the delays don't
    # incidentally include a message loading delay
    logger.info('Waiting for message loader to load first message...')
    while message_loader.queue.empty():
        pass

    # Start message sending loop
    try:
        last_time = 0.0
        for index, message in enumerate(all_messages):

            # Delay the time delta unless it's zero
            delay = (message.time - last_time) * args.time_factor
            if delay > 0.0:
                time.sleep(delay)

            # Get the message contents from the message loader
            message_contents = \
                message_loader.queue.get(block=True, timeout=None)

            # Send the message contents
            try:
                message.socket.send(message_contents)
            except Exception as e:
                logger.error(
                    'Caught exception while sending message: {:} (index={:})'
                    .format(message, index))
                traceback.print_exc()
                raise(e)
            else:
                logger.info(
                    'Message sent: {:} (index={:})'
                    .format(message, index))

            # Remember last time to calculate next time delta
            last_time = message.time

    # Catch any overarching exceptions such as KeyboardInterrupt and SystemExit
    except:
        logger.info('Caught exception while sending messages')
        traceback.print_exc()
        logger.info('Killing message loading thread')

        # Kill the message loader
        globalKill()
        message_loader.join()

    # Delete everything that can hold references to the socket wrappers so
    # that the socket wrappers close the sockets
    del message_loader
    del all_messages
    del sock

    logger.info('Replay done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
