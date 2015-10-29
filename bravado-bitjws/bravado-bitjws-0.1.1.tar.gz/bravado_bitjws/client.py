# -*- coding: utf-8 -*-
"""
The :class:`SwaggerClient` provides an interface for making API calls based on
a swagger spec, and returns responses of python objects which build from the
API response.

Structure Diagram::

        +---------------------+
        |                     |
        |    SwaggerClient    |
        |                     |
        +------+--------------+
               |
               |  has many
               |
        +------v--------------+
        |                     |
        |     Resource        +------------------+
        |                     |                  |
        +------+--------------+         has many |
               |                                 |
               |  has many                       |
               |                                 |
        +------v--------------+           +------v--------------+
        |                     |           |                     |
        |     Operation       |           |    SwaggerModel     |
        |                     |           |                     |
        +------+--------------+           +---------------------+
               |
               |  uses
               |
        +------v--------------+
        |                     |
        |     HttpClient      |
        |                     |
        +---------------------+


To get a client

.. code-block:: python

    client = bravado.client.SwaggerClient.from_url(swagger_spec_url)
"""
import bitjws
import urlparse

from bravado.client import SwaggerClient

from bravado_bitjws.requests_client import BitJWSRequestsClient



__all__ = ['BitJWSSwaggerClient']


class BitJWSSwaggerClient(SwaggerClient):
    """
    A client for accessing a Swagger-documented RESTful service,
    which also uses bitjws authentication.
    """

    def __init__(self, swagger_spec):
        """
        :param swagger_spec: :class:`bravado_core.spec.Spec`
        """
        super(BitJWSSwaggerClient, self).__init__(swagger_spec)

    @classmethod
    def from_url(cls, spec_url, http_client=None, privkey=None, **kwargs):
        """
        Build a :class:`SwaggerClient` from a url to the Swagger
        specification for a RESTful API.

        :param spec_url: url pointing at the swagger API specification
        :type spec_url: str
        :param http_client: an HTTP client used to perform requests
        :type  http_client: :class:`bravado.http_client.HttpClient`
        """
        if privkey is None:
            privkey = bitjws.PrivateKey()
        elif isinstance(privkey, str):
            privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(privkey))

        if http_client is None:
            host = urlparse.urlsplit(spec_url).hostname
            http_client = BitJWSRequestsClient()
            private_key = bitjws.privkey_to_wif(privkey.private_key)
            http_client.set_bitjws_key(host, private_key)
        return SwaggerClient.from_url(spec_url, http_client=http_client,
                                      **kwargs)

    @classmethod
    def from_spec(cls, spec_dict, origin_url=None, http_client=None,
                  privkey=None, **kwargs):
        """
        Build a :class:`SwaggerClient` from swagger api docs

        :param spec_dict: a dict with a Swagger spec in json-like form
        :param origin_url: the url used to retrieve the spec_dict
        :type  origin_url: str
        :param http_client: an HTTP client used to perform requests
        :type  http_client: :class:`bravado.http_client.HttpClient`
        :param str privkey: The WIF private key to use for bitjws signing
        """
        if privkey is None:
            privkey = bitjws.PrivateKey()
        elif isinstance(privkey, str):
            privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(privkey))

        if http_client is None:
            host = urlparse.urlsplit(origin_url).hostname
            http_client = BitJWSRequestsClient()
            private_key = bitjws.privkey_to_wif(privkey.private_key)
            http_client.set_bitjws_key(host, private_key)

        return SwaggerClient.from_spec(spec_dict, http_client=http_client,
                                       **kwargs)

