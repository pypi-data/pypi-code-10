from __future__ import unicode_literals

from zerotest.utils.generator_helper import dict_to_param_style_code


class Response(object):
    def __init__(self, status=None, headers=None, body=None):
        self.status = status
        self.headers = headers
        self.body = body

    @staticmethod
    def from_requests_response(response):
        res = Response(status=response.status_code, body=response.text,
                       headers=dict(response.headers))
        # make dict key/value to unicode
        import json
        res.__dict__ = json.loads(json.dumps(res.__dict__))
        return res

    def get_header(self, header):
        for k, v in self.headers.items():
            if k.upper() == header.upper():
                return v

    def __eq__(self, other):
        if type(other) != Response:
            return False

        return self.__dict__ == other.__dict__

    def __str__(self):
        return """{status}
{headers}
{body}""".format(**self.__dict__)

    def __repr__(self):
        return '{}({})'.format(Response.__name__, dict_to_param_style_code(self.__dict__))
