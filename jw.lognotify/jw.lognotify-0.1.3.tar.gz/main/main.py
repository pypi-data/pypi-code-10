#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Main Program
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import dict, open
from collections import deque
from functools import reduce
from operator import or_

from future import standard_library
from past.builtins import basestring

standard_library.install_aliases()
from functools import partial
import io
import logging
import re
from subprocess import call
import sys
from os import fstat, stat
import time
from tkinter import Tcl

import yaml

from gevent import sleep, spawn
from gevent.hub import LoopExit
from gevent.queue import Queue
from pkg_resources import get_distribution

__version__ = get_distribution('jw.lognotify').version
Logger = logging.getLogger(__name__)

VERSION = ("""
lognotify version %s
Copyright (c) 2015 Johnny Wezel
License: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software. You are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
""" % __version__).strip()
LOG_POLL_MIN_SLEEP = 0.05
LOG_POLL_MAX_SLEEP = 0.5
LOG_POLL_SLEEP_STEP = 0.001
LOGGING_LEVELS = (
    sorted(l for l in logging._levelNames if isinstance(l, int)) if sys.version_info[:2] < (3, 4)
    else sorted(logging._levelToName.keys())
)
INITIAL_LOGGING_LEVEL = logging.ERROR
DEFAULT_DO = [
    'python',
    "print('%s: %s' % (logfile, message))"
]

# Mapping of regex specifier suffix to flags in re module
REGEX_FLAGS = {
    "l": re.LOCALE,
    "i": re.IGNORECASE,
    "m": re.MULTILINE,
    "s": re.DOTALL,
    "u": re.UNICODE,
    "x": re.VERBOSE,
}

class RunPython(object):
    """
    Python code
    """

    def __init__(self, block):
        """
        Create a RunPython object
        """
        self.code = compile(block, '<filter-code>', 'exec')

    def run(self, context):
        """
        Run Python code

        :param context: variables available in the code
        :type context: dict
        """
        exec(self.code, context)

class RunBash(object):
    """
    Bash code
    """

    def __init__(self, block):
        """
        Create a RunBash object
        """
        self.block = block

    def run(self, context):
        """
        Run bash code

        :param context: variables available in the code
        :type context: dict
        """
        call(
            [
                '/bin/bash',
                '-c',
                ''.join("%s='%s'\n" % (var, value) for var, value in context.items()) + self.block
            ],
            stderr=sys.stderr,
            stdout=sys.stdout,
        )

class RunSh(object):
    """
    Sh code
    """

    def __init__(self, block):
        """
        Create a RunSh object
        """
        self.block = block

    def run(self, context):
        """
        Run sh code

        :param context: variables available in the code
        :type context: dict
        """
        call(
            [
                '/bin/sh',
                '-c',
                ''.join("%s='%s'\n" % (var, value) for var, value in context.items()) + self.block
            ],
            stderr=sys.stderr,
            stdout=sys.stdout,
        )

class RunTcl(object):
    """
    Sh code
    """

    def __init__(self, block):
        """
        Create a RunSh object
        """
        self.block = block
        self.tcl = Tcl()

    def run(self, context):
        """
        Run Tcl code

        :param context: variables available in the code
        :type context: dict
        """
        self.tcl.eval(''.join('set %s "%s"\n' % (var, value) for var, value in context.items()) + self.block)

LANGUAGE_HANDLERS = {
    'python': RunPython,
    'bash': RunBash,
    'sh': RunSh,
    'tcl': RunTcl,
}

def QuotedIn(crit):
    """
    Return predicate for quoted string appearing in line

    :param crit: Search text
    :type crit: str
    :return: predicate for a quoted string
    :rtype: function
    """
    def quotedIn(crit, text):
        result = crit in text
        Logger.debug('"%s" in "%s" -> %s', crit, text, result)
        return result
    return partial(quotedIn, crit[0])

def QuotedNotIn(crit):
    """
    Return predicate for quoted string not appearing in line

    :param crit: Search text
    :type crit: str
    :return: predicate for a quoted string
    :rtype: function
    """
    def quotedNotIn(crit, text):
        result = crit not in text
        Logger.debug('"%s" not in "%s" -> %s', crit, text, result)
        return result
    return partial(quotedNotIn, crit[0])

def UnquotedIn(crit):
    """
    Return predicate for unquoted string appearing in line

    :param crit: Search text
    :type crit: str
    :return: predicate for a quoted string
    :rtype: function
    """
    def unquotedIn(crit, text):
        result = bool(crit.search(text))
        Logger.debug('`%s` in "%s" -> %s', crit.pattern, text, result)
        return result
    return partial(unquotedIn, re.compile(r'\b%s\b' % crit[0], re.IGNORECASE))

def UnquotedNotIn(crit):
    """
    Return predicate for unquoted string not appearing in line

    :param crit: Search text
    :type crit: str
    :return: predicate for a quoted string
    :rtype: function
    """
    def unquotedNotIn(crit, text):
        result = not bool(crit.search(text))
        Logger.debug('`%s` not in "%s" -> %s', crit.pattern, text, result)
        return result
    return partial(unquotedNotIn, re.compile(r'\b%s\b' % crit[0], re.IGNORECASE))

