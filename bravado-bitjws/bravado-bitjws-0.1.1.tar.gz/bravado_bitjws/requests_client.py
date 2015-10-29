# -*- coding: utf-8 -*-
"""
Wrappers for the bravado.requests_client classes.
"""

import bitjws
import json
import requests
import requests.auth
import time
from bravado.requests_client import (Authenticator, RequestsClient,
                                     RequestsResponseAdapter,
                                     RequestsFutureAdapter)

from bravado.http_future import HttpFuture

__all__ = ['BitJWSRequestsClient', 'BitJWSAuthenticator',
           'BitJWSRequestsResponseAdapter']


class BitJWSAuthenticator(Authenticator):
    """BitJWS authenticator uses JWS and the CUSTOM-BITCOIN-SIGN algorithm.

    :param host: Host to authenticate for.
    :param privkey: Private key as a WIF string
    """

    def __init__(self, host, privkey):
        super(BitJWSAuthenticator, self).__init__(host)
        self.privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(privkey))

    def apply(self, request):
        if len(request.data) > 0:
            data = bitjws.sign_serialize(self.privkey, requrl=request.url,
                                         iat=time.time(),
                                         data=json.loads(request.data))
        else:
            data = bitjws.sign_serialize(self.privkey, requrl=request.url,
                                         iat=time.time(),
                                         data=request.params)
        request.params = {}
        request.data = data
        request.headers['content-type'] = 'application/jose'
        return request


class BitJWSRequestsClient(RequestsClient):
    """Synchronous HTTP client implementation.
    """

    def __init__(self):
        super(BitJWSRequestsClient, self).__init__()
        self.session = requests.Session()
        self.authenticator = None

    def request(self, request_params, response_callback=None):
        """
        :param request_params: complete request data.
        :type request_params: dict
        :param response_callback: Function to be called on the response
        :returns: HTTP Future object
        :rtype: :class: `bravado_core.http_future.HttpFuture`
        """
        sanitized_params, misc_options = self.separate_params(request_params)
        requests_future = RequestsFutureAdapter(
            self.session,
            self.authenticated_request(sanitized_params),
            misc_options)

        return HttpFuture(
            requests_future,
            BitJWSRequestsResponseAdapter,
            response_callback,
        )

    def set_bitjws_key(self, host, privkey):
        """
        :param host: The host to authenticate for.
        :param privkey: This client's private key to sign with.
        """
        self.authenticator = BitJWSAuthenticator(host=host, privkey=privkey)


class BitJWSRequestsResponseAdapter(RequestsResponseAdapter):
    """Wraps a requests.models.Response object to provide a uniform interface
    to the response innards.
    """

    def json(self, **kwargs):
        jso = {}
        if 'content-type' in self._delegate.headers and \
                'application/jose' in self._delegate.headers['content-type']:
            rawtext = self.text.decode('utf8')
            headers, jwtpayload = \
                    bitjws.validate_deserialize(rawtext, requrl='/response')
            if headers is None:
                raise bitjws.jws.InvalidPayload("Response failed validation")
            if 'data' in jwtpayload:
                jso = jwtpayload['data']
            else:
                jso = jwtpayload
        else:
            jso = self._delegate.json(**kwargs)
        return jso

