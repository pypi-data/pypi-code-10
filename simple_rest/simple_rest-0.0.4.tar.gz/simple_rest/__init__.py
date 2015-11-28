#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import requests, re

http_methods = ['get', 'head', 'post', 'put', 'patch', 'delete']

class RequestStatusException(Exception):
    pass

class ForbiddenRequestException(Exception):
    pass

__endpoint_matcher__ = re.compile(r'\$[a-zA-Z_]+')

class Endpoint(object):
    def __init__(self, name, methods = {}, endpoints = {}):
        self.__name__    = name
        self.__methods__ = methods

        self.__endpoints__ = {}
        for key, value in endpoints.items():
            endpoint_name = key.replace('$', '')
            if isinstance(value, Endpoint):
                if not value.__name__.startswith(self.__name__):
                    value.__name__ = '%s/%s' (self.__name__, value.__name__)

                self.__endpoints__.update({ endpoint_name: value })
            elif isinstance(value, dict):
                self.__endpoints__.update({ endpoint_name: Endpoint('%s/%s' % (name, key), **value) })
            else:
                raise ValueError(str({ key: value }))

    def __str__(self):
        return self.__name__

    def __dir__(self):
        return list(self.__endpoints__.keys()) + list(self.__methods__.keys())

    def __contains__(self, name):
        return name in self.__endpoints__

    def __call__(self, argument):
        if '$' in self.__name__:
            new_name = __endpoint_matcher__.sub(argument, self.__name__)
            return Endpoint(new_name, self.__methods__, self.__endpoints__)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError as e:
            if name in self.__endpoints__:
                return self.__endpoints__.get(name)
            elif name in self.__methods__:
                base_method = getattr(requests, name)
                success_codes = self.__methods__.get(name)

                def method(**kwargs):
                    response = base_method(self.__name__, **kwargs)
                    if response.status_code not in success_codes:
                        raise RequestStatusException(response.status_code)

                return method
            elif name in http_methods:
                raise ForbiddenRequestException(name)

            raise e

class API(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if isinstance(value, Endpoint):
                self.__setattr__(name, value)
            elif isinstance(value, dict):
                self.__setattr__(name, Endpoint(name, **value))
            else:
                raise ValueError(str({ name: value }))

    def __contains__(self, name):
        return name in vars(self)

class Client(object):
    def __init__(self, host, api):
        self.__host__ = host
        self.api  = api

        def get_patched_method(name):
            def patched_method(endpoint, **kwargs):
                return requests.request(name, '%s/%s' % (self.__host__, endpoint), **kwargs)

            return patched_method

        requests.get = get_patched_method('get')
        requests.options = get_patched_method('options')
        requests.head = get_patched_method('head')
        requests.post = get_patched_method('post')
        requests.put = get_patched_method('put')
        requests.patch = get_patched_method('patch')
        requests.delete = get_patched_method('delete')

    def __str__(self):
        return self.__host__

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError as e:
            try:
                return object.__getattribute__(self.api, name)
            except AttributeError:
                raise e

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
