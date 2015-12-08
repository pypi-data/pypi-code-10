#!/usr/bin/env python
# coding=utf-8

import functools
from collections import namedtuple

from .util import redis_logger, ServiceException, wrapper_topic


_Service = namedtuple("_Service", ["topic", "method"])


class Service(object):

    def __init__(self):
        self._services = {}

    def add(self, topic, method):
        redis_logger.info((topic, method))
        self._services[topic] = _Service(topic, method)

    def get_all_services(self):
        return self._services

    def get_service_by_topic(self, topic):
        if topic in self._services:
            return self._services[topic]

    def C(self, topic):

        topic = wrapper_topic(topic)
        if not topic:
            raise ServiceException("topic not empty")

        if topic in self._services:
            raise ServiceException("topic %s has watching" % topic)

        def _f(method):
            self.add(topic, method)

            @functools.wraps(method)
            def _wraps(*args, **kwargs):
                return method(*args, **kwargs)
            return _wraps
        return _f
