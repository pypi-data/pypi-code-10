
import os
import unittest
import json
from nose.tools import assert_equal, eq_, nottest
from server.app.AMSapp import app
from server.utils.AMSUserApp import userapp_authenticate

class TestAMSServer(unittest.TestCase):
    app_config = {
        "port-number": "14001"
    }
    def setUp(self, use_test_app = True):
        if use_test_app is True:
            self.app = app.test_client()
        else:
            self.app = None
        print(__name__, ': TestAMSServer.setUp()  - - - - - - - -')


    def test_add(self):
        self.assertEqual(1 + 1, 2)

    @staticmethod
    def check_content_type(headers):
        eq_(headers['Content-Type'], 'application/json')


    def test_userapp_login_via_flask(self):
        rv = userapp_authenticate("dk-it", "dk-it")
        self.assertIsNotNone(rv)


    def test_endtoend_protected_success_via_flask(self):
        token = userapp_authenticate("dk-it", "dk-it")
        self.assertIsNotNone(token)
        self.app.set_cookie("localhost", "ua_session_token", token, path='/v1/endtoendprotected')
        rv = self.app.get('/v1/endtoendprotected')
        tple = rv.headers[0]
        self.assertEqual(tple[1], 'application/json')
        self.assertIsNotNone(rv)
        resp = json.loads(rv.data)
        self.assertIsNotNone(resp)
        self.assertEqual(rv.status_code, 200)


    def test_endtoend_protected_put_success_with_cookie_via_flask(self):
        token = userapp_authenticate("dk-it", "dk-it")
        self.assertIsNotNone(token)
        self.app.set_cookie("localhost", "ua_session_token", token, path='/v1/endtoendprotected')
        d1 = dict()
        d1['att'] = 'val'
        d1['ua_session_token'] = token
        rv = self.app.post('/v1/endtoendprotected', data=json.dumps(d1))

        tple = rv.headers[0]
        self.assertEqual(tple[1], 'application/json')
        self.assertIsNotNone(rv)
        resp = json.loads(rv.data)
        self.assertIsNotNone(resp)
        self.assertEqual(rv.status_code, 200)


    def test_endtoend_protected_post_success_without_cookie_via_flask(self):
        token = userapp_authenticate("dk-it", "dk-it")
        self.assertIsNotNone(token)
        d1 = dict()
        d1['att'] = 'val'
        d1['ua_session_token'] = token
        rv = self.app.post('/v1/endtoendprotected', data=json.dumps(d1))

        tple = rv.headers[0]
        self.assertEqual(tple[1], 'application/json')
        self.assertIsNotNone(rv)
        resp = json.loads(rv.data)
        self.assertIsNotNone(resp)
        self.assertEqual(rv.status_code, 200)


    def test_endtoend_protected_get_success_without_cookie_via_flask(self):
        token = userapp_authenticate("dk-it", "dk-it")
        self.assertIsNotNone(token)
        d1 = dict()
        d1['ua_session_token'] = token
        rv = self.app.get('/v1/endtoendprotected', data=json.dumps(d1))

        tple = rv.headers[0]
        self.assertEqual(tple[1], 'application/json')
        self.assertIsNotNone(rv)
        rvd = rv.data
        rvd2 = rvd.replace("\\", "").replace("\"{", "{").replace("}\"", "}")
        resp = json.loads(rvd2)
        if 'end' in resp:
            self.assertIsNotNone(resp['end'])
        else:
            self.assertTrue(False, 'unable to get json')

        self.assertEqual(rv.status_code, 200)




    def tearDown(self):
        print(__name__, ': TestAMSServer.tearDown() - - - - - - -')
        directory = '.'

        try:
            os.remove('./AMSAppConfig.json')
        except OSError, ose:
            pass


    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
