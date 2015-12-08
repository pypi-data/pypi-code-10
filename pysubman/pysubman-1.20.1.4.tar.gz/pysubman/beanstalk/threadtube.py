#!/usr/bin/env python
# coding=utf-8

import Queue
import signal
import traceback
import threading

from .jobitem import decode as jobitem_decode
from .log import logger
from .producer import Producer
from .job import Job
from .constants import JobException, JOB_STATUS_ERROR
from .connection import Connection

_Thread_Exit = False


def _thread_exit_handler(signum, frame):
    global _Thread_Exit
    _Thread_Exit = True
    logger.info("receive a signal %d, is_exit = %d " % (signum, _Thread_Exit))

signal.signal(signal.SIGINT, _thread_exit_handler)


class ThreadTube(object):
    def __init__(self, client, tube):
        self.tube = tube
        self.client = client
        self.connection = client.connection
        self.services = client.services

        self._set_watching_tube(self.tube)
        logger.info("All Watching Tube IN {}".format(tube))

        self.t_queue = Queue.Queue(maxsize=4)

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

    def _set_work_pool(self, thread_tubes, maxsize):
        for i in xrange(maxsize):
            t = _Worker(self.tube, self.client.address, self.t_queue, self.services)
            t.start()
            thread_tubes.append(t)

    def run(self):

        thread_tubes = []
        self._set_work_pool(thread_tubes, 4)

        while True:
            if not _Thread_Exit:
                bjob = self.connection.reserve()
                bjob.bury(self.connection)

                self.t_queue.put(bjob)
            else:
                break

        #: exit
        logger.info("get all bury job")
        logger.info("get queue numbers")

        self._wait_thread_completed(thread_tubes)
        logger.info("all threading is stop")

        logger.info("kick all buried jobs")
        self._kick_all_bury_jobs()

    def _kick_all_bury_jobs(self):
        stats_tube = self.connection.stats_tube(self.tube)
        buried_job_nums = stats_tube["current-jobs-buried"]
        if not buried_job_nums:
            buried_job_nums = 10
        result = self.connection.kick()
        logger.info(result)

    def _wait_thread_completed(self, thread_tubes):
        while True:
            if not filter(lambda k: k.is_alive(), thread_tubes):
                return


class _Worker(threading.Thread):
    def __init__(self, tube, address, queue, services):
        threading.Thread.__init__(self)
        self._tube = tube
        self._address = address
        self._queue = queue
        self._services = services

        self.connect()

    def connect(self):
        self._connection = Connection(address=self._address)

    def _release_new_job(self, topic, status, retry, info):
        producer = Producer(self._address)
        producer.put_detail(self._tube, topic, status, retry, info)

    def run(self):
        while True:
            if not _Thread_Exit:
                bjob = self._queue.get()
                job = Job(self._connection, bjob.jid, bjob.body, bjob.reserved)
                self._run_job(job)
                self._queue.task_done()

            else:
                logger.info("receive a signal to exit, thread[%s] stop" % self.getName())
                break

    def _run_job(self, job):
        try:
            jobitem = jobitem_decode(job.body)
        except JobException as e:
            logger.error(e)
            job.delete()
            return

        service = self._services.get_service_by_topic(jobitem.topic)
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
