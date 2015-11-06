import sys
import os
import argparse
from .info import InfoCommand
from .gen import GenCommand
from .send import SendCommand
from ..formatters import formatter_factory


EXIT_CODE_BAD_ARG = 1
EXIT_CODE_GENERAL_ERR = 2


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


class Cmd(object):

    def __init__(self):
        self.argparser = None

    def run(self):
        self.build_argparser()
        self.build_commands()
        self.run_argparser()

    def build_argparser(self):

        # Entry parser
        self.argparser = ThrowingArgumentParser()
        self.argparser.add_argument(
            '--load-providers', '-l', default=None, dest='providers',
            help='an optional file path or importable module name that may be'
                 ' included and added to the list of default providers.')
        self.argparser.add_argument(
            '--patterns', '-p', default=None, dest='patterns',
            help='optional file containing pattern strings separated by new'
                 ' lines when .txt, or a json array of patterns when .json')
        self.argparser.add_argument(
            '--format', '-f', default='txt', dest='format',
            help='format for output data, one of txt, json or csv default: txt')
        self.argparser.add_argument(
            '--debug', '-d', default=False, action='store_true', dest='debug',
            help='debug flag for additional troubleshooting information')
        self.argparser.add_argument(
            '--number', default=1, dest='number', type=int,
            help='number of times to generate pattern, default: 1')
        self.argparser.add_argument(
            '--persistent', default=True, dest='persistent', action='store_true',
            help='when sending multiple message keep the connection open. note when using'
                 ' this option you should terminate your pattern if needed. default: true')
        gen_parser_group = self.argparser.add_mutually_exclusive_group()
        gen_parser_group.add_argument(
            '--noseed', default=False, dest='noseed', action='store_true',
            help='do not seed the pseudo-random number generator to produce non-deterministic data')
        gen_parser_group.add_argument(
            '--seed', default=1, dest='seed', type=int,
            help='seed the pseudo-random number generator, default: 1')

    def build_commands(self):

        # Sub parser for commands
        sub_parsers = self.argparser.add_subparsers(title='commands')

        # Info command
        info_parser = sub_parsers.add_parser(
            'info',
            description='dump information to stdout and exit')
        info_parser.set_defaults(func=self.command_info)
        info_parser.add_argument('commands', nargs='*')

        # Gen command
        gen_parser = sub_parsers.add_parser(
            'gen',
            description='generate data',
            help='ex: gensend gen pattern1 ... patternN')
        gen_parser.set_defaults(func=self.command_gen)
        gen_parser.add_argument('commands', nargs='*')

        # Send command
        send_parser = sub_parsers.add_parser(
            'send',
            description='send data',
            help='ex: gensend send pattern1 ... patternN scheme://netloc/path;parameters?query#fragment')
        send_parser.set_defaults(func=self.command_send)
        send_parser.add_argument('commands', nargs='*')

    def run_argparser(self):
        ns = None

        try:
            ns = self.argparser.parse_args()
            self.command(ns)
        except ArgumentParserError, e:
            self.oops(str(e))
        return ns

    def oops(self, message):
        print '\nOops: ' + message
        print 'Maybe you could try: gensend -h'
        print "\n----\n"
        self.argparser.print_help()
        self.error('', EXIT_CODE_GENERAL_ERR)

    def error(self, msg, code):
        sys.stderr.write(msg + "\n")
        sys.stderr.flush()
        os._exit(code)

    def command(self, ns):
        ns.formatter = formatter_factory(sys.stdout, ns.format)
        ns.func(ns)

    def command_info(self, ns):
        """ Command: gensend info"""
        infocmd = InfoCommand()
        infocmd(ns)

    def command_gen(self, ns):
        """ Command: gensend gen"""
        gencmd = GenCommand()
        gencmd(ns)

    def command_send(self, ns):
        """ Command: gensend send"""
        sendcmd = SendCommand()
        sendcmd(ns)
