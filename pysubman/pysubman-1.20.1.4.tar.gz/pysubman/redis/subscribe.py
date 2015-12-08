#!/usr/bin/env python
# coding=utf-8

import redis
import signal
import sys
import threading
import time
import traceback

from .util import redis_logger
from .service import Service

#: threading exist
_Subscribe_Threads = []


def _thread_exit_handler(signum, frame):
    global _Subscribe_Threads

    print "Ctrl-C.... Exiting"
    redis_logger.info("receive a signal %d, is_exit = %d " % (signum, len(_Subscribe_Threads)))

    if not _Subscribe_Threads:
        sys.exit(0)

    for t in _Subscribe_Threads:
        t.alive = False

    _waiting_exit()
    sys.exit(0)

signal.signal(signal.SIGINT, _thread_exit_handler)


def _waiting_exit():
    global _Subscribe_Threads
    while len(_Subscribe_Threads) > 0:
        threads = []
        for k in _Subscribe_Threads:
            if k is not None and k.isAlive():
                k.join(1)
                threads.append(k)
        _Subscribe_Threads = threads


class Subscriber(object):
    def __init__(self, client):
        self.client = client

    def subscribe(self, service):
        global _Subscribe_Threads
        assert isinstance(service, Service)

        for topic, item in service.get_all_services().iteritems():
            listener = Listener(self.client, item)
            listener.start()
            _Subscribe_Threads.append(listener)

        #: waiting exit
        _waiting_exit()


class Listener(threading.Thread):

    def __init__(self, client, service):
        threading.Thread.__init__(self)
        self.client = client
        self.service = service
        self.alive = True

    def get_topic_count(self):
        return self.client.get_redis_client().llen(self.service.topic)

    def run(self):

        count = self.get_topic_count()
        if count:
            redis_logger.info("Topic %s is waiting to subscribe. remain %d topics" % (self.service.topic, count))

        while self.alive:

            #: rpop
            message = self.client.get_redis_client().brpop(self.service.topic, timeout=1)
            if message is None:
                time.sleep(1)
                continue

            #: running
            try:
                self.service.method(message[1], topic=message[0])
            except:
                traceback.print_exc()

        count = self.get_topic_count()
        if count:
            redis_logger.info("Topic %s not completed in list. remain %d topics" % (self.service.topic, count))
        return


class ListenerV2(threading.Thread):

    def __init__(self, client, service):
        threading.Thread.__init__(self)
        self.client = client
        self.service = service
        self.pubsub = self.client.get_redis_client().pubsub()
        self.alive = True

    def get_redis_client(self):
        return redis.StrictRedis(connection_pool=self.redis_pool)

    def run(self):
        #: handler extra topic
        self._handler_topic_in_list()

        #: subscribe
        self.pubsub.subscribe(self.service.topic)

        while self.alive:
            tube = self.pubsub.get_message()
            if tube is None:
                time.sleep(2)
                continue

            if tube["type"] == "subscribe":
                redis_logger.info("Topic `%s` has %d watcher" % (self.service.topic, tube["data"]))

            #: using type is message
            if tube["type"] != "message":
                continue

            #: running
            self.service.method(tube["data"])

    def _handler_topic_in_list(self):
        if not self.client.get_redis_client().llen(self.service.topic):
            return
        redis_logger.info("Topic %s has not handler in list" % self.service.topic)

        while True:

            #: is interrupt
            if not self.alive:
                count = self.client.get_redis_client().llen(self.service.topic)
                redis_logger.info("Topic %s not completed in list. remain %d topics" % (self.service.topic, count))
                return

            #: rpop
            message = self.client.get_redis_client().brpop(self.service.topic, timeout=1)
            if message is None:
                break

            self.service.method(message)
        redis_logger.info("Topic %s completed in list" % self.service.topic)
