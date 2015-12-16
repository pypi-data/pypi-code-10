import sys
import time
import logging
import logging.handlers
from .default import DefaultLogger

MONTH_NAMES = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class OrderedFormatsFormatter(logging.Formatter):
    '''
    Allows for multiple _fmt to be applied in order until all their keys are
    accounted for and processed.

    OrderedFormatsFormatter(['%(host)s -- %(message)s', '%(message)s'])
    creates a formatter that will first try to format a host into the message
    and default to just message if the 'host' argument is not present in the
    record.
    '''

    def usesTime(self, fmt=None):
        '''
        Check if the format uses the creation time of the record.
        '''
        if fmt is None:
            fmt = self._fmt
        if not isinstance(fmt, basestring):
            fmt = fmt[0]
        return fmt.find('%(asctime)') >= 0

    def format(self, record):
        # Copied from logger default formatter with array of formats awareness
        record.message = record.getMessage()
        fmts = self._fmt
        if isinstance(fmts, basestring):
            fmts = [fmts]

        for fmt in fmts:
            if self.usesTime(fmt):
                record.asctime = self.formatTime(record, self.datefmt)
            try:
                s = fmt % record.__dict__
                break
            except KeyError:
                continue

            if record.exc_info:
                # Cache the traceback text to avoid converting it multiple times
                # (it's constant anyway)
                if not record.exc_text:
                    record.exc_text = self.formatException(record.exc_info)
            if record.exc_text:
                if s[-1:] != '\n':
                    s = s + '\n'
                try:
                    s = s + record.exc_text
                except UnicodeError:
                    # Sometimes filenames have non-ASCII chars, which can lead
                    # to errors when s is Unicode and record.exc_text is str
                    # See issue 8924.
                    # We also use replace for when there are multiple
                    # encodings, e.g. UTF-8 for the filesystem and latin-1
                    # for a script. See issue 13232.
                    s = s + record.exc_text.decode(sys.getfilesystemencoding(), 'replace')
        return s

class FlaskStyleTimeFormatter(OrderedFormatsFormatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        year, month, day, hh, mm, ss, x, y, z = ct
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            s = '%02d/%3s/%04d %02d:%02d:%02d' % (day, MONTH_NAMES[month], year, hh, mm, ss)
        return s

FLASK_FORMAT = FlaskStyleTimeFormatter(
    ['%(host)s - - [%(asctime)s] %(message)s',
    '[%(asctime)s] %(message)s',
    '%(message)s'])

class FlaskLikeLogger(DefaultLogger):
    def set_host(self, host):
        self.extra_record_args['host'] = host

    def apply_default_handlers(
        self,
        log_dir=None,
        console_enabled=True,
        max_log_size=5*1024*1024,
        max_backup_logs=5,
        formatter=FLASK_FORMAT):
        DefaultLogger.apply_default_handlers(
            self,
            log_dir,
            console_enabled,
            max_log_size,
            max_backup_logs,
            formatter)

def build_flask_like_logger(
    logger_name='logger',
    log_level=None,
    log_dir=None,
    console_enabled=True,
    max_log_size=5*1024*1024,
    max_backup_logs=5,
    host=None):
    '''
    Generates a logger that outputs messages in the same format as default Flask applications.
    '''
    old_logger_class = logging.getLoggerClass()
    logging.setLoggerClass(FlaskLikeLogger)
    logger = logging.getLogger(logger_name)
    logging.setLoggerClass(old_logger_class)

    if log_level:
        logger.setLevel(log_level)
    if host:
        logger.set_host(host)
    logger.apply_default_handlers(log_dir, console_enabled, max_log_size, max_backup_logs)
    return logger
