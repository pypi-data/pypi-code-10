#!/usr/bin/env python
from .command import Command
import platform


class Hello(Command):

    def _add_arguments(self, parser):
        parser.add_argument(
            '-m', '--message',
            type=str,
            dest='message',
            required=True,
            help='Message')

    def _execute(self):
        self._logger.info('Hello')
        self._logger.info(self.args.message)
        self._logger.info(platform.python_version())
