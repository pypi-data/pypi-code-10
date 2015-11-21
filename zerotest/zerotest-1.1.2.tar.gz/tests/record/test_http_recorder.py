import os
import tempfile

from zerotest.record.formatter import Formatter
from zerotest.record.http_recorder import HTTPRecorder
from zerotest.request import Request
from zerotest.response import Response


req = Request(scheme="http", method="get", params="query_string=here", host="example.com", path="/test",
              headers={"just": "header"}, data="request")
res = Response(status=200, headers={"responsed": "header"}, body="response")


def test_http_recorder():
    _, filepath = tempfile.mkstemp()
    formatter = Formatter()
    recorder = HTTPRecorder(filepath)
    try:
        recorder.start_service()
        recorder.record_http(req, res)
    finally:
        recorder.close()

    with open(filepath, 'r') as readable:
        request, response = formatter.read_record(readable)
        assert req.__dict__ == request.__dict__
        assert res.__dict__ == response.__dict__

    os.remove(filepath)
