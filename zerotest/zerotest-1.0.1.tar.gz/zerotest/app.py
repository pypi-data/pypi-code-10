
from werkzeug.serving import run_simple

from zerotest.forwarder import Forwarder
from zerotest.record.http_recorder import HTTPRecorder
from zerotest.common import DEBUG


class App(object):
    def __init__(self, forward_url, record_file_path):
        forwarder = Forwarder(forward_url)
        self.recorder = HTTPRecorder(record_file_path)
        forwarder.on_forward_complete(lambda req, res: self.recorder.record_http(req, res))
        self._app = forwarder

    def run(self, host, port):
        self.recorder.start_service()
        try:
            run_simple(host, port, self._app, use_debugger=DEBUG, use_reloader=DEBUG)
        finally:
            self.recorder.close()
