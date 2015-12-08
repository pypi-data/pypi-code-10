#!/usr/bin/env python
# coding=utf-8

import redis

from .util import wrapper_topic


def _create_redis_pool(source):
    host, port, db = source.split(":")
    port = int(port)
    db = int(db)

    return redis.ConnectionPool(host=host, port=port, db=db)


class Client(object):

    def __init__(self, host):
        self.host = host
        self.redis_pool = _create_redis_pool(host)

    def get_redis_client(self):
        return redis.StrictRedis(connection_pool=self.redis_pool)

    def publish(self, topic, message):
        return self.get_redis_client().lpush(wrapper_topic(topic), message)

    def publishv2(self, topic, message):
        sub_count = self.get_redis_client().publish(wrapper_topic(topic), message)
        if sub_count == 0:
            self.get_redis_client().lpush(wrapper_topic(topic), message)
            return 1
        return sub_count
