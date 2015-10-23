"""
WebPortfolio RQ Worker

A simple RQ manager to interact with a connected RQ worker and job

requirements:

rq==0.5.3

It has only on Q name: default

"""

import functools
import redis
from rq import Worker, Queue, Connection

class RQ_Worker(object):

    def __init__(self, uri=None, name="default", ttl=600, result_ttl=3600):
        self.name = name
        self.ttl = ttl
        self.result_ttl = result_ttl

        if uri:
            self.conn = redis.StrictRedis.from_url(url=uri)
            self.q = Queue(name=self.name, connection=self.conn)

    def init_app(self, app):
        uri = app.config.get("RQ_WORKER_URI")
        name = app.config.get("RQ_WORKER_URI", "default")
        ttl = app.config.get("RQ_WORKER_TTL", 600)
        result_ttl = app.config.get("RQ_WORKER_RESULT_TTL")
        self.__init__(uri=uri, name=name, ttl=ttl, result_ttl=result_ttl)

    def add_job(self, f, *args, **kwargs):
        """
        Enqueue a function to be executed
        :param f: the function to call
        :param args:
        :param kwargs:
        :return object: the job instance including the id

        :example:
        def my_job(args):
            pass

        rq_worker.add(my_job, args)
        """

        if "result_ttl" not in kwargs:
            kwargs["result_ttl"] = self.result_ttl
        if "ttl" not in kwargs:
            kwargs["ttl"] = self.ttl
        return self.q.enqueue(f, *args, **kwargs)

    def get_job(self, job_id):
        """
        Return a job by id
        :param job_id:
        :return Job:

        useful properties:
            is_finished
            is_failed
            is_started
            is_queued
            result

        useful methods:
            get_status()
        """
        return self.q.fetch_job(job_id)

    def job(self, f):
        """
        A decorator to add to function, to automatically enqueue
        :return:

        :example:

        @rq_worker.job
        def my_job(args):
            pass

        """
        @functools.wraps(f)
        def delay(*args, **kwargs):
            return self.add_job(f, *args, **kwargs)
        return delay

    def run(self):
        """
        This function run the worker in the background
        This function may need to be Supervised so it stays up
        :return:
        """
        listen = [self.name]
        with Connection(self.conn):
            worker = Worker(list(map(Queue, listen)))
            worker.work()

    def clear(self):
        """
        To empty out all queue
        :return:
        """
        c = self.q.count
        self.q.empty()


