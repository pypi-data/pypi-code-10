#!/usr/bin/env python
# coding=utf-8

__version__ = "1.10.6"

import beanstalkd
import json
import logging
import functools
import traceback
from collections import namedtuple

_logger = logging.getLogger("pysubman")

__all__ = ["Consumer", "Producer", "Service", "format"]
DEFAULT_PRIORITY = 2 ** 31
DEFAULT_ADDRESS = 'localhost:11300'


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
                raise SubmanServiceException("topic %s has watching" % topic)

        def _f(method):

            #: topic verify
            for topic in topics:
                self.add(topic, method, is_retry, retry_nums)

            @functools.wraps(method)
            def _wraps(*args, **kwargs):
                return method(*args, **kwargs)
            return _wraps
        return _f


def format(obj, *args):
    info = {}
    for index, k in enumerate(obj.Info):
        info[k[0]] = k[1] % (args[index])
    return info


class Producer(object):
    def __init__(self, address=DEFAULT_ADDRESS):
        self.address = address

    def put(self, obj, *args):
        info = format(obj, *args)
        return self.put_detail(obj.Tube, obj.Topic, JOB_STATUS_UNTREATED, 0, info)

    def put_detail(self, tube, topic, status, retry, info):
        self.connection = beanstalkd.Connection(self.address)
        self.connection.use(tube)

        job_detail = encode_job(topic, status, retry, info)
        _logger.debug(job_detail)
        return self.connection.put(job_detail)

    def __del__(self):
        self.connection.close()


class Consumer(object):
    def __init__(self, address=DEFAULT_ADDRESS):
        self.address = address
        self.connection = beanstalkd.Connection(self.address)

    def tube(self, tube):
        return _Tube(self, tube)


class _Tube(object):
    def __init__(self, client, tube):
        self.tube = tube
        self.client = client
        self.connection = client.connection

        self._set_watching_tubes(self.tube)
        _logger.info("All Watching Tube IN {}".format(tube))

    def _set_watching_tubes(self, tubes):
        if tubes is None:
            tubes = ["default"]
        if not isinstance(tubes, list):
            tubes = [tubes]

        for tube_name in tubes:
            if tube_name != "default":
                _logger.info("watch list sum %d in %s" % (
                    tube_name, self.connection.watch(tube_name)))

        if "default" not in tubes:
            _logger.info("watch list sum %d in %s" % (
                "default", self.connection.ignore("default")))

    def _release_new_job(self, topic, status, retry, info):
        producer = Producer(self.client.beanstalkd_host)
        producer.put_detail(self.tube, topic, status, retry, info)

    def run(self, services):
        if (services is None or not isinstance(services, Service)):
            raise SubmanConsumerException("services not empty")
        if not services.get_all_services():
            raise SubmanConsumerException("services not empty")

        while True:
            job = self.connection.reserve()
            job.bury()

            try:
                job_item = decode_job(job.body)
            except SubmanJobException as e:
                _logger.error(e)
                job.delete()
                continue

            service = services.get_service_by_topic(job_item.topic)
            if not service:
                job.release()
                continue

            #: error and retry
            if (job_item.status == JOB_STATUS_ERROR
                    and job_item.retry > service.retry_nums):
                _logger.debug("Job %d retry over %d . Deleted" % (job.jid, service.retry_nums))
                job.delete()
                continue

            try:
                service.method(job_item.info)
            except:
                _logger.error(traceback.format_exc())

                self._release_new_job(
                    topic=job_item.topic,
                    status=JOB_STATUS_ERROR,
                    retry=job.item.retry + 1,
                    info=job_item.info)

            job.delete()
