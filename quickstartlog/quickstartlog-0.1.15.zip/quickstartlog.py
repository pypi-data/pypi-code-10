import os
import sys
import logging
import logging.handlers
import ctypes


__version__ = '0.1.15'


if sys.version_info[0] == 3:
    _unicode = str
    _base_string = str
else:
    _unicode = unicode
    _base_string = basestring


_domain = None
_level = logging.INFO
_format = ['[%(asctime)s %(levelname)-5.5s] %(message)s', '%H:%M:%S']

_prog = os.path.basename(sys.argv[0])
_prog_ext_index = _prog.rfind('.')
if _prog_ext_index != -1:
    _prog = _prog[:_prog_ext_index]

_file_path = os.path.join('var', 'log', '%s.log' % _prog)

_file_encoding = 'utf8'
_default_msg_encodings = ['utf8', 'gbk']
_msg_encoding = _default_msg_encodings[:]

_logger = None


class Error(Exception):
    pass


class UnsupportedMessageEncoding(Error):
    def __init__(self, msg):
        Error.__init__(self, msg)
        self.msg = msg

    def __str__(self):
        return "Message '%s' can't decode by [%s]" % (self.msg, ', '.join(_msg_encoding))


if os.name == 'nt':
    BLACK = 0X00
    GRAY = 0X08

    BLUE = 0X01
    LIGHT_BLUE = 0X09

    GREEN = 0X02
    LIGHT_GREEN = 0X0A

    AQUA = 0X03
    LIGHT_AQUA = 0X0B

    RED = 0X04
    LIGHT_RED = 0X0C

    PURPLE = 0X05
    LIGHT_PURPLE = 0X0D

    YELLOW = 0X06
    LIGHT_YELLOW = 0X0E

    WHITE = 0X07
    BRIGHT_WHITE = 0X0F

    DEFAULT_FORE_COLOR = WHITE
    DEFAULT_BACK_COLOR = BLACK
else:
    raise NotImplementedError('Unsupported os.')


class _LoggingWithColoredConsole(object):
    def __init__(self, log_func_name, fore_color, back_color):
        self.log_func_name = log_func_name
        self.fore_color = fore_color
        self.back_color = back_color
    def __call__(self, msg, *args, **kwargs):
        adjust_args = []
        for arg in args:
            adjust_args.append(_decode(arg) if isinstance(arg, _base_string) else arg)
        exec('_get_logger().%s(_decode(msg), *adjust_args, **kwargs)' % self.log_func_name)


class _WindowsLoggingWithColoredConsole(_LoggingWithColoredConsole):
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    handle = ctypes.windll.kernel32.GetStdHandle(STD_ERROR_HANDLE)

    def __init__(self, log_func_name, fore_color=DEFAULT_FORE_COLOR, back_color=DEFAULT_BACK_COLOR):
        super(_WindowsLoggingWithColoredConsole, self).__init__(log_func_name, fore_color, back_color)
    def __call__(self, msg, *args, **kwargs):
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.__class__.handle, self.fore_color|self.back_color)
        super(_WindowsLoggingWithColoredConsole, self).__call__(msg, *args, **kwargs)
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.__class__.handle, DEFAULT_FORE_COLOR|DEFAULT_BACK_COLOR)


_cls_LoggingWithColoredConsole = _WindowsLoggingWithColoredConsole if os.name == 'nt' else _LoggingWithColoredConsole


def set_domain(domain):
    global _domain
    _domain = domain


def set_level(level):
    global _level
    _level = level


def set_format(fmt=None, datefmt=None):
    global _format
    if fmt is not None:
        _format[0] = fmt
    if datefmt is not None:
        _format[1] = datefmt


def set_file_path(path):
    global _file_path
    _file_path = path


def set_file_encoding(encoding):
    global _file_encoding
    _file_encoding = encoding


def set_msg_encoding(encoding):
    global _msg_encoding
    _msg_encoding.remove(encoding)
    _msg_encoding.insert(0, encoding)


def debug_ex(*args, **kwargs):
    return _cls_LoggingWithColoredConsole('debug', *args, **kwargs)


def info_ex(*args, **kwargs):
    return _cls_LoggingWithColoredConsole('info', *args, **kwargs)


def warn_ex(*args, **kwargs):
    return _cls_LoggingWithColoredConsole('warn', *args, **kwargs)


def error_ex(*args, **kwargs):
    return _cls_LoggingWithColoredConsole('error', *args, **kwargs)


def critical_ex(*args, **kwargs):
    return _cls_LoggingWithColoredConsole('critical', *args, **kwargs)


def debug(msg, *args, **kwargs):
    debug_ex()(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    info_ex()(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    warn_ex(LIGHT_YELLOW)(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    error_ex(LIGHT_RED)(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    critical_ex(LIGHT_RED)(msg, *args, **kwargs)


def _create_logger():
    logger = logging.getLogger(_domain)
    logger.setLevel(_level)

    formatter = logging.Formatter(_format[0], _format[1])

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    dir_path = os.path.dirname(_file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_handler = logging.handlers.TimedRotatingFileHandler(_file_path, 'D', 1, 30, _file_encoding)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _create_logger()
    return _logger


def _decode(msg):
    if isinstance(msg, _unicode):
        return msg
    else:
        for encoding in _msg_encoding:
            try:
                return msg.decode(encoding)
            except:
                pass
        raise UnsupportedMessageEncoding(msg)