__author__ = 'Hari Jiang'

import argparse
import sys
from urlparse import urlparse
import os
import logging
import tempfile

from zerotest.common import init_logging_config

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

        run_parser = subparsers.add_parser('replay', help='replay record file test')
        run_parser.add_argument('file', help="zerotest record file")
        run_parser.add_argument('--endpoint', help="replace requests endpoint, https://example.com")
        run_parser.add_argument('--ignore-headers', help="pass a list of ignored headers in response match", nargs='*')
        run_parser.add_argument('--verify-ssl', help="enable ssl verify", dest="verify_ssl", action="store_true")
        run_parser.add_argument('--no-verify-ssl', help="disable ssl verify", dest="verify_ssl",
                                action="store_false")
        run_parser.set_defaults(verify_ssl=False)

        self._parser = parser

    def run(self, argv=sys.argv[1:]):
        self._init_arg_parser()
        self._parse_result = self._parser.parse_args(argv)
        getattr(self, 'command_{}'.format(self._parse_result.subparser_name))()

    def exit_with_error_message(self, message):
        LOG.error(message)
        exit(1)

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
            self.exit_with_error_message("invalid url '{}'".format(forward_url))

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
            exit(1)


def main():
    CLI().run()


if __name__ == '__main__':
    main()
