from __future__ import unicode_literals

import argparse
import logging
import os
import sys
import tempfile

from zerotest.common import init_logging_config
from zerotest.utils.url_helper import urlparse

DESCRIPTION = """
Capture HTTP request/response and convert to test code.
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
        server_parser.add_argument('url', help="target url, example: http://example.com")
        server_parser.add_argument('-f', '--file', help="file path to save record data, default: [random path]")
        server_parser.add_argument('-b', '--bind', help="local bind address, default: 127.0.0.1")
        server_parser.add_argument('-p', '--port', help="local port, default: 7000")

        generate_parser = subparsers.add_parser('generate', help='generate test code from record data')
        self._add_match_options_to_parser(generate_parser)

        replay_parser = subparsers.add_parser('replay', help='replay test from record data')
        self._add_match_options_to_parser(replay_parser)
        replay_parser.add_argument('-t', '--pytest', help="pass options to pytest, example: -t='-vv'", nargs='*')

        self._parser = parser

    @staticmethod
    def _add_match_options_to_parser(parser):
        parser.add_argument('file', help="path of record data file")
        parser.add_argument('--endpoint', help="replace requests endpoint, https://example.com")
        parser.add_argument('--ignore-headers', help="list of headers ignore in response matching",
                            nargs='*')
        parser.add_argument('--ignore-all-headers', help="skip headers match", dest="ignore_all_headers",
                            action='store_true'),
        parser.add_argument('--fuzzy-match',
                            help="enable fuzzy match, check the schema of response data instead of fully match",
                            action='store_true')
        parser.add_argument('--allow-blank', help="allow blank fields, only work on fuzzy match", action='store_true')
        parser.add_argument('--allow-none', help="allow none(null) fields, only work on fuzzy match", action='store_true')
        parser.add_argument('--ignore-fields',
                            help="list of fields ignore in response matching,"
                                 " only work on serializable content-type,"
                                 " example: --ignore-fields a b c.d(explained as d under c)",
                            nargs='*')
        parser.add_argument('--verify-ssl', help="enable ssl verify", dest="verify_ssl", action="store_true")
        parser.add_argument('--no-verify-ssl', help="disable ssl verify", dest="verify_ssl",
                            action="store_false")
        parser.set_defaults(verify_ssl=False)
        parser.set_defaults(ignore_all_headers=False)

    def run(self, argv=sys.argv[1:]):
        """
        run cli
        :param argv:
        :return: cli exit code
        """
        self._init_arg_parser()
        self._parse_result = self._parser.parse_args(argv)
        if not self.verify_parse_result():
            return 1
        return getattr(self, 'command_{}'.format(self._parse_result.subparser_name))()

    def verify_parse_result(self):
        cli_options = self.get_cli_options('endpoint', 'url')
        endpoint = cli_options.get('endpoint')
        if endpoint:
            parsed_url = urlparse(endpoint)
            if not parsed_url.hostname or not parsed_url.scheme:
                LOG.error("invalid endpoint '{}'".format(endpoint))
                return False

        url = cli_options.get('url')
        if url:
            parsed_url = urlparse(url)
            if not parsed_url.hostname:
                LOG.error("invalid url '{}'".format(url))
                return False

        return True

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
        import tempfile
        import pytest

        generator = self._generator_from_command()
        pytest_args = self._parse_result.pytest or []
        with tempfile.NamedTemporaryFile('w+', suffix='.py') as f:
            f.write(generator.generate())
            f.flush()
            return pytest.main([f.name] + pytest_args)

    def _generator_from_command(self):
        from zerotest.generator.generator import Generator
        filepath = self._parse_result.file
        options = self.get_cli_options('endpoint', 'verify_ssl')
        match_options = self.get_cli_options(
            'ignore_headers',
            'ignore_fields',
            'ignore_all_headers',
            'fuzzy_match',
            'allow_blank',
            'allow_none',
        )
        generator = Generator(filepath, options=options, match_options=match_options)
        return generator

    def command_generate(self):
        """
        sub-command generate
        :return:
        """
        generator = self._generator_from_command()
        print(generator.generate())


def main():
    code = CLI().run() or 0
    exit(code)


if __name__ == '__main__':
    main()
