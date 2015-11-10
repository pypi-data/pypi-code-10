""" Utilities for authenticating requests. """

import treq
from twisted.internet.defer import succeed, inlineCallbacks, returnValue
from zope.interface import implements, Interface


class IAuthenticator(Interface):
    """ Authenticator interface. """

    def owner_id(request):
        """ Retrieve an owner_id for a request.

        :type request:
            A Klein request object.
        :param request:
            The request to authenticate.

        :return:
            A deferred that fires with either an owner_id or None if the
            request could not be authenticated.
        """


class RequestHeaderAuth(object):

    implements(IAuthenticator)

    def owner_id(self, request):
        return succeed(request.getHeader('X-Owner-ID'))


class BouncerAuth(object):

    implements(IAuthenticator)

    def __init__(self, auth_bouncer_url):
        self._auth_bouncer_url = auth_bouncer_url.rstrip('/')

    @inlineCallbacks
    def owner_id(self, request):
        auth_headers = {}
        auth = request.getHeader('Authorization')
        if auth:
            auth_headers['Authorization'] = auth
        uri = "".join([self._auth_bouncer_url, request.path])
        resp = yield treq.get(uri, headers=auth_headers, persistent=False)
        yield resp.content()
        if resp.code >= 400:
            returnValue(None)
        x_owner_id = resp.headers.getRawHeaders('X-Owner-Id')
        if x_owner_id is None or len(x_owner_id) != 1:
            returnValue(None)
        returnValue(x_owner_id[0])
