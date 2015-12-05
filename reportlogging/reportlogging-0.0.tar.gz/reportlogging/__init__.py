# -*- coding:utf-8 -*-
import logging
import six
from cached_property import cached_property as reify
from logging.handlers import BufferingHandler
logger = logging.getLogger(__name__)

# warning: not threadsafe


def text_(s, encoding="utf-8"):
    if isinstance(s, six.binary_type):
        s = s.decode(encoding)
    return s


class ReportingMemoryHandler(BufferingHandler):
    def __init__(self, capacity=10000, has_history=True):
        super(ReportingMemoryHandler, self).__init__(capacity)
        self.has_history = has_history
        self.history = []

    def flush(self):
        self.acquire()
        if self.buffer:
            result = self.getvalue()
            if self.has_history:
                self.history.append(result)
        try:
            self.buffer = []
        finally:
            self.release()

    def emit(self, record):
        text = self.format(record)
        if text:
            super(ReportingMemoryHandler, self).emit(text)

    def getvalue(self):
        return u"\n".join(self.buffer)

    def getallvalue(self):
        self.flush()
        return u"\n".join(self.history)


class MultiLogger(object):
    def __init__(self, loggers=None):
        self.loggers = loggers or []

    def apply_all(self, name, *args, **kwargs):
        for logger in self.loggers:
            try:
                getattr(logger, name)(*args, **kwargs)
            except AttributeError:
                raise
            except Exception as e:
                logger.warn("exception is raised %s", e, exc_info=True)

    def debug(self, msg, *args, **kwargs):
        return self.apply_all("debug", msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return self.apply_all("info", msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return self.apply_all("warning", msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        return self.apply_all("warn", msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return self.apply_all("error", msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        return self.apply_all("exception", msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        return self.apply_all("critical", msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        return self.apply_all("fatal", msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        return self.apply_all("log", level, msg, *args, **kwargs)


class ReportLoggerManager(object):
    def __init__(self, logger_name="reporting", level=logging.INFO, handler_factory=ReportingMemoryHandler):
        self.handler_factory = handler_factory
        self.logger_name = logger_name
        self.level = level

    @reify
    def handler(self):
        handler = self.handler_factory()
        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)
        return handler

    @reify
    def formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    @reify
    def logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.level)
        return logger

    def getLogger(self, *loggers):
        loggers = list(loggers[:])
        loggers.append(self.logger)
        return MultiLogger(loggers)

    def activate(self, level=None, format=None, style="%"):
        if level is not None:
            self.logger.setLevel(level)
            self.handler.setLevel(level)
        if format is not None:
            self.formatter = logging.Formatter(format, style=style)
            self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def getvalue(self):
        return self.handler.getallvalue()

manager = ReportLoggerManager()
