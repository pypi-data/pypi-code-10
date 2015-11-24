import unittest
import logging
import mox
import mock
from nose.tools import assert_equal
from stupeflix_api.connection import Connection
from stupeflix_api import httplib2


class ConnectionTests(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def disable_retries(self):
        self.orig_max_retries = Connection.MAX_NETWORK_RETRY
        Connection.MAX_NETWORK_RETRY = 1

    def restore_retries(self):
        Connection.MAX_NETWORK_RETRY = self.orig_max_retries 

    def test_request(self):
        self.disable_retries()

        # Setup mocks
        http = self.mox.CreateMock(httplib2.Http)
        http.request(u'http://my.site.com', 'GET', body=None,
                headers={'User-Agent': 'Basic Agent'},
                sendcallback=None).AndReturn(("headers", "content"))

        orig_http = httplib2.Http
        httplib2.Http = mock.Mock(return_value=http)

        # Test the request method
        self.mox.ReplayAll()
        connection = Connection("http://my.site.com/")
        ret = connection.request("foo")
        self.assertEqual(ret, {"body": "content", "headers": "headers"})

        # Verify mocks
        self.mox.VerifyAll()
        httplib2.Http = orig_http

        self.restore_retries()

    def test_request_raw(self):
        self.disable_retries()

        # Setup mocks
        http = self.mox.CreateMock(httplib2.Http)
        http.request('http://my.site.com/', 'GET', body=None, headers={},
                sendcallback=None).AndReturn(("headers", "content"))

        orig_http = httplib2.Http
        httplib2.Http = mock.Mock(return_value=http)

        # Test the request method
        self.mox.ReplayAll()
        connection = Connection("http://my.site.com/")
        ret = connection.request_raw()
        self.assertEqual(ret, {"body": "content", "headers": "headers"})

        # Verify mocks
        self.mox.VerifyAll()
        httplib2.Http = orig_http

        self.restore_retries()

    def test_request_errors(self):
        # Setup mocks
        http = self.mox.CreateMock(httplib2.Http)
        for i in range(Connection.MAX_NETWORK_RETRY):
            http.request(u'http://my.site.com', 'GET', body=None,
                    headers={'User-Agent': 'Basic Agent'},
                    sendcallback=None).AndRaise(httplib2.ServerNotFoundError)

        orig_http = httplib2.Http
        httplib2.Http = mock.Mock(return_value=http)

        logger = logging.getLogger("stupeflix_api.connection")
        handler = TestHandler()
        logger.addHandler(handler)

        # Test the request method
        self.mox.ReplayAll()
        connection = Connection("http://my.site.com/")
        self.assertRaises(httplib2.ServerNotFoundError, 
                connection.request, "foo")
        handler.assert_handled_count(4)

        # Verify mocks
        self.mox.VerifyAll()
        httplib2.Http = orig_http


class TestHandler(logging.Handler):

    def __init__(self, *args, **kwargs):
        super(TestHandler, self).__init__(*args, **kwargs)
        self.recorder = mock.Mock()

    def emit(self, record):
        self.recorder(record)

    def assert_handled_count(self, num_times):
        assert_equal(self.recorder.call_count, num_times)
