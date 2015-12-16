import os
import sys
import logging
import logging.handlers

DEFAULT_LOGGER_FORMAT = logging.Formatter('[%(asctime)s] %(message)s')
NO_FILE_INDICATOR = {'file': False}
NO_CONSOLE_INDICATOR = {'console': False}

class ExtraAttributeLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET, extra_record_args=None):
        logging.Logger.__init__(self, name, level=level)
        self.extra_record_args = extra_record_args or {}

    def _log(self, level, msg, args, exc_info=None, extra=None):
        if extra is None:
            extra = {}
        extra = dict(self.extra_record_args, **extra)
        logging.Logger._log(self, level, msg, args, exc_info=exc_info, extra=extra)

class DebugEvalLogger(logging.Logger):
    def debug_generate(self, debug_generator, *gen_args, **gen_kwargs):
        '''
        Used for efficient debug logging, where the actual message isn't evaluated unless it
        will actually be accepted by the logger.
        '''
        if self.isEnabledFor(logging.DEBUG):
            message = debug_generator(*gen_args, **gen_kwargs)
            # Allow for content filtering to skip logging
            if message is not None:
                return self.debug(message)

class FileFilter(logging.Filter):
    def filter(self, record):
        return getattr(record, 'file', True)

class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return getattr(record, 'console', True)

class SubErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

class StdOutForwarder(object):
    '''
    Used to forward content to the current sys.stdout. This allows for rebinding sys.stdout without
    remapping associations in loggers
    '''
    def write(self, content):
        sys.stdout.write(content)

    def flush(self):
        sys.stdout.flush()

    def isatty(self):
        return sys.stdout.isatty()

class StdErrForwarder(object):
    '''
    Used to forward content to the current sys.stdout. This allows for rebinding sys.stdout without
    remapping associations in loggers
    '''
    def write(self, content):
        sys.stderr.write(content)

    def flush(self):
        sys.stderr.flush()

    def isatty(self):
        return sys.stderr.isatty()

class DefaultLogger(ExtraAttributeLogger, DebugEvalLogger):
    def apply_default_handlers(
        self,
        log_dir=None,
        console_enabled=True,
        max_log_size=5*1024*1024,
        max_backup_logs=5,
        formatter=DEFAULT_LOGGER_FORMAT):
        
        if console_enabled:
            stdout_handler = logging.StreamHandler(StdOutForwarder())
            stdout_handler.setFormatter(formatter)
            stdout_handler.addFilter(ConsoleFilter())
            stdout_handler.addFilter(SubErrorFilter())
            self.addHandler(stdout_handler)

            stderr_handler = logging.StreamHandler(StdErrForwarder())
            stderr_handler.setLevel(logging.ERROR)
            stderr_handler.setFormatter(formatter)
            stderr_handler.addFilter(ConsoleFilter())
            self.addHandler(stderr_handler)

        if log_dir:
            file_handler = logging.handlers.RotatingFileHandler(os.path.join(log_dir, 'console.log'),
                maxBytes=max_log_size, backupCount=max_backup_logs)
            file_handler.setFormatter(formatter)
            file_handler.addFilter(FileFilter())
            self.addHandler(file_handler)

            error_file_handler = logging.handlers.RotatingFileHandler(
                os.path.join(log_dir, 'errors.log'),
                maxBytes=max_log_size,
                backupCount=max_backup_logs)
            error_file_handler.setLevel(logging.ERROR)
            error_file_handler.setFormatter(formatter)
            error_file_handler.addFilter(FileFilter())
            self.addHandler(error_file_handler)

            # Overwrites the log each run
            session_file_handler = logging.FileHandler(os.path.join(log_dir, 'session.log'), mode='wb')
            session_file_handler.setFormatter(formatter)
            session_file_handler.addFilter(FileFilter())
            self.addHandler(session_file_handler)

def build_default_logger(
    logger_name='logger',
    log_level=None,
    log_dir=None,
    console_enabled=True,
    max_log_size=5*1024*1024,
    max_backup_logs=5):
    '''
    Generates a logger that outputs messages in the same format as default Flask applications.
    '''
    old_logger_class = logging.getLoggerClass()
    logging.setLoggerClass(DefaultLogger)
    logger = logging.getLogger(logger_name)
    logging.setLoggerClass(old_logger_class)

    if log_level:
        logger.setLevel(log_level)
    logger.apply_default_handlers(log_dir, console_enabled, max_log_size, max_backup_logs)
    return logger
