#!/usr/bin/python
import json
import re
import socket
from string import Template
import sys
from datetime import datetime, timedelta, tzinfo
from urlparse import urlparse

from tornado import ioloop
from tornado import gen
from tornado.iostream import PipeIOStream
from tornado.tcpclient import TCPClient

import fnmatch2


SYSLOG_PROTOCOL_PORT = 514

ONCE_CONNECT_TIMEOUT = 0.5
RECONNECT_INTERVAL = 1

ZERO_TD = timedelta(0)


class LoggerValueTemplate(Template):
    idpattern = '\w+'


class LoggerBaseData(object):
    _yaml_schema = {
        'type': 'array',
        'items': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'pattern': {
                    'type': 'string'
                }
            },
            'patternProperties': {
                '^[\w-]+$': {
                    'type': 'string'
                }
            },
        }
    }

    def __init__(self, base_dict=None):
        self.base_dict = base_dict or {}
        self._data_cache = {}
        self._patterns = []

    def add_yaml_config(self, filename):
        import yaml
        from jsonschema import validate

        with open(filename) as f:
            result = yaml.safe_load(f)
        validate(result, self._yaml_schema)
        for row in result:
            self._patterns.append({
                'regex': re.compile(fnmatch2.translate(row.pop('pattern'))),
                'values': {k: LoggerValueTemplate(v) for k, v in row.items()}
            })

    def get_data_for_filename(self, filename):
        filename = filename or ''
        if filename not in self._data_cache:
            data = self._data_cache[filename] = dict(self.base_dict)
            for pattern in self._patterns:
                match = pattern['regex'].search(filename)
                if match:
                    replace_dict = {str(i): match.group(i) for i in range(pattern['regex'].groups + 1)}
                    data.update({k: v.substitute(replace_dict) for k, v in pattern['values'].items()})

        return self._data_cache[filename]


class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO_TD

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO_TD


utc = UTC()

FACILITY = {
    'kern': 0, 'user': 1, 'mail': 2, 'daemon': 3,
    'auth': 4, 'syslog': 5, 'lpr': 6, 'news': 7,
    'uucp': 8, 'cron': 9, 'authpriv': 10, 'ftp': 11,
    'local0': 16, 'local1': 17, 'local2': 18, 'local3': 19,
    'local4': 20, 'local5': 21, 'local6': 22, 'local7': 23,
}
REVERSE_FACILITY = {v: k for k, v in FACILITY.items()}

