#!/usr/bin/env python
# coding=utf-8

import logging

#: logging handler
logger = logging.getLogger("pysuman")
redis_logger = logging.getLogger("pysuman.redis")


class ServiceException(Exception):
    pass


def wrapper_topic(topic):
    return "mq:" + topic
