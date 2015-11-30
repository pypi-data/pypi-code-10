import os
import unittest
from nose.tools import raises
from kwick import Kwick, KwickError, __version__

user = os.environ['kwick_user'] or 'test'
password = os.environ['kwick_password'] or 'changeme'

class testKwick(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.kwick = Kwick()
        resp = cls.kwick.kwick_login(user, password)
        assert 'session_name' in resp

    @classmethod
    def teardown_class(cls):
        resp = cls.kwick.kwick_logout()
        assert 'textMsg' in resp

    @raises(KwickError)
    def test_raises_kwick_login_error(self):
        self.kwick.kwick_login(user, 'qwertz')

    def test_index(self):
        resp = self.kwick.kwick_index(page=0)
        assert 'socialstream' in resp
        resp = self.kwick.kwick_index(page=0, community=True)
        assert 'community' in resp and resp['community'] is True

    def test_infobox(self):
        resp = self.kwick.kwick_infobox()
        assert 'infobox' in resp
        assert 'ticker' in resp

    def test_user(self):
        testuser = 'kwick'
        resp = self.kwick.kwick_user(username=testuser)
        assert 'isFriend' in resp

        not_availuser = 'ar5oih435llsv83252jkffSdfs'
        resp = self.kwick.kwick_user(username=not_availuser)
        assert 'errorMsg' in resp

    def test_friends(self):
        resp = self.kwick.kwick_friends()
        assert 'totalSize' in resp

    def test_search_members(self):
        resp = self.kwick.kwick_search_members(gender=0)
        assert 'users' in resp
        resp = self.kwick.kwick_search_members(gender=0, distance=100)
        assert 'users' in resp
        resp = self.kwick.kwick_search_members(gender=0,
                                               online=1,
                                               single=1,
                                               distance=100,
                                               haspic=1)
        assert 'users' in resp

    def test_status(self):
        msg = 'kwickmapi-python Version: {0}'.format(__version__)
        resp = self.kwick.kwick_setstatus(statustext=msg)
        for s in self.kwick.kwick_index(page=0)['socialstream']:
            if s['body'] == msg:
                resp = self.kwick.kwick_socialobject_delete('Microblog', s['socialObjectId'])
                assert 'error' in resp and resp['error'] is False
