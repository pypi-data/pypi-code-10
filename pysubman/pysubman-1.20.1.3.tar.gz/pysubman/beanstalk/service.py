#!/usr/bin/env python
# coding=utf-8

import functools
from collections import namedtuple
from .log import logger


_Service = namedtuple("_Service", ["topic", "method", "is_retry", "retry_nums"])


class ServiceException(Exception):
    pass


class Service(object):

    def __init__(self):
        self._services = {}

    def add(self, topic, method, is_retry, retry_nums):
        logger.info((topic, method, is_retry, retry_nums))
        self._services[topic] = _Service(topic, method, is_retry, retry_nums)

    def get_all_services(self):
        return self._services

    def get_service_by_topic(self, topic):
        if topic in self._services:
            return self._services[topic]

    def C(self, topics, is_retry=True, retry_nums=3):

        if not topics:
            raise ServiceException("topic not empty")

        if not isinstance(topics, list):
            topics = [topics]

        for topic in topics:
            if topic in self._services:
                raise ServiceException("topic %s has watching" % topic)

        def _f(method):

            #: topic verify
            for topic in topics:
                self.add(topic, method, is_retry, retry_nums)

            @functools.wraps(method)
            def _wraps(*args, **kwargs):
                return method(*args, **kwargs)
            return _wraps
        return _f
