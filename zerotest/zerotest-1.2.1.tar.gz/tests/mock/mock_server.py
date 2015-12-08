# coding=utf8
from __future__ import unicode_literals

"""
Mocked API server
"""
import threading
import time
import json
import requests
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from tests.mock import pickup_port
from zerotest.utils.generator_helper import get_name_from_request
from zerotest.utils.url_helper import urljoin


class Server(object):
    def __init__(self):
        self.count = 0
        self.host = None
        self.port = None
        self.thread = None
        self.running = False

    def dispatch_request(self, request):
        handler = getattr(self, get_name_from_request(request), None)
        if handler:
            return handler(request)
        else:
            return Response("non route", status=404)

    def get_count(self, request):
        return Response(json.dumps(dict(count=self.count)),
                        content_type='application/json; charset=utf-8')

    def post_echo(self, request):
        return Response(request.data,
                        content_type=request.headers['content_type'])

    def post_raw_to_json(self, request):
        data = request.data
        return Response(data,
                        content_type='application/json')

    def get_chinese_hello_world(self, request):
        return Response(json.dumps(dict(count=self.count, content="你好,世界")),
                        content_type='application/json; charset=utf-8')

    def delete_shutdown_server(self, request):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return Response("shutdown")

    def __call__(self, environ, start_response):
        request = Request(environ)
        self.count += 1
        environ['HTTP_COUNT'] = self.count
        return self.dispatch_request(request)(environ, start_response)

    def start(self, host, port):
        self.host = host
        self.port = port
        self.running = True
        run_simple(host, port, self)

    @property
    def url(self):
        return 'http://{}:{}'.format(self.host, self.port)

    def start_daemon(self, host, port):
        self.thread = threading.Thread(target=lambda: self.start(host, port))
        self.thread.start()

    def shutdown(self):
        if self.running:
            requests.delete(urljoin(self.url, 'shutdown_server'))
            self.running = False
            self.thread.join(30)

    def start_mock_server(self):
        port = pickup_port()
        self.start_daemon('127.0.0.1', port)
        test_count = 10
        while test_count > 0:
            try:
                if self.running:
                    r = requests.get(urljoin(self.url, '/count'))
                    if r.status_code == 200:
                        return

                    print("wait server start, response", r.status_code, r.text)
            except requests.exceptions.ConnectionError:
                pass

            time.sleep(1)
            test_count -= 1
        else:
            self.shutdown()
            raise RuntimeError("start mock server timeout")
