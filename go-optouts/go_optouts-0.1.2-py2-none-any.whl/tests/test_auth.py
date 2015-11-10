""" Test for go_optouts.auth. """

from zope.interface.verify import verifyClass, verifyObject

from twisted.internet.defer import inlineCallbacks, Deferred
from twisted.web.resource import Resource
from twisted.web.server import Request, Site

from vumi.tests.helpers import VumiTestCase

from go_optouts.auth import IAuthenticator, RequestHeaderAuth, BouncerAuth
from go_optouts.tests.utils import SiteHelper


def mk_request(path=None, headers=None):
    request = Request(channel=None, queued=True)
    if path:
        request.path = path
    if headers:
        for k, v in headers.items():
            request.requestHeaders.addRawHeader(k, v)
    return request


class TestRequestHeaderAuth(VumiTestCase):
    def test_class_interface(self):
        self.assertTrue(verifyClass(IAuthenticator, RequestHeaderAuth))

    def test_instance_iface(self):
        auth = RequestHeaderAuth()
        self.assertTrue(verifyObject(IAuthenticator, auth))

    @inlineCallbacks
    def test_owner_id_present(self):
        auth = RequestHeaderAuth()
        request = mk_request(headers={"X-Owner-ID": "owner-1"})
        owner_id_d = auth.owner_id(request)
        self.assertTrue(isinstance(owner_id_d, Deferred))
        self.assertEqual((yield owner_id_d), "owner-1")

    @inlineCallbacks
    def test_owner_id_absent(self):
        auth = RequestHeaderAuth()
        request = mk_request()
        owner_id_d = auth.owner_id(request)
        self.assertTrue(isinstance(owner_id_d, Deferred))
        self.assertEqual((yield owner_id_d), None)


class DummyAuthResource(Resource):

    isLeaf = True

    def __init__(self):
        self.requests = []
        self.responses = []

    def add_response(self, code=401, body="Unauthorized", owner_id=None):
        self.responses.append({
            'code': code,
            'body': body,
            'owner_id': owner_id
        })

    def pop_response(self):
        if not self.responses:
            self.add_response()
        return self.responses.pop(0)

    def render(self, request):
        self.requests.append(request)
        response = self.pop_response()
        request.setResponseCode(response['code'])
        if response['owner_id']:
            request.setHeader('X-Owner-ID', response['owner_id'])
        return response['body']


class TestBouncerAuth(VumiTestCase):
    @inlineCallbacks
    def setUp(self):
        self.auth_resource = DummyAuthResource()
        self.site = Site(self.auth_resource)
        self.site_helper = yield self.add_helper(SiteHelper(self.site))

    @property
    def auth_url(self):
        return self.site_helper.url

    def test_class_interface(self):
        self.assertTrue(verifyClass(IAuthenticator, BouncerAuth))

    def test_instance_iface(self):
        auth = BouncerAuth(self.auth_url)
        self.assertTrue(verifyObject(IAuthenticator, auth))

    @inlineCallbacks
    def test_auth_success(self):
        self.auth_resource.add_response(
            code=200, body='Authorized', owner_id='owner-1')
        auth = BouncerAuth(self.auth_url)
        request = mk_request(path="/foo")
        owner_id_d = auth.owner_id(request)
        self.assertTrue(isinstance(owner_id_d, Deferred))
        self.assertEqual((yield owner_id_d), "owner-1")
        [auth_request] = self.auth_resource.requests
        self.assertEqual(auth_request.uri, '/foo')

    @inlineCallbacks
    def test_auth_failed(self):
        auth = BouncerAuth(self.auth_url)
        request = mk_request(path="/foo")
        owner_id_d = auth.owner_id(request)
        self.assertTrue(isinstance(owner_id_d, Deferred))
        self.assertEqual((yield owner_id_d), None)
        [auth_request] = self.auth_resource.requests
        self.assertEqual(auth_request.uri, '/foo')

    @inlineCallbacks
    def test_auth_headers_proxied(self):
        auth = BouncerAuth(self.auth_url)
        request = mk_request(
            path="/foo", headers={'Authorization': 'token'})
        yield auth.owner_id(request)
        [auth_request] = self.auth_resource.requests
        self.assertEqual(auth_request.getHeader('Authorization'), 'token')

    @inlineCallbacks
    def test_auth_headers_absent(self):
        auth = BouncerAuth(self.auth_url)
        request = mk_request(path="/foo")
        yield auth.owner_id(request)
        [auth_request] = self.auth_resource.requests
        self.assertEqual(auth_request.getHeader('Authorization'), None)
