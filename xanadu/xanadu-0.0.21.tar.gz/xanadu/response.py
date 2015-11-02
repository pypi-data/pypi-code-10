#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from .util import *
reload(sys)
sys.setdefaultencoding("utf-8")


class Response(object):

    PATTERN_RESPONSE_STATUS = re.compile(r'^\d\d\d(\ [\w\ ]+)?$')

    def __init__(self):
        self._status = '200 OK'
        self._headers = {'CONTENT-TPYE': 'text/html; charset=utf-8'}

    @property
    def headers(self):
        """
        Return response headers as [(key1, value1), (key2, value2)...] including cookies.
        """
        headers = [(RESPONSE_HEADER_DICT.get(k, k), v) for k, v in self._headers.iteritems()]
        if hasattr(self, '_cookies'):
            for value in self._cookies.itervalues():
                headers.append(('Set-Cookie', value))
        headers.append(HEADER_X_POWERED_BY)
        return headers

    def header(self, name):
        key = name.upper()
        if key not in RESPONSE_HEADER_DICT:
            key = name
        return self._headers.get(key)

    def unset_header(self, name):
        key = name.upper()
        if key not in RESPONSE_HEADER_DICT:
            key = name
        if key in self._headers:
            del self._headers['key']

    def set_header(self, name, value):
        key = name.title()
        if key not in RESPONSE_HEADER_DICT:
            key = name
        self._headers[key] = to_str(value)

    @property
    def content_type(self):
        return self.header('CONTENT-TYPE')

    @content_type.setter
    def content_type(self, value):
        if value:
            self.set_header('CONTENT-TYPE', value)
        else:
            self.unset_header('CONTENT-TYPE')

    @property
    def content_length(self):
        return self.header('CONTENT-LENGTH')

    @content_length.setter
    def content_length(self, value):
        self.set_header('CONTENT-LENGTH', to_str(value))

    def del_cookie(self, name):
        self.set_cookie(name, '__deleted__', expires=0)

    def set_cookie(self, name, value, max_age=None, expires=None, path='/', domain=None, secure=False, http_only=True):
        if not hasattr(self, '_cookies'):
            self._cookies = {}
        lst = ['{name}={value}'.format(name=quote(name), value=quote(value))]
        if expires is not None:
            if isinstance(expires, (float, int, long)):
                lst.append('Expires={}'.format(datetime.datetime.fromtimestamp(expires, UTC_0).strftime(TIME_FORMAT)))
            if isinstance(expires, (datetime.date, datetime.datetime)):
                lst.append('Expires=%s' % expires.astimezone(UTC_0).strftime(TIME_FORMAT))
        elif isinstance(max_age, (int, long)):
            lst.append('Max-Age=%d' % max_age)
        lst.append('Path=%s' % path)
        if domain:
            lst.append('Domain=%s' % domain)
        if secure:
            lst.append('Secure')
        if http_only:
            lst.append('HttpOnly')
        self._cookies[name] = '; '.join(lst)

    def unset_coookie(self, name):
        if hasattr(self, '_cookies'):
            if name in self._cookies:
                del self._cookies[name]

    @property
    def status_code(self):
        return int(self._status[:3])

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, (int, long)):
            if 100 <= value <= 999:
                st = RESPONSE_STATUSES.get(value, '')
                if st:
                    self._status = '%d %s' % (value, st)
                else:
                    self._status = str(value)
            else:
                raise ValueError('Bad response code: %d' % value)
        elif isinstance(value, basestring):
            value = to_str(value)
            if self.PATTERN_RESPONSE_STATUS.match(value):
                self._status = value
            else:
                raise ValueError('Bad response code: %s' % value)
        else:
            raise TypeError('Bad type of response code.')
