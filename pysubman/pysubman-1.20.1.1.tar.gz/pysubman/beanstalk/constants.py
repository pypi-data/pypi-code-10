#!/usr/bin/env python

CRLF = "\r\n"
DEFAULT_PRIORITY = 2 ** 31
DEFAULT_TTR = 10 * 60  # 10min
DEFAULT_ADDRESS = 'localhost:11300'

JOB_STATUS_UNTREATED = 0
JOB_STATUS_ERROR = 100
JOB_STATUS_SUCCESS = 10


class JobException(Exception):
    pass


class ConsumerException(Exception):
    pass
