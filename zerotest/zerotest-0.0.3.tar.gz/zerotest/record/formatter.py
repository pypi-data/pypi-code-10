import json

from zerotest.request import Request
from zerotest.response import Response

__author__ = 'Hari Jiang'


class Formatter(object):
    def write_record(self, writeable, request, response):
        record = dict(request=request.__dict__, response=response.__dict__)
        writeable.write(json.dumps(record, encoding='utf-8'))
        writeable.write("\n")

    def read_record(self, readable):
        line = readable.readline()
        if not line:
            return None
        record = json.loads(line, encoding='utf-8')
        request = Request()
        request.__dict__.update(record['request'])
        response = Response()
        response.__dict__.update(record['response'])
        return request, response
