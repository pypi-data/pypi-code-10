#!/usr/bin/env python
# encoding=utf-8

"""
一些常用的帮助方法
"""

import urllib
import threading

from .const import *

__author__ = 'xlzd'

context = threading.local()


def quote(string, encoding='utf-8'):
    if isinstance(string, unicode):
        string = string.encode(encoding)
    return urllib.quote(string)


def unquote(string, encoding='utf-8'):
    return urllib.unquote(string).decode(encoding)


def to_str(obj):
    """
    convert a object to string
    """
    if isinstance(obj, str):
        return obj
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    return str(obj)


def to_unicode(obj):
    """
    convert a object to unicode string
    """
    return obj.decode('utf-8')


class UTC(datetime.tzinfo):
    def __init__(self, utc):
        super(UTC, self).__init__()
        utc = str(utc.strip().upper())
        mt = RE_TZ.match(utc)
        if not mt:
            raise ValueError('utc time zone error')
        minus = mt.group(1) == '-'
        h = int(mt.group(2))
        m = int(mt.group(3))
        if minus:
            h, m = -h, -m
        self._utcoffset = datetime.timedelta(hours=h, minutes=m)
        self._tzname = 'UTC' + utc

    def utcoffset(self, dt):
        return self._utcoffset

    def dst(self, dt):
        return TIMEDELTA_ZERO

    def tzname(self, dt):
        return self._tzname

    def __str__(self):
        return "UTC tzinfo object <%s>" % self._tzname

    __repr__ = __str__


UTC_0 = UTC('+00:00')
