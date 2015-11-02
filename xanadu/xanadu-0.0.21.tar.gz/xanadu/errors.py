#!/usr/bin/env python
# encoding=utf-8

from .util import *

__author__ = 'xlzd'


class HTTPError(Exception):
    """
    HTTP error.
    """
    def __init__(self, error_code):
        super(HTTPError, self).__init__()
        self._error_code = error_code
        self._status = '%d %s' % (error_code, RESPONSE_STATUSES[error_code])
        self._headers = [HEADER_X_POWERED_BY]

    def header(self, name, value):
        self._headers.append((name, value))

    @property
    def headers(self):
        return self._headers

    @property
    def status(self):
        return self._status

    def __str__(self):
        return self._status

    __repr__ = __str__


class RedirectError(HTTPError):
    """
    Redirect error
    """

    def __init__(self, code, location):
        super(RedirectError, self).__init__(code)
        self._location = location

    @property
    def location(self):
        return self._location

    def __str__(self):
        return '{status}, {location}'.format(status=self._status, location=self._location)

    __repr__ = __str__


_gen_error = lambda code: lambda: HTTPError(code)

badrequest = _gen_error(400)
unauthorized = _gen_error(401)
forbidden = _gen_error(403)
notfound = _gen_error(404)
internalerror = _gen_error(500)
redirect = lambda location: RedirectError(301, location)
found = lambda location: RedirectError(302, location)
seeother = lambda location: RedirectError(303, location)
