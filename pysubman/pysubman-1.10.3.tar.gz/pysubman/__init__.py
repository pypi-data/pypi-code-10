#!/usr/bin/env python
# coding=utf-8

__version__ = "1.10.3"

import beanstalkc
import json
import logging
import functools
import traceback
from collections import namedtuple

_logger = logging.getLogger("pysubman")

__all__ = ["Consumer", "Producer", "Service", "format"]
DEFAULT_PRIORITY = 2 ** 31


class SubmanConsumerException(Exception):
    pass


class SubmanJobException(Exception):
    pass


class SubmanServiceException(Exception):
    pass


JOB_STATUS_UNTREATED = 0
JOB_STATUS_ERROR = 100
JOB_STATUS_SUCCESS = 10
_JobItem = namedtuple("_JobItem", ["topic", "status", "retry", "info"])
_Service = namedtuple("_Service", ["topic", "method", "is_retry", "retry_nums"])


def encode_job(topic, status, retry, info):
    return json.dumps(dict(
        topic=topic,
        status=status,
        retry=retry,
        info=info
    ))


def decode_job(body):
    try:
        body_r = json.loads(body)
        return _JobItem(
            topic=body_r["topic"],
            status=body_r["status"],
            retry=body_r["retry"],
            info=body_r["info"]
        )
    except ValueError:
        raise SubmanJobException("body format error >>> '{}'".format(body))


class _Job(object):
    def __init__(self, job):
        self.job = job

    @property
    def jid(self):
        return self.job.jid

    def decode(self):
        self.item = decode_job(self.job.body)

    def consume(self, handler):
        self.bury()
        return handler(self.item.info)

    def bury(self):
        self.job.bury()

    def delete(self):
        self.job.delete()

    def release(self):
        self.job.release()


class Service(object):

    def __init__(self):
        self._services = {}

    def add(self, topic, method, is_retry, retry_nums):
        _logger.info((topic, method, is_retry, retry_nums))
        self._services[topic] = _Service(topic, method, is_retry, retry_nums)

    def get_all_services(self):
        return self._services

    def get_service_by_topic(self, topic):
        if topic in self._services:
            return self._services[topic]

    def C(self, topics, is_retry=True, retry_nums=3):

        if not topics:
            raise SubmanServiceException("topic not empty")

        if not isinstance(topics, list):
            topics = [topics]

        for topic in topics:
            if topic in self._services:
                raise SubmanServiceException("topic ({}) has watching".format(topic))

        def _f(method):

            #: topic verify
            for topic in topics:
                self.add(topic, method, is_retry, retry_nums)

            @functools.wraps(method)
            def _wraps(*args, **kwargs):
                return method(*args, **kwargs)
            return _wraps
        return _f


class _Connection(object):
    def __init__(self, beanstalkd_host):
        self.connection = self._get_connection(beanstalkd_host)

    def _get_connection(self, beanstalkd_host):
        beanstalkd_list = beanstalkd_host.split(":")
        beanstalkd_host = beanstalkd_list[0]
        beanstalkd_port = 11300
        if len(beanstalkd_list) > 1:
            beanstalkd_port = int(beanstalkd_list[1])

        return beanstalkc.Connection(beanstalkd_host, beanstalkd_port)

    def use(self, tube):
        return self.connection.use(tube)

    def put(self, body, priority=DEFAULT_PRIORITY, delay=0):
        return self.connection.put(body, priority=priority, delay=delay)

    def watch(self, name):
        return self.connection.watch(name)

    def ignore(self, name):
        return self.connection.ignore(name)

    def reserve(self, timeout=None):
        return self.connection.reserve(timeout)


def format(obj, *args):
    info = {}
    for index, k in enumerate(obj.Info):
        info[k[0]] = k[1] % (args[index])
    return info


class Producer(object):
    def __init__(self, beanstalkd_host="localhost:11300"):
        self.beanstalkd_host = beanstalkd_host

    def put(self, obj, *args):
        info = format(obj, *args)
        self.put_detail(obj.Tube, obj.Topic, JOB_STATUS_UNTREATED, 0, info)

    def put_detail(self, tube, topic, status, retry, info):
        self.connection = _Connection(self.beanstalkd_host)
        self.connection.use(tube)
        job_detail = encode_job(topic, status, retry, info)
        _logger.debug(job_detail)

        self.connection.put(job_detail)

    def __del__(self):
        self.connection.close()


class Consumer(object):
    def __init__(self, beanstalkd_host="localhost:11300", services=None):
        if (services is None
                or not isinstance(services, Service)):
            raise SubmanConsumerException("params: services not empty")
        self.services = services
        if not self.services.get_all_services():
            raise SubmanConsumerException("params: services not empty")

        self.beanstalkd_host = beanstalkd_host
        self.connection = _Connection(self.beanstalkd_host)

    def tube(self, tube):
        return _Tube(tube, self)


class _Tube(object):
    def __init__(self, tube, client):
        self.tube = tube
        self.client = client
        self.connection = client.connection
        self.services = client.services

        self._set_watching_tubes(self.tube)
        _logger.info("All Watching Tube IN {}".format(tube))

    def _set_watching_tubes(self, tubes):
        if tubes is None:
            tubes = ["default"]
        if not isinstance(tubes, list):
            tubes = [tubes]

        for tube_name in tubes:
            if tube_name != "default":
                self.connection.watch(tube_name)
        if "default" not in tubes:
            self.connection.ignore("default")

    def _release_new_job(self, topic, status, retry, info):
        producer = Producer(self.client.beanstalkd_host)
        producer.put_detail(self.tube, topic, status, retry, info)

    def run(self):

        while True:
            job = _Job(self.connection.reserve())
            job.bury()

            try:
                job.decode()
            except SubmanJobException as e:
                _logger.error(e)
                job.delete()
                continue

            service = self.services.get_service_by_topic(job.item.topic)
            if not service:
                job.release()
                continue

            if (job.item.status == JOB_STATUS_ERROR
                    and job.item.retry > service.retry_nums):
                _logger.debug("Job {} retry over {} . Delete".format(job.jid, service.retry_nums))
                job.delete()
                continue

            try:

                job.consume(service.method)
            except:
                _logger.error(traceback.format_exc())
                self._release_new_job(
                    topic=job.item.topic,
                    status=JOB_STATUS_ERROR,
                    retry=job.item.retry + 1,
                    info=job.item.info)

            job.delete()
