# -*- coding: utf-8 -*-
#
#  DuedilApiClient v3 Pro + Credit
#  @copyright 2014 Christian Ledermann
#  @copyright 2015 Andrew Miller
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#
#

import hashlib
import six

from collections import OrderedDict


class Cache(object):
    """
    Basic in-memory cache implementation.

    The key-values are stored internally as a dictionary. An existing
    dictionary can be passed to the constructor to initialise.
    """

    _raw_dict = {}

    def __init__(self, raw_dict=None):
        if not raw_dict:
            self._raw_dict = {}
        else:
            self._raw_dict = raw_dict

    def _cache_key(self, key, url_params):
        cache_key = key
        if url_params:
            cache_key += six.text_type(OrderedDict(url_params))
        return hashlib.md5(six.b(key)).hexdigest()

    def get_url(self, url, url_params=None):
        """
        get the value in cache or None if URL doesn't match any

        :param url: The URL to query
        :return: the value in cache or None
        """
        cache_key = self._cache_key(url, url_params)
        return self._raw_dict.get(cache_key, None)

    def set_url(self, url, data, url_params=None):
        """
        Store the data for given URL in cache, override any previously present value

        :param url: The URL as key
        :param data: The value to store
        :return: Nothing
        """
        cache_key = self._cache_key(url, url_params)
        self._raw_dict[cache_key] = data


from dogpile.cache import make_region
import json

# from dogpile.cache.proxy import ProxyBackend
# from requests import Response
# from urlparse import urlsplit
#
# class HttpProxy(ProxyBackend):
#     def set(self, key, value):
#         # value should be a http response object
#         assert isinstance(value, Response)
#         value = value.json()
#         params = value.url
#         self.proxied.set(key, value)


def kwargs_key_generator(namespace, fn, **kw):
    fname = fn.__name__
    def generate_key(*args, **kwargs):
        args_str = "_".join(str(s) for s in args)
        kwargs_str = json.dumps(kwargs)
        key = '{}_{}:{}_{}'.format(namespace, fname, args_str, kwargs_str)
        hashkey = hashlib.md5(key.encode('utf-8'))
        return hashkey.hexdigest()
    return generate_key

dp_region = make_region(name='duedilv3', function_key_generator = kwargs_key_generator)


def configure_cache(backend='dogpile.cache.pylibmc', expiration_time=86400, **kwargs):
    if not kwargs:
        kwargs = {
            'url': ["127.0.0.1"],
        }
    return dp_region.configure(
        backend,
        expiration_time = expiration_time, # 1 day
        arguments = kwargs
    )
