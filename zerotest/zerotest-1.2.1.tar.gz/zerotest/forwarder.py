from __future__ import unicode_literals

import logging

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
        if not environ.get('CONTENT_LENGTH'):
            environ.pop('CONTENT_LENGTH', None)

        request = werkzeug.wrappers.Request(environ)

        headers = {k: v for k, v in request.headers if k not in ('Host',)}
        LOG.debug("forward to [%s]%s, headers: -----%s-----, data %s",
                  request.method, self._forward_url, headers, request.data)
        forward_request = Request(method=request.method, headers=headers, data=request.data,
                                  params=request.query_string, path=request.path, endpoint=self._forward_url)
        response = forward_request.send_request()
        forward_response = Response.from_requests_response(response)
        self.trigger_on_forward_complete(forward_request, forward_response)
        return response_with_response(response, start_response)

    def on_forward_complete(self, callback):
        self._on_forward_complete_callbacks.append(callback)

    def trigger_on_forward_complete(self, request, response):
        for callback in self._on_forward_complete_callbacks:
            callback(request, response)
