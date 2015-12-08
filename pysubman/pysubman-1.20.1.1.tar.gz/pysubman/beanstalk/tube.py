#!/usr/bin/env python
# coding=utf-8

import traceback


from .jobitem import decode as jobitem_decode
from .log import logger
from .producer import Producer
from .job import Job
from .constants import JobException, JOB_STATUS_ERROR


class Tube(object):
    def __init__(self, client, tube):
        self.tube = tube
        self.client = client
        self.connection = client.connection
        self.services = client.services

        self._set_watching_tube(self.tube)
        logger.info("All Watching Tube IN {}".format(tube))

    def _set_watching_tube(self, tube):
        if tube is None:
            tube = ["default"]
        if not isinstance(tube, list):
            tube = [tube]

        for tube_name in tube:
            if tube_name != "default":
                logger.info("watch list sum %d in %s" % (
                    self.connection.watch(tube_name), tube_name))

        if "default" not in tube:
            logger.info("watch list sum %d in %s" % (
                self.connection.ignore("default"), "default"))

    def _release_new_job(self, topic, status, retry, info):
        producer = Producer(self.client.address)
        producer.put_detail(self.tube, topic, status, retry, info)

    def run(self):
        while True:
            bjob = self.connection.reserve()
            job = Job(self.connection, bjob.jid, bjob.body, bjob.reserved)
            job.bury()
            self._run_job(job)

    def _run_job(self, job):
        try:
            jobitem = jobitem_decode(job.body)
        except JobException as e:
            logger.error(e)
            job.delete()
            return

        service = self.services.get_service_by_topic(jobitem.topic)
        if not service:
            job.release()
            return

        #: error and retry
        if (jobitem.status == JOB_STATUS_ERROR
                and jobitem.retry > service.retry_nums):
            logger.debug("Job %d retry over %d . Deleted" % (job.jid, service.retry_nums))
            job.delete()
            return

        try:
            service.method(jobitem.info)
        except:
            logger.error(traceback.format_exc())

            self._release_new_job(
                topic=jobitem.topic,
                status=JOB_STATUS_ERROR,
                retry=jobitem.retry + 1,
                info=jobitem.info)

        job.delete()
