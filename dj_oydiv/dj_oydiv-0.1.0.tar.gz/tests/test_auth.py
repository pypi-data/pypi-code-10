from __future__ import absolute_import, unicode_literals

import random
import base64

from django.test import TestCase
from django.core.validators import ValidationError
from django.http import HttpRequest, HttpResponse
from django.test.client import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.encoding import force_bytes

from . import VIDYO_PORTAL_PASSWORD
from .models import create_test_admin

from dj_oydiv.auth.decorators import vidyo_admin_rpc_auth
from dj_oydiv.auth.basic import http_basic_credentials


class HttpBasicAuthTests(TestCase):
    USER = 'mac'
    PASSWORD = 'mygoodpassword'
    CLIENT_IP = '192.168.1.100'

    def _bare_credentialed_request(self, ip=None, user=None, password=None):
        extra = {}
        user = user or self.USER
        password = password or self.PASSWORD
        auth_header = b'Basic ' + base64.b64encode(force_bytes('%s:%s' % (user, password)))
        extra['HTTP_AUTHORIZATION'] = auth_header
        if ip:
            extra['REMOTE_ADDR'] = ip

        request = self.factory.get('/', **extra)
        return request

    def _session_middleware_credentialed_request(self, **kwargs):
        request = self._bare_credentialed_request(**kwargs)
        request.user = AnonymousUser()
        # setup sessions, etc.
        SessionMiddleware().process_request(request)

        return request

    def _good_credentials(self, ip=None, user=None, password=None):
        return self._session_middleware_credentialed_request(ip=ip, user=user, password=password)

    def _bad_credentials(self, ip=None, user=None, password=None):
        password = password or 'mybadpassword'
        return self._session_middleware_credentialed_request(ip=ip, user=user, password=password)

    def setUp(self):
        self.user = User.objects.create_user(
            username=self.USER, email='mac@example.com', password=self.PASSWORD
        )
        self.vidyo_admin = create_test_admin(
            dj_auth_user=self.user, password=self.PASSWORD
        )
        self.vidyo_admin.use_ip_auth = False
        self.vidyo_admin.save()
        self.factory = RequestFactory()

    def myview(self, request):
        """Just a dummy view to pass to the decorators"""
        return HttpResponse('success')

    def test_bad_credentials(self):
        request = self._bad_credentials()
        response = vidyo_admin_rpc_auth(self.myview)(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'')

    def test_no_credentials_401(self):
        response = vidyo_admin_rpc_auth(self.myview)(HttpRequest())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'')

    def test_good_credentials_deny_empty_ip(self):
        self.vidyo_admin.use_ip_auth = True
        self.vidyo_admin.save()
        request = self._good_credentials()
        response = vidyo_admin_rpc_auth(self.myview)(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'')

    def test_good_credentials_good_ip(self):
        self.vidyo_admin.use_ip_auth = True
        self.vidyo_admin.save()
        self.vidyo_admin.ipmodel_set.create(ip=self.CLIENT_IP)
        request = self._good_credentials(ip=self.CLIENT_IP)

        response = vidyo_admin_rpc_auth(self.myview)(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')

    def test_good_credentials_bad_ip(self):
        self.vidyo_admin.use_ip_auth = True
        self.vidyo_admin.save()
        self.vidyo_admin.ipmodel_set.create(ip=self.CLIENT_IP)
        request = self._good_credentials(ip='255.255.255.255')
        response = vidyo_admin_rpc_auth(self.myview)(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'')

    def test_good_credentials_no_ip_auth(self):
        request = self._good_credentials()
        response = vidyo_admin_rpc_auth(self.myview)(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')

    def test_successful_auth_user_login(self):
        """
        Tests for successful user login on delivery of good auth credentials
        The purpose of this is to avoid expensive calls to
        ``django.contrib.auth.authenticate()`` with every request, when
        a session can be set up instead.  (cookie support required clientside)
        """
        request = self._good_credentials()
        self.assertEqual(request.user.is_authenticated(), False)
        response = vidyo_admin_rpc_auth(self.myview)(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')
        self.assertEqual(request.user.is_authenticated(), True)
        self.assertEqual(self.user, request.user)

    def test_vidyo_admin_model_decrypted(self):
        """
        tests that given proper credentials, a decrypted vidyoadmin model is
        available as an attribute of request.user
        """
        request = self._good_credentials()
        vidyo_admin_rpc_auth(self.myview)(request)
        try:
            self.assertEqual(request.user.vidyoadmin.password, VIDYO_PORTAL_PASSWORD)
        except ValueError as e:
            self.addFailure(e)

    def test_user_no_vidyoadmin_401(self):
        """
        If a given user doesn't have a vidyoadmin FK, then authentication
        should fail, regardless  of the quality of the given credentials
        """
        User.objects.create_user(
            username='mac2', email='mac2@example.com', password='mymac2password'
        )
        request = self._session_middleware_credentialed_request(
            user='mac2', password='mymac2password'
        )
        response = vidyo_admin_rpc_auth(self.myview)(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'')

    def test_extract_http_basic_credentials(self):
        user, password = http_basic_credentials(
            self._session_middleware_credentialed_request(user='silly', password='sausage')
        )
        self.assertEqual(user, b'silly')
        self.assertEqual(password, b'sausage')

    def test_extract_http_basic_credentials_with_colon(self):
        user, password = http_basic_credentials(
            self._session_middleware_credentialed_request(user='silly', password='sau:sage')
        )
        self.assertEqual(user, b'silly')
        self.assertEqual(password, b'sau:sage')


class IPAddressWhitelistTest(TestCase):
    ITERATIONS = 20

    def setUp(self):
        self.admin = create_test_admin()
        self.admin.use_ip_auth = True
        self.admin.save()

    @staticmethod
    def random_bad_ipv4():
        return ''.join(str(random.randint(256, 999)) + '.' for x in range(4))[:-1]

    @staticmethod
    def random_ipv4():
        return ''.join(str(random.randint(0, 255)) + '.' for x in range(4))[:-1]

    @staticmethod
    def random_ipv6():
        return ''.join(hex(random.randint(0, 65535))[2:] + ':' for x in range(8))[:-1]

    def test_ip6_multiple_representation(self):
        """
        IPv6 addresses can be formatted in multiple styles, and are often shortened
        with multiple colons when a particular tuple is all-zeros.
        This test checks that IP addresses are properly normalised before comparison.
        """
        self.admin.ipmodel_set.create(ip='0000:0000:0000:0000:0000:0000:0000:0001')
        self.assertTrue(self.admin.is_ip_allowed('::1'))

    def test_ip_auth_off_permissive(self):
        """
        Ensure that a reasonable set of random ip addresses
        are permitted when ip auth is off.
        """
        self.admin.use_ip_auth = False
        for x in range(self.ITERATIONS):
            self.assertTrue(self.admin.is_ip_allowed(self.random_ipv4()))
            self.assertTrue(self.admin.is_ip_allowed(self.random_ipv6()))

    def test_ip_auth_on_strict(self):
        """
        Make a reasonable claim that all ip addresses but
        those added to the allowed whitelist are rejected.
        """
        for x in range(self.ITERATIONS):
            self.assertFalse(self.admin.is_ip_allowed(self.random_ipv4()))
            self.assertFalse(self.admin.is_ip_allowed(self.random_ipv6()))

    def test_added_ip_passed(self):
        """check that any ip is rejected, until it is added"""
        ips = [self.random_ipv4() for x in range(self.ITERATIONS)] + \
              [self.random_ipv6() for x in range(self.ITERATIONS)]
        for ip in ips:
            self.assertFalse(self.admin.is_ip_allowed(ip))
            self.admin.ipmodel_set.create(ip=ip)
            self.assertTrue(self.admin.is_ip_allowed(ip))

    def test_malformed_ip_rejected(self):
        for x in range(self.ITERATIONS):
            with self.assertRaises(ValidationError):
                self.admin.ipmodel_set.create(ip=self.random_bad_ipv4())
                self.admin.save()
