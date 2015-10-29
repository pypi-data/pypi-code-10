import sys
import traceback
import unittest
import httpretty
import pushalot.exc
from pushalot.transport import (
    API_URL,
    HTTPTransport,
)

class TestHTTPTransport(unittest.TestCase):

    @httpretty.activate
    def test_raises_exception_if_wrong_json_returned(self):
        with self.assertRaises(pushalot.exc.PushalotException):
            httpretty.register_uri(
                httpretty.POST,
                API_URL,
                body='Whatever..'
            )
            transport = HTTPTransport()
            result = transport.send(
                Title='Test',
            )

    @unittest.skipIf(sys.version_info[0] > 2, 'Not required in python3')
    @httpretty.activate
    def test_uncaught_exception_keeps_stacktrace(self):
        try:
            httpretty.register_uri(
                httpretty.POST,
                API_URL,
                body='Whatever..'
            )
            transport = HTTPTransport()
            result = transport.send(
                Title='Test',
            )
        except (pushalot.exc.PushalotException) as e:
            ex_type, ex, tb = sys.exc_info()
            trace = traceback.format_exc(tb)
            del tb
            self.assertTrue('raise ValueError("No JSON object could be decoded")' in trace)

    @httpretty.activate
    def test_success_send(self):
        httpretty.register_uri(
            httpretty.POST,
            API_URL,
            body='{"Success":true}'
        )
        transport = HTTPTransport()
        result = transport.send(
            AuthroizationToken='some-token',
            Title='Title',
            Body='Test body'
        )
        self.assertTrue(result)

    @httpretty.activate
    def test_raises_exception_on_200_code_with_false_in_result(self):
        with self.assertRaises(pushalot.exc.PushalotException):
            httpretty.register_uri(
                httpretty.POST,
                API_URL,
                body='{'
                     '"Success":false,'
                     '"Description":"The request has been completed successfully."'
                     '}'
            )
            transport = HTTPTransport()
            result = transport.send(
                AuthroizationToken='some-token',
                Title='Title',
                Body='Test body'
            )

    @httpretty.activate
    def test_raises_badrequestexception_on_400_code(self):
        with self.assertRaises(pushalot.exc.PushalotBadRequestException):
            httpretty.register_uri(
                httpretty.POST,
                API_URL,
                body='{"Description": "Whatever.."}',
                status=400
            )
            transport = HTTPTransport()
            result = transport.send(
                Title='Test',
            )

    @httpretty.activate
    def test_raises_notacceptableexception_on_406_code(self):
        with self.assertRaises(pushalot.exc.PushalotNotAcceptableException):
            httpretty.register_uri(
                httpretty.POST,
                API_URL,
                body='{"Description": "Whatever.."}',
                status=406
            )
            transport = HTTPTransport()
            result = transport.send(Title='Test')

    @httpretty.activate
    def test_raises_goneexception_on_410_code(self):
        with self.assertRaises(pushalot.exc.PushalotGoneException):
            httpretty.register_uri(
                httpretty.POST,
                API_URL,
                body='{"Description": "Whatever.."}',
                status=410
            )
            transport = HTTPTransport()
            result = transport.send(Title='Test')

    @httpretty.activate
    def test_raises_internalerrorexception_on_500_code(self):
        with self.assertRaises(pushalot.exc.PushalotInternalErrorException):
            httpretty.register_uri(
                httpretty.POST,
                API_URL,
                body='{"Description": "Whatever.."}',
                status=500
            )
            transport = HTTPTransport()
            result = transport.send(Title='Test')

    @httpretty.activate
    def test_raises_unavailableexception_on_503_code(self):
        with self.assertRaises(pushalot.exc.PushalotUnavailableException):
            httpretty.register_uri(
                httpretty.POST,
                API_URL,
                body='{"Description": "Whatever.."}',
                status=503
            )
            transport = HTTPTransport()
            result = transport.send(Title='Test')

    @httpretty.activate
    def test_raises_on_unkown_http_code_returned(self):
        with self.assertRaises(pushalot.exc.PushalotException):
            httpretty.register_uri(
                httpretty.POST,
                API_URL,
                body='{"Description": "Whatever.."}',
                status=302
            )
            transport = HTTPTransport()
            result = transport.send(Title='Test')
