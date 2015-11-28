from __future__ import absolute_import, unicode_literals

import base64

from django.http import HttpResponse
from django.utils.encoding import force_bytes


class HttpResponseBasicChallenge(HttpResponse):
    status_code = 401

    def __init__(self, realm='Unknown'):
        super(HttpResponseBasicChallenge, self).__init__()
        self['WWW-Authenticate'] = 'Basic realm="%s"' % realm


def http_basic_credentials(request):
    """
    Strips the plaintext HTTP basic auth parameters out of the given request.
    Returns a bytestring tuple of (username, password)
    """
    try:
        # rfc2617 specifies the Authorization header only contains
        # 'Basic '+ base64 alphabet chars, which is a subset of utf-8
        auth_header = force_bytes(request.META['HTTP_AUTHORIZATION'])
    except KeyError:
        raise AttributeError("The request has no HTTP AUTH data")
    auth64 = auth_header.split(b'Basic ')[1]
    return base64.b64decode(auth64).split(b':', 1)
