# -*- coding: utf-8 -*-
# Created by lvjiyong on 15/6/15

__all__ = ['logger', 'set_level']

import logging
# import logging.config
import sys

log_console = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")

logger = logging.getLogger('debuglog')
logger.setLevel(logging.DEBUG)
log_console.setFormatter(formatter)
logger.addHandler(log_console)


def set_level(log_level):
    global logger
    if log_level == logging.ERROR:
        logger.removeHandler(log_console)
    logger.setLevel(log_level)


def set_formatter(log_formatter):
    global logger
    log_console.setFormatter(log_formatter)


def get_logger(name, level=logging.DEBUG, formatter=formatter):
    name_logger = logging.getLogger(name)
    name_logger.setLevel(level)
    name_logger.addHandler(log_console)
    set_formatter(formatter)
    return name_logger
