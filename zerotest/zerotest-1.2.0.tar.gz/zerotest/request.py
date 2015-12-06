from __future__ import unicode_literals

import requests

from zerotest.utils.generator_helper import dict_to_param_style_code
from zerotest.utils.url_helper import urlparse
from zerotest.utils.encode_helper import ensure_unicode


class Request(object):
    def __init__(self, scheme=None, method=None, params=None, host=None, path=None, headers=None, data=None,
                 endpoint=None):
        self.scheme = scheme
        self.method = method
        self.headers = headers
        self.host = host
        self.path = path
        self.params = ensure_unicode(params)
        self.data = ensure_unicode(data)
        if endpoint:
            self.endpoint = endpoint

    @property
    def endpoint(self):
        return "{scheme}://{host}".format(**self.__dict__)

    @endpoint.setter
    def endpoint(self, endpoint):
        parsed = urlparse(endpoint)
        self.scheme = parsed.scheme
        if parsed.port:
            host = "{}:{}".format(parsed.hostname, parsed.port)
        else:
            host = parsed.hostname
        self.host = host

    @property
    def url(self):
        return "{}{}".format(self.endpoint, self.path)

    def send_request(self, verify=True):
        return requests.request(self.method, self.url, headers=self.headers,
                                params=self.params, data=self.data,
                                stream=True, allow_redirects=False, verify=verify)

    def __eq__(self, other):
        if type(other) != Request:
            return False

        return self.__dict__ == other.__dict__

    def __str__(self):
        return """[{method}]{url}
{headers}
{data}""".format(method=self.method, url=self.url, headers=self.headers, data=self.data)

    def __repr__(self):
        return '{}({})'.format(Request.__name__,
                               dict_to_param_style_code({k: v for k, v in self.__dict__.items() if v}))
