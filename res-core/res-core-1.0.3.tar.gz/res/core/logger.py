"""
Resystem common service package.
Released under New BSD License.
Copyright © 2015, Vadim Markovtsev :: Angry Developers LLC
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Angry Developers LLC nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL VADIM MARKOVTSEV BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
# Portions of code were extracted from from https://github.com/Samsung/veles


import asyncio
import asyncio_mongo
from codecs import getwriter
import io
import logging
import logging.handlers
import os
import re
import sys
from time import time

from .configuration import r
from .utils import has_colors
from .argument_parser import get_argument_parser


class Logger(object):
    """
    Provides logging facilities to derived classes.
    """

    SET_UP = False

    class LoggerHasBeenAlreadySetUp(Exception):
        pass

    class ColorFormatter(logging.Formatter):
        GREEN_MARKERS = [' ok', "ok:", 'finished', 'completed', 'ready',
                         'done', 'running', 'successful', 'saved']
        GREEN_RE = re.compile("|".join(GREEN_MARKERS))

        def formatMessage(self, record):
            level_color = "0"
            text_color = "0"
            fmt = ""
            if record.levelno <= logging.DEBUG:
                fmt = "\033[0;37m" + logging.BASIC_FORMAT + "\033[0m"
            elif record.levelno <= logging.INFO:
                level_color = "1;36"
                lmsg = record.message.lower()
                if Logger.ColorFormatter.GREEN_RE.search(lmsg):
                    text_color = "1;32"
            elif record.levelno <= logging.WARNING:
                level_color = "1;33"
            elif record.levelno <= logging.CRITICAL:
                level_color = "1;31"
            if not fmt:
                fmt = "\033[" + level_color + \
                    "m%(levelname)s\033[0m:%(name)s:\033[" + text_color + \
                    "m%(message)s\033[0m"
            return fmt % record.__dict__

        if not hasattr(logging.Formatter, "formatMessage"):
            def format(self, record):
                record.message = record.getMessage()
                if self.usesTime():
                    record.asctime = self.formatTime(record, self.datefmt)
                s = self.formatMessage(record)
                if record.exc_info:
                    if not record.exc_text:
                        record.exc_text = self.formatException(record.exc_info)
                if record.exc_text:
                    if s[-1:] != "\n":
                        s += "\n"
                    try:
                        s += record.exc_text
                    except UnicodeError:
                        s += \
                            record.exc_text.decode(sys.getfilesystemencoding(),
                                                   'replace')
                return s

    @staticmethod
    def setup_logging(level=None):
        if Logger.SET_UP:
            raise Logger.LoggerHasBeenAlreadySetUp()
        Logger.SET_UP = True
        if level is None:
            # Figure out log level through sys.argv
            level = Logger.parse_log_level()
        Logger.ensure_utf8_streams()
        # Set basic log level
        logging.basicConfig(level=level, stream=sys.stdout)
        # Override the global log level and the output stream in case they have
        # been already changed previously
        root_logger = logging.getLogger()
        root_logger.level = level
        root_logger.handlers[0].stream = sys.stdout
        # Turn on colors in case of an interactive out tty or IPython
        if has_colors():
            root = logging.getLogger()
            handler = root.handlers[0]
            handler.setFormatter(Logger.ColorFormatter())

    @staticmethod
    def parse_log_level():
        parser = init_argument_parser(get_argument_parser())
        args, _ = parser.parse_known_args()
        return logging.ERROR - min(args.verbose, 3) * 10

    @staticmethod
    def redirect_stream(system_stream, target_stream):
        """ Redirect a system stream to a specified file.
            `system_stream` is a standard system stream such as
            ``sys.stdout``. `target_stream` is an open file object that
            should replace the corresponding system stream object.
            If `target_stream` is ``None``, defaults to opening the
            operating system's null device and using its file descriptor.
            """
        if target_stream is None:
            target_fd = os.open(os.devnull, os.O_RDWR)
        else:
            target_fd = target_stream.fileno()
        os.dup2(target_fd, system_stream.fileno())

    @staticmethod
    def ensure_utf8_streams():
        """Forces UTF-8 on stdout and stderr; in some crazy environments,
        they use 'ascii' encoding by default
        """

        def ensure_utf8_stream(stream):
            if not isinstance(stream, io.StringIO):
                stream = getwriter("utf-8")(getattr(stream, "buffer", stream))
                stream.encoding = "utf-8"
            return stream

        sys.stdout, sys.stderr = (ensure_utf8_stream(s)
                                  for s in (sys.stdout, sys.stderr))

    def __init__(self, **kwargs):
        self._logger_ = kwargs.get(
            "logger", logging.getLogger(self.__class__.__name__))
        try:
            super(Logger, self).__init__()
        except TypeError as e:
            mro = type(self).__mro__
            mro.index(Logger)
            self.error("Failed to call __init__ in super() = %s",
                       mro[mro.index(Logger) + 1])
            raise e from None

    @property
    def logger(self):
        """Returns the logger associated with this object.
        """
        return self._logger_

    @logger.setter
    def logger(self, value):
        if not isinstance(value, logging.Logger):
            raise TypeError("value must be an instance of type logging.Logger")
        self._logger_ = value

    def __getstate__(self):
        parent = super(Logger, self)
        state = getattr(parent, "__getstate__", lambda: {})()
        state["_logger_"] = self.logger.name
        return state

    def __setstate__(self, state):
        logger = state.get("_logger_")
        if logger is not None:
            self._logger_ = state["_logger_"] = logging.getLogger(logger)
        getattr(super(Logger, self), "__setstate__", lambda _: None)(state)

    @staticmethod
    def redirect_all_logging_to_file(file_name, max_bytes=1024 * 1024,
                                     backups=1):
        handler = logging.handlers.RotatingFileHandler(
            filename=file_name, maxBytes=max_bytes, backupCount=backups,
            encoding="utf-8"
        )
        formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: "
                                      "%(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logging.getLogger("Logger").info("Will save the logs to %s", file_name)
        if not has_colors():
            logging.getLogger().handlers[0] = handler
            sys.stderr.flush()
            stderr = open("%s.stderr%s" % os.path.splitext(file_name), 'a',
                          encoding="utf-8")
            Logger.redirect_stream(sys.stderr, stderr)
            sys.stderr = stderr
        else:
            logging.getLogger().handlers.append(handler)
        logging.getLogger().addFilter(handler)
        logging.getLogger("Logger").info("Continuing to log in %s", file_name)

    @staticmethod
    @asyncio.coroutine
    def duplicate_logs_to_mongo(docid, nodeid, root_path=None):
        parser = init_argument_parser(get_argument_parser())
        args, _ = parser.parse_known_args()
        if args.disable_logging_to_mongo:
            return
        if root_path is None:
            root_path = \
                os.path.dirname(next(iter(sys.modules["res"].__path__)))
        handler = MongoLogHandler(
            root_path=root_path, docid=docid, nodeid=nodeid, **r.logs.db)
        yield from handler.initialize()
        logging.getLogger("Logger").info(
            "Saving logs to Mongo on %s:%d (%s)",
            r.logs.db.host, r.logs.db.port, r.logs.db.db)
        logging.getLogger().addHandler(handler)

    @staticmethod
    @asyncio.coroutine
    def discard_logs_to_mongo():
        to_remove = []
        for handler in logging.getLogger().handlers:
            if isinstance(handler, MongoLogHandler):
                yield from handler.disconnect()
                to_remove.append(handler)
        for h in to_remove:
            logging.getLogger().handlers.remove(h)

    def _change_log_message(self, msg):
        return msg

    def msg_changeable(fn):
        def msg_changeable_wrapper(self, msg, *args, **kwargs):
            msg = self._change_log_message(msg)
            return fn(self, msg, *args, **kwargs)

        msg_changeable_wrapper.__name__ = fn.__name__ + "_msg_changeable"
        return msg_changeable_wrapper

    @msg_changeable
    def log(self, level, msg, *args, **kwargs):
        self.logger.log(
            level, msg, *args, extra={"caller": self.logger.findCaller()},
            **kwargs)

    @msg_changeable
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(
            msg, *args, extra={"caller": self.logger.findCaller()}, **kwargs)

    @msg_changeable
    def info(self, msg, *args, **kwargs):
        self.logger.info(
            msg, *args, extra={"caller": self.logger.findCaller()}, **kwargs)

    @msg_changeable
    def warning(self, msg, *args, **kwargs):
        self.logger.warning(
            msg, *args, extra={"caller": self.logger.findCaller()}, **kwargs)

    @msg_changeable
    def error(self, msg, *args, **kwargs):
        self.logger.error(
            msg, *args, extra={"caller": self.logger.findCaller()}, **kwargs)

    @msg_changeable
    def critical(self, msg, *args, **kwargs):
        self.logger.critical(
            msg, *args, extra={"caller": self.logger.findCaller()}, **kwargs)

    @msg_changeable
    def exception(self, msg="Exception", *args, **kwargs):
        self.logger.exception(
            msg, *args, extra={"caller": self.logger.findCaller()}, **kwargs)

    msg_changeable = staticmethod(msg_changeable)

    def event(self, name, etype, **info):
        """
        Records an event to MongoDB. Events can be later viewed in web status.
        Parameters:
            name: the name of the event, for example, "Work".
            etype: the type of the event, can be either "begin", "end" or
            "single".
            info: any extra event attributes.
        """
        if etype not in ("begin", "end", "single"):
            raise ValueError("Event type must any of the following: 'begin', "
                             "'end', 'single'")
        for handler in logging.getLogger().handlers:
            if isinstance(handler, MongoLogHandler):
                data = {"session": handler.log_id,
                        "instance": handler.node_id,
                        "time": time(),
                        "domain": self.__class__.__name__,
                        "name": name,
                        "type": etype}
                dupkeys = set(data.keys()).intersection(set(info.keys()))
                if len(dupkeys) > 0:
                    raise ValueError("Event kwargs may not contain %s" %
                                     dupkeys)
                data.update(info)
                handler.events.insert(data, w=0)


class MongoLogHandler(logging.Handler):
    def __init__(self, root_path, docid, nodeid, host, port=27017,
                 db="res_accounting", user=None, password=None,
                 level=logging.NOTSET):
        super(MongoLogHandler, self).__init__(level)
        self._client = host, port, db, user, password
        self._db = None
        self._collection = None
        self._log_id = docid
        self._node_id = nodeid
        self._root_path = root_path

    @asyncio.coroutine
    def initialize(self):
        db = self._client[2]
        self._client = yield from asyncio_mongo.Connection.create(
            *self._client)
        self._db = getattr(self._client, db)
        self._collection = self._db.logs

    @asyncio.coroutine
    def disconnect(self):
        client = self._client
        self._client = None
        return client.disconnect()

    @property
    def log_id(self):
        return self._log_id

    @property
    def node_id(self):
        return self._node_id

    def emit(self, record):
        if self._client is None:
            return
        data = dict(record.__dict__)
        for bs in ("levelno", "args", "msg", "module", "msecs", "processName"):
            del data[bs]
        if "caller" in data:
            data["pathname"], data["lineno"], data["funcName"], _ = \
                data["caller"]
            del data["caller"]
        data["session"] = self.log_id
        data["node"] = self.node_id
        data["pathname"] = pathname = os.path.normpath(data["pathname"])
        if os.path.isabs(pathname) and pathname.startswith(self._root_path):
            data["pathname"] = os.path.relpath(
                data["pathname"], self._root_path)
        if data["exc_info"] is not None:
            data["exc_info"] = repr(data["exc_info"])
        if "_id" in data:
            print(str(data["_id"]))
            data["_id"] = str(data["_id"])

        @asyncio.coroutine
        def insert():
            try:
                yield from self._collection.insert(data)
            except Exception as e:
                # https://bitbucket.org/mrdon/asyncio-mongo/pull-requests/1/update-bson-to-support-mongodb-26/diff
                sys.stderr.write(
                    "Failed to send the message to Mongo: %s: %s\n" %
                    (type(e), e))
            sys.stderr.flush()

        asyncio.async(insert())


def init_argument_parser(parser):
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="stdout log verbosity (may be set multiple times "
                             "for more verbosity)")
    parser.add_argument("--disable-logging-to-mongo", action="store_true")
    return parser
