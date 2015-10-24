"""
Syncronous adapter based on the 'requests' library.
"""

from __future__ import print_function, division

import json
import requests
from syndicate.adapters import base


class SyncAdapter(base.AdapterBase):

    def __init__(self, config=None):
        self.session = requests.Session(**(config or {}))
        self.request_timeout = None
        self.connect_timeout = None
        super(SyncAdapter, self).__init__()

    def set_header(self, header, value):
        self.session.headers[header] = value

    def get_header(self, header):
        return self.session.headers[header]

    def set_cookie(self, cookie, value):
        self.session.cookies[cookie] = value

    def get_cookie(self, cookie):
        return self.session.cookies.get_dict()[cookie]

    @property
    def auth(self):
        return self.session.auth

    @auth.setter
    def auth(self, value):
        self.session.auth = value

    def request(self, method, url, data=None, query=None, callback=None,
                timeout=None):
        if data is not None:
            data = self.serializer.encode(data)
        if timeout is None:
            timeout = self.connect_timeout, self.request_timeout
        resp = self.session.request(method, url, data=data, params=query,
                                    timeout=timeout)
        content = None
        try:
            if resp.content and len(resp.content):
                content = self.serializer.decode(resp.content.decode())
        except Exception as e:
            error = e
            content = None
        else:
            error = None
        r = base.Response(http_code=resp.status_code, headers=resp.headers,
                          content=content, error=error, extra=resp)
        data = self.ingress_filter(r)
        if callback:
            callback(data)
        return data


class HeaderAuth(requests.auth.AuthBase):
    """ A simple header based auth.  Instantiate this with header name and
    value arguments for a single header or with a dictionary of name/value
    pairs. """

    def __init__(self, header_or_headers_dict, value=None):
        if hasattr(header_or_headers_dict, 'items'):
            self.headers = header_or_headers_dict.copy()
        else:
            self.headers = {header_or_headers_dict: value}

    def __call__(self, request):
        request.headers.update(self.headers)
        return request


class LoginAuth(requests.auth.AuthBase):
    """ Auth where you need to perform an arbitrary "login" to get a cookie.
    The expectation is that the args to this constructor can be used to
    perform a request that generates the required cookie(s) for a valid
    session. """

    content_type = 'application/json'
    OK_HTTP_CODES = 200, 201

    def __init__(self, url, method='POST', **kwargs):
        headers = {
            'content-type': self.content_type
        }
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        if 'data' in kwargs:
            kwargs['data'] = self.serializer(kwargs['data'])
        self.url = url
        self.method = method
        self.req_kwargs = kwargs
        self.login = None

    def __call__(self, request):
        if not self.login:
            self.login = requests.request(self.method, self.url,
                                          **self.req_kwargs)
        self.check_login_response()
        request.prepare_cookies(self.login.cookies)
        return request

    def check_login_response(self):
        if self.login.status_code not in self.OK_HTTP_CODES:
            raise Exception('login failed')

    def serializer(self, data):
        return json.dumps(data)
