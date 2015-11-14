__author__ = 'Hari Jiang'

import logging
from urlparse import urlparse

import werkzeug.wrappers

from zerotest.request import Request
from zerotest.response import Response
from zerotest.utils.http_helper import response_with_response

LOG = logging.getLogger(__name__)


class Forwarder(object):
    def __init__(self, forward_url):
        self._forward_url = forward_url
        self._on_forward_complete_callbacks = []

    def __call__(self, environ, start_response):
        # pop incorrect content length, I don't know why
        environ.pop('CONTENT_LENGTH', None)
        request = werkzeug.wrappers.Request(environ)

        headers = {k: v for k, v in request.headers if k not in ('Host',)}
        LOG.debug("forward to [%s]%s, headers: -----%s-----", request.method, self._forward_url, headers)
        forward_to = urlparse(self._forward_url)
        host = "{}:{}".format(forward_to.hostname, forward_to.port or 80)
        forward_request = Request(scheme=forward_to.scheme, method=request.method, headers=headers, data=request.data,
                                  params=request.query_string, path=request.path, host=host)
        response = forward_request.send_request()
        forward_response = Response.from_requests_response(response)
        self.trigger_on_forward_complete(forward_request, forward_response)
        return response_with_response(response, start_response)

    def on_forward_complete(self, callback):
        self._on_forward_complete_callbacks.append(callback)

    def trigger_on_forward_complete(self, request, response):
        for callback in self._on_forward_complete_callbacks:
            callback(request, response)
