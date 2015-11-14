import argparse
import logging
import os
import sys
import tempfile
from urlparse import urlparse

from zerotest.common import init_logging_config

__author__ = 'Hari Jiang'

DESCRIPTION = """
Capture HTTP request/response and replay it for the test purpose.
"""
init_logging_config()

LOG = logging.getLogger(__name__)


class CLI(object):
    def __init__(self):
        self._parser = None
        self._parse_result = None

    def _init_arg_parser(self):
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

        server_parser = subparsers.add_parser('server', help='start zerotest local proxy server')
        server_parser.add_argument('url', help="target url: http://example.com")
        server_parser.add_argument('-f', '--file', help="file path to store record, default: [random path]")
        server_parser.add_argument('-b', '--bind', help="local bind address, default: 127.0.0.1")
        server_parser.add_argument('-p', '--port', help="local port, default: 7000")

        replay_parser = subparsers.add_parser('replay', help='replay from record data')
        replay_parser.add_argument('file', help="path of record data file")
        replay_parser.add_argument('--endpoint', help="replace requests endpoint, https://example.com")
        replay_parser.add_argument('--ignore-headers', help="pass a list of ignored headers in response match",
                                   nargs='*')
        replay_parser.add_argument('--verify-ssl', help="enable ssl verify", dest="verify_ssl", action="store_true")
        replay_parser.add_argument('--no-verify-ssl', help="disable ssl verify", dest="verify_ssl",
                                   action="store_false")
        replay_parser.set_defaults(verify_ssl=False)

        generate_parser = subparsers.add_parser('generate', help='generate test code from record data')
        generate_parser.add_argument('file', help="path of record data file")
        generate_parser.add_argument('--endpoint', help="replace requests endpoint, https://example.com")
        generate_parser.add_argument('--ignore-headers', help="pass a list of ignored headers",
                                     nargs='*')
        generate_parser.add_argument('--verify-ssl', help="enable ssl verify", dest="verify_ssl", action="store_true")
        generate_parser.add_argument('--no-verify-ssl', help="disable ssl verify", dest="verify_ssl",
                                     action="store_false")

        self._parser = parser

    def run(self, argv=sys.argv[1:]):
        self._init_arg_parser()
        self._parse_result = self._parser.parse_args(argv)
        return getattr(self, 'command_{}'.format(self._parse_result.subparser_name))()

    def get_cli_options(self, *keys):
        options = {k: getattr(self._parse_result, k) for k in keys if
                   getattr(self._parse_result, k, None)}
        return options

    def command_server(self):
        """
        sub-command start
        :return:
        """
        from zerotest.app import App

        forward_url = self._parse_result.url
        parsed_url = urlparse(forward_url)
        forward_host = parsed_url.hostname
        if not forward_host:
            LOG.error("invalid url '{}'".format(forward_url))
            return 1

        filepath = self._parse_result.file

        if not filepath:
            _, filepath = tempfile.mkstemp()
        else:
            if os.path.exists(filepath):
                LOG.warning("file '{}' is exists, new record will append to the file".format(filepath))

        app = App(forward_url, filepath)
        host = self._parse_result.bind or '127.0.0.1'
        port = int(self._parse_result.port or 7000)
        app.run(host, port)

    def command_replay(self):
        """
        sub-command replay
        run record file
        :return:
        """
        from zerotest.record.record_test_runner import RecordTestRunner

        filepath = self._parse_result.file
        if not os.path.exists(filepath):
            LOG.warning("file '{}' not exists".format(filepath))

        endpoint = self._parse_result.endpoint
        ignore_headers = self._parse_result.ignore_headers or []
        verify_ssl = self._parse_result.verify_ssl

        _, failed = RecordTestRunner(filepath, endpoint=endpoint, ignore_headers=ignore_headers,
                                     verify_ssl=verify_ssl).run()

        # exit with code 1 if any case failed
        if failed > 0:
            return 1

    def command_generate(self):
        """
        sub-command generate
        :return:
        """
        from zerotest.generator.generator import Generator
        filepath = self._parse_result.file
        options = self.get_cli_options('endpoint', 'verify_ssl')
        match_options = self.get_cli_options('ignore_headers')
        generator = Generator(filepath, options=options, match_options=match_options)
        print(generator.generate())


def main():
    code = CLI().run() or 0
    exit(code)


if __name__ == '__main__':
    main()
