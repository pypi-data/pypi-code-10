#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from .util import *

reload(sys)
sys.setdefaultencoding("utf-8")


class Request(object):
    """
    request
    """
    def __init__(self, environ):
        self._environ = environ

    def _parse_input(self):
        def _convert(item):
            if isinstance(item, list):
                return [to_unicode(each.value) for each in item]
            if item.filename:
                return MultipartFile(item)
            return to_unicode(item.value)
        fs = cgi.FieldStorage(fp=self._environ['wsgi.input'], environ=self._environ, keep_blank_values=True)
        return {key: _convert(fs[key]) for key in fs}

    def _get_raw_input(self):
        """
        Get raw input as dict containing values as unicode, list or MultipartFile.
        """
        if not hasattr(self, '_raw_input'):
            self._raw_input = self._parse_input()
        return self._raw_input

    def __getitem__(self, item):
        value = self._get_raw_input()[item]
        if isinstance(value, list):
            return value[0]
        return value

    def get(self, key, default=None):
        value = self._get_raw_input().get(key, default)
        if isinstance(value, list):
            return value[0]
        return value

    def gets(self, key):
        value = self._get_raw_input()[key]
        if isinstance(value, list):
            return value[:]
        return [value]

    def input(self, **kwargs):
        """
        Get input as dict from request, fill dict using provided default value if key not exist.
        """
        raw = self._get_raw_input()
        for key, value in raw.iteritems():
            kwargs[key] = value[0] if isinstance(value, list) else value
        return kwargs

    def get_body(self):
        """
        Get raw data from HTTP POST and return as str.
        """
        return self._environ['wsgi.input'].read()

    @property
    def remote_addr(self):
        return self._environ.get('REMOTE_ADDR', '0.0.0.0')

    @property
    def document_root(self):
        return self._environ.get('DOCUMENT_ROOT', '')

    @property
    def query_string(self):
        return self._environ.get('QUERY_STRING', '')

    @property
    def environ(self):
        return self._environ

    @property
    def request_method(self):
        return self._environ['REQUEST_METHOD']

    @property
    def path_info(self):
        return unquote(self._environ.get('PATH_INFO', ''))

    @property
    def host(self):
        return self._environ.get('HTTP_HOST', '')

    def _get_headers(self):
        if not hasattr(self, '_headers'):
            headers = {}
            for key, value in self._environ.iteritems():
                if key.startswith('HTTP_'):
                    headers[key[5:].replace('_', '-').upper] = to_unicode(value)
            self._headers = headers
        return self._headers

    @property
    def headers(self):
        return dict(**self._get_headers())

    def header(self, header, default=None):
        return self._get_headers().get(header.upper(), default)

    def _get_cookies(self):
        if not hasattr(self, '_cookies'):
            cookies = {}
            cookie_str = self._environ.get('HTTP_COOKIE', '')
            for ck in cookie_str.split(';'):
                pos = ck.find('=')
                if pos > 0:
                    cookies[ck[:pos].strip()] = unquote(ck[pos + 1:])
            self._cookies = cookies
        return self._cookies

    @property
    def cookies(self):
        return dict(**self._get_cookies())

    def cookie(self, name, default):
        return self._get_cookies().get(name, default)