def RegexIn(crit):
    """
    Return predicate for regular expression appearing in line

    :param crit: Search text
    :type crit: str
    :return: predicate for a quoted string
    :rtype: function
    """
    def regexIn(crit, text):
        result = bool(crit.search(text))
        Logger.debug('/%s/ in "%s" -> %s', crit.pattern, text, result)
        return result
    return partial(regexIn, re.compile(crit[0], reduce(or_, (REGEX_FLAGS[f] for f in crit[1]), 0)))

def RegexNotIn(crit):
    """
    Return predicate for regular expression not appearing in line

    :param crit: Search text
    :type crit: str
    :return: predicate for a quoted string
    :rtype: function
    """
    def regexNotIn(crit, text):
        result = not bool(crit.search(text))
        Logger.debug('/%s/ not in "%s" -> %s', crit.pattern, text, result)
        return result
    return partial(regexNotIn, re.compile(crit[0], reduce(or_, (REGEX_FLAGS[f] for f in crit[1]), 0)))

# Table of (criterion, predicate) generation function pairs
SPECIFIERS = (
    (re.compile(r'\s*\^\s*["\']([^"\']*)["\']\s*'), QuotedNotIn),
    (re.compile(r'\s*["\']([^"\']*)["\']\s*'), QuotedIn),
    (re.compile(r'\s*\^\s*/([^/]*)/\s*([iIlLmMsSuUxX]*)\s*'), RegexNotIn),
    (re.compile(r'\s*/([^/]*)/\s*([iIlLmMsSuUxX]*)\s*'), RegexIn),
    (re.compile(r'\s*"([^"]*)\s*'), (RuntimeError, 'Unterminated quote, did you mean "{1}"?')),
    (re.compile(r'\s*\^\s*["]([^"]*)\s*'), (RuntimeError, 'Unterminated quote, did you mean ^"{1}"?')),
    (re.compile(r"\s*'([^']*)\s*"), (RuntimeError, "Unterminated quote, did you mean '{1}'?")),
    (re.compile(r"\s*\^\s*'([^']*)\s*"), (RuntimeError, "Unterminated quote, did you mean ^'{1}'?")),
    (re.compile(r'\s*\^\s*([^/].*)\s*'), UnquotedNotIn),
    (re.compile(r'\s*(.*)\s*'), UnquotedIn),
)

def Reader(path, fullscan, queue):
    """
    Deliver new log events via queue

    :param path: log path
    :type path: str
    :param fullscan: whether to scan logfile from start
    :type fullscan: bool
    :param queue: queue to send line information to
    :type queue:  Queue

    Intended to be run asynchronously for every log file to scan
    """
    logger = logging.getLogger(path)
    stopDelay = False
    exceptionCount = 0
    lastException = 0
    while True:
        try:
            delay = LOG_POLL_MIN_SLEEP
            logger.debug('Reset sleep to %f', delay)
            with open(path, 'rU') as f:
                seqNo = 0
                inode = fstat(f.fileno()).st_ino
                if not fullscan:
                    f.seek(0, io.SEEK_END)
                lastCheck = time.time()
                ok = True
                while ok:
                    line = f.readline()
                    if line:
                        queue.put((path, seqNo, line.rstrip()))
                        if not fullscan:
                            sleep(0)
                        delay = LOG_POLL_MIN_SLEEP
                        stopDelay = False
                    else:
                        sleep(delay)
                        if delay <= LOG_POLL_MAX_SLEEP:
                            delay += LOG_POLL_SLEEP_STEP
                        else:
                            if not stopDelay:
                                stopDelay = True
                    if time.time() > lastCheck + 2:
                        ok = stat(path).st_ino == inode
                        if not ok:
                            logger.info('Log rotation')
                        lastCheck = time.time()
                    if lastException and time.time() > lastException + 60:
                        lastException = 0
                        exceptionCount = 0
                    seqNo += 1
            fullscan = False
        except Exception:
            logger.critical('Exception', exc_info=True)
            exceptionCount += 1
            lastException = time.time()
            if exceptionCount > 3:
                logger.critical('Too many exceptions, bailing out')
                return

class ConfigurationError(RuntimeError):
    """
    Configuration error
    """