SEVERITY = {
    'emerg': 0, 'alert': 1, 'crit': 2, 'err': 3,
    'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}
REVERSE_SEVERITY = {v: k for k, v in SEVERITY.items()}


class UDPStream:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def write(self, data):
        self.sock.sendto(data, (self.host, self.port))


# noinspection PyBroadException
class SafeTcpStream:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stream = None
        self.tcp_client = TCPClient()
        self.make_tcp_connection_loop()

    @gen.coroutine
    def make_tcp_connection_loop(self, once=False):
        while True:
            if self.stream is None:
                try:
                    if once:
                        self.stream = yield gen.with_timeout(
                            ioloop.IOLoop.instance().time() + ONCE_CONNECT_TIMEOUT,
                            self.tcp_client.connect(self.host, self.port))
                    else:
                        self.stream = yield self.tcp_client.connect(self.host, self.port)

                    if self.stream is not None:
                        self.stream.set_close_callback(self.disconnected)
                except Exception:
                    pass
            if once:
                break
            yield gen.Task(ioloop.IOLoop.instance().add_timeout, ioloop.IOLoop.instance().time() + RECONNECT_INTERVAL)

    def disconnected(self):
        try:
            self.stream.close()
        except Exception:
            pass
        self.stream = None

    def write(self, data):
        if self.stream is not None:
            return self.stream.write(data)


class TcpUdpStream(SafeTcpStream, UDPStream):
    def __init__(self, host, port):
        UDPStream.__init__(self, host, port)
        SafeTcpStream.__init__(self, host, port)

    def write(self, data):
        (UDPStream if len(data) <= 1472 else SafeTcpStream).write(self, data)


# noinspection PyBroadException
class Logger:
    def __init__(self, transport_uri, logger_data=None):
        """
        :type logger_data: LoggerBaseData
        """
        uri = urlparse(transport_uri)
        if '+' in uri.scheme:
            self.transport, self.out_format = uri.scheme.split('+', 1)
        else:
            self.transport, self.out_format = uri.scheme, 'json'
        self.host, self.port = uri.hostname, uri.port

        self.output_stream = None
        self.input_stream = None
        self.current_filename = None  # used with `tail -f` with multiple files
        self.logger_data = logger_data

        if self.out_format == 'syslog':
            self.encode_data = lambda x, o: (b'<%d>%s %s %s: %s\x00' % (
                (x['facility'] << 3) | x['severity'],
                o['timestamp'].strftime("%b %d %H:%M:%S"),
                x.get('logsource', ''), x.get('program', ''), x['message']))
        elif self.out_format == 'json':
            self.encode_data = lambda x, o: json.dumps(x, separators=(',', ':')).encode('utf-8') + "\n"
        elif self.out_format == 'msgpack':
            import umsgpack
            self.encode_data = lambda x, o: umsgpack.packb(x)
        else:
            raise ValueError('Unknown output format {}'.format(self.out_format))

        if self.transport == 'stdout':
            pass
        elif self.transport in ['tcp', 'udp', 'tup']:
            if not self.port and self.out_format == 'syslog':
                self.port = SYSLOG_PROTOCOL_PORT
            if not self.host:
                self.host = 'localhost'
            if not self.port:
                raise ValueError('Port not specified')
        else:
            raise ValueError('Unknown transport {}'.format(self.transport))

    @gen.coroutine
    def rw_loop(self):
        while True:
            try:
                line = yield self.input_stream.read_until("\n")
            except Exception:
                ioloop.IOLoop.instance().stop()
                break

            if not line:
                continue

            message = line.strip("\r\n")
            if not message:
                continue

            if message.startswith("==> ") and message.endswith(" <=="):  # tail, ==> service-access.log <==
                self.current_filename = message[4:-4]
                continue

            assert self.output_stream is not None, 'Not started yet'
            utcnow = datetime.utcnow().replace(tzinfo=utc)
            data_dict = dict(self.logger_data.get_data_for_filename(self.current_filename))
            data_dict['message'] = message
            data_dict['timestamp'] = utcnow.isoformat()
            orig_data_dict = {'timestamp': utcnow}

            data_to_send = self.encode_data(data_dict, orig_data_dict)

            try:
                yield self.output_stream.write(data_to_send)
            except Exception:
                pass

    @gen.coroutine
    def start(self):
        if self.transport == 'tcp':
            self.output_stream = SafeTcpStream(self.host, self.port)
            # make first attempt synchronously once
            yield self.output_stream.make_tcp_connection_loop(once=True)
        elif self.transport == 'stdout':
            self.output_stream = PipeIOStream(sys.stdout.fileno())
        elif self.transport == 'tup':
            self.output_stream = TcpUdpStream(self.host, self.port)
        else:  # udp
            self.output_stream = UDPStream(host=self.host, port=self.port)

        self.input_stream = PipeIOStream(sys.stdin.fileno())

        # run concurrently asynchronous
        self.rw_loop()


description = '''
transport format:
 [stdout|tcp|udp|tup]+[msgpack|json|syslog]://[host][:port]
      (ip/port is ignored in stdout transport)
      default host is `localhost`
      port is required (except for syslog)
'''


def main(args=None):
    import argparse

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--facility', help='Log Facility', default=None)
    parser.add_argument('-s', '--severity', help='Log Level/Severity', default=None)
    parser.add_argument('-e', '--field', help='Custom Field (\"name:value\")', action='append')
    parser.add_argument('-c', '--config', help='Path to yaml config file', action='append')
    parser.add_argument('-t', '--transport', help='Transport URI (see examples)', action='store', default='stdout://')
    args = vars(parser.parse_args(args))

    base_dict = dict()
    base_dict['facility'] = FACILITY.get(args['facility'], 1)  # default is `user`
    base_dict['facility_label'] = REVERSE_FACILITY[base_dict['facility']]
    base_dict['severity'] = SEVERITY.get(args['severity'], 6)  # default is `info`
    base_dict['severity_label'] = REVERSE_SEVERITY[base_dict['severity']]

    for field in args['field'] or ():
        field_name, field_val = field.split(":", 1)
        base_dict[field_name] = field_val

    logger_data = LoggerBaseData(base_dict)
    for field in args['config'] or ():
        logger_data.add_yaml_config(field)

    logger = Logger(transport_uri=args['transport'], logger_data=logger_data)

    loop = ioloop.IOLoop.instance()
    loop.add_callback(logger.start)
    try:
        loop.start()
    except KeyboardInterrupt:
        loop.stop()


if __name__ == "__main__":
    main()
