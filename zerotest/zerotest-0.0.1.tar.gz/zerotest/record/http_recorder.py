__author__ = 'Hari Jiang'

from Queue import Queue, Empty
import threading
import logging

from zerotest.record.formatter import Formatter

LOG = logging.getLogger(__name__)


class HTTPRecorder(object):
    """
    format and record tunnel request/response to file
    """

    def __init__(self, filepath):
        """
        :param filepath: new record will append to file if filepath exists
        :return:
        """
        self.filepath = filepath
        self._running = False
        self._closing = False
        self._service_thread = None
        self._queue = Queue()
        self._formatter = Formatter()

    def start_service(self):
        """
        start recorder service
        :return:
        """
        self._service_thread = threading.Thread(target=self._loop_work)
        self._running = True
        LOG.info("recorder service start, store http record to '{}'".format(self.filepath))
        self._service_thread.start()

    def _loop_work(self):
        record_file = open(self.filepath, "a+b")
        while True:
            task = self._queue.get()
            LOG.debug("receive task %s", task)
            if task is None:
                record_file.close()
                return

            self._formatter.write_record(record_file, task[0], task[1])

    def record_http(self, request, response):
        """
        async method, put request, response into task queue
        :return:
        """
        if not self._closing:
            LOG.debug("record http %s, %s", request, response)
            self._queue.put((request, response))

    def close(self):
        """
        graceful close, wait util queue empty
        :return:
        """
        if self._running:
            LOG.debug("closing...")
            self._closing = True
            self._queue.put(None)
            LOG.debug("wait task complete...")
            self._service_thread.join()
        else:
            raise RuntimeError("current service is not running")

        LOG.info("closed, record file: '{}'".format(self.filepath))

    def shutdown(self):
        """
        shutdown service, threw out items already in queue
        :return:
        """
        LOG.debug("shutdown...")
        self._closing = True
        try:
            while True:
                self._queue.get_nowait()
        except Empty:
            pass

        self.close()
