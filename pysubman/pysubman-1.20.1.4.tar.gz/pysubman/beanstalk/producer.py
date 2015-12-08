#!/usr/bin/env python
# coding=utf-8

from .connection import Connection
from .jobitem import format as jobitem_format
from .jobitem import encode as jobitem_encode
from .jobitem import JobItem
from .constants import DEFAULT_ADDRESS, JOB_STATUS_UNTREATED
from .log import logger


class Producer(object):
    def __init__(self, address=DEFAULT_ADDRESS):
        self.address = address

    def put(self, obj, *args):
        info = jobitem_format(obj, *args)
        return self.put_detail(obj.Tube, obj.Topic, JOB_STATUS_UNTREATED, 0, info)

    def put_detail(self, tube, topic, status, retry, info):
        self.connection = Connection(self.address)
        self.connection.use(tube)

        job_detail = jobitem_encode(JobItem(topic=topic, status=status, retry=retry, info=info))
        logger.debug(job_detail)
        return self.connection.put(job_detail)

    def __del__(self):
        self.connection.close()