class Scanner(object):
    """
    Scanner
    """

    def __init__(self, item, contextLength=10):
        """
        Create a Scanner object
        """
        self.contextLength = contextLength
        self.handlers = self.parseBody(item)
        self.context = {}

    def run(self, log, seqNo, message):
        """
        Run scanner

        :param log: logfile path
        :type log: str
        :param seqNo: sequence number of line
        :type seqNo: int
        :param message: log line
        :type message: str

        Evaluates all sections' `when` clause and runs the `do` clause of those that evaluate to True
        """
        for h in self.handlers:
            context = self.context.setdefault(log, deque(maxlen=self.contextLength))
            if self.runOrFilter(h[0], message):
                h[1].run(dict(logfile=log, sequenceNo=seqNo, message=message, context=context))
            context.append(message)

    def runOrFilter(self, items, text):
        """
        Evaluate OR list

        :param items:
        :type items:
        :return: True if all items and sub lists evaluate to True
        :rtype: bool

        Dispatches a filter item to the corresponding method
        """
        result = any(self.runAndFilter(item, text) if isinstance(item, list) else item(text) for item in items)
        Logger.debug('OR block: %s', result)
        return result

    def runAndFilter(self, items, text):
        """
        Evaluate AND list

        :param items:
        :type items:
        :return: true if one of the items or sub lists evaluate to True
        :rtype: bool
        """
        result = all(self.runOrFilter(item, text) if isinstance(item, list) else item(text) for item in items)
        Logger.debug('AND block: %s', result)
        return result

    def parseBody(self, items):
        """
        Handle filter body

        :param items:
        :type items:
        :return: a list of pairs of when/do blocks
        :rtype: list

        """
        items = list(items)
        for i in items:
            if 'when' not in i:
                raise ConfigurationError('Condition block must have a "when" clause')
        return [
            (self.parseCriterionList(i['when']), self.parseDo(i.get('do', DEFAULT_DO)))
            for i in items
            if i.get('disabled', not i.get('enabled'))
        ]

    def parseDo(self, items):
        """
        Prepare code

        :return:
        :rtype:
        """
        if isinstance(items, list) and all(isinstance(i, basestring) for i in items):
            language, block = items
        elif isinstance(items, basestring):
            language, block = 'bash', items
        else:
            raise ConfigurationError('A do clause must be either a string or a list of strings, but got ' + repr(items))
        return LANGUAGE_HANDLERS[language](block)

    def parseCriterionList(self, items):
        """
        Handle item

        :param items:
        :type items:
        :return:
        :rtype:

        Creates a list of
        """
        return [self.parseCriterionList(i) if isinstance(i, list) else self.criterion(i) for i in items]

    @staticmethod
    def criterion(text):
        """
        Handle criterion

        :param text:
        :type text:
        :return:
        :rtype:

        Returns a function filter from a specifier in the configuration
        """
        if isinstance(text, dict):
            raise ConfigurationError('Search criterion is non-string. Did you forget to quote a string with a colon?')
        if isinstance(text, list):
            raise ConfigurationError(
                'Search criterion is non-string. Did you forget to quote a string with "[" and "]"?'
            )
        if text is None:
            raise ConfigurationError('Search criterion is non-string. Did you forget to quote "null" or "~"?')
        if isinstance(text, bool):
            raise ConfigurationError(
                'Search criterion is non-string. Did you forget to quote "yes"/"no"/"on"/"off"/"true"/"false"?'
            )
        if not isinstance(text, basestring):
            raise ConfigurationError(
                'Search criterion is non-string (%s). Did you forget to quote?' % type(text).__name__
            )
        for regex, action in SPECIFIERS:
            match = regex.match(text)
            if match:
                if isinstance(action, tuple) and issubclass(action[0], Exception):
                    raise action[0](action[1].format(*(text,) + match.groups()))
                return action(match.groups())
        raise RuntimeError('Invalid text specifier: %s' % text)

def Main():
    import sys
    from argparse import ArgumentParser, Action

    class Version(Action):
        def __call__(self, *args, **kwargs):
            print(VERSION)
            sys.exit(0)

    class Program(object):
        """
        Program
        """

        def __init__(self):
            argp = ArgumentParser()
            argp.add_argument('logfile', nargs='+')
            argp.add_argument('--config', '-c', action='store', required=True, help='specify config file')
            argp.add_argument('--full', '-f', action='store_true', help='scan files from beginning')
            argp.add_argument('--debug', '-d', action='count', default=0, help='Print some debug information to stderr')
            argp.add_argument('--version', '-v', action=Version, nargs=0, help='display version and exit')
            self.args = argp.parse_args()

        def run(self):
            """
            Run program
            """
            logging.basicConfig(
                stream=sys.stderr,
                level=LOGGING_LEVELS[max(1, LOGGING_LEVELS.index(INITIAL_LOGGING_LEVEL) - self.args.debug)],
                format='%(asctime)s %(levelname)-8s %(name)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            Logger.info('lognotify version %s', __version__)
            if self.args.config:
                config = yaml.load_all(open(self.args.config))
                scanner = Scanner(config)
            else:
                scanner = None
            queue = Queue()
            for log in self.args.logfile:
                spawn(Reader, log, self.args.full, queue)
            try:
                while True:
                    log, seqNo, message = queue.get()
                    try:
                        scanner.run(log, seqNo, message)
                    except Exception:
                        Logger.critical('Exception caught in scanner.run()', exc_info=True)
            except LoopExit:
                Logger.info('lognotify terminating')
            return 0

    program = Program()
    sys.exit(program.run())

if __name__ == '__main__':
    Main()
