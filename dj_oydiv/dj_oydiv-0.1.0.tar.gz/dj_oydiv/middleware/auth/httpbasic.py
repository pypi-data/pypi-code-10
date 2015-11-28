from __future__ import absolute_import, unicode_literals

from django.contrib.auth import authenticate

from ...auth.basic import (
    HttpResponseBasicChallenge,
    http_basic_credentials
)


class HTTPBasicMiddleWare(object):
    """This middleware checks the incoming request for a valid user/password
    combination. The request is rejected with 403 Forbidden if a valid user
    cannot be authenticated against the User db
    """
    def process_request(self, request):
        try:
            username, password = http_basic_credentials(request)
        except AttributeError:
            return HttpResponseBasicChallenge()

        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponseBasicChallenge()
        try:
            request.user.vidyoadmin.decrypt(password)
        except ValueError:
            raise Exception('user / vidyoadmin decryption mismatch')
