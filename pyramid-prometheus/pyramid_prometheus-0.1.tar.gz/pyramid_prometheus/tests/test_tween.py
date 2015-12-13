import sys

try:
    from unitest import mock
except ImportError:
    import mock
import pytest
from pyramid import testing, urldispatch

import pyramid_prometheus

class LoggingHandler:

    def __init__(self):
        self.requests = []

    def __call__(self, request):
        self.requests.append(request)
        return request.response

@pytest.fixture
def handler():
    return LoggingHandler()

@pytest.fixture
def config(request):
    config = testing.setUp()
    return config

@mock.patch('pyramid_prometheus.start_http_server')
def test_includeme(start_http_server, config):
    pyramid_prometheus.includeme(config)
    assert not start_http_server.called

@mock.patch('pyramid_prometheus.start_http_server')
def test_includeme_with_port(start_http_server, config):
    config.registry.settings['prometheus.port'] = '9105'
    pyramid_prometheus.includeme(config)
    start_http_server.assert_called_once_with(9105)

def test_tween(config, handler):
    tween = pyramid_prometheus.tween_factory(handler, config.registry)
    req = testing.DummyRequest()
    req.matched_route = None
    got_resp = tween(req)
    assert got_resp == req.response

def test_tween_with_route(config, handler):
    tween = pyramid_prometheus.tween_factory(handler, config.registry)
    req = testing.DummyRequest()
    route = urldispatch.Route('index_page', '/pattern')
    req.matched_route = route
    got_resp = tween(req)
    assert got_resp == req.response
