import os
import unittest
import random
import string
from pyramid import testing
from paste.deploy.loadwsgi import appconfig

from webtest import TestApp
from mock import Mock

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from ringo.lib.sql import DBSession

from ringo import main
from ringo.tests.crud import List, Create, Read, Update, Delete


def get_settings():
    """Returns the settings of the application.
    :returns: appconfig instance

    """
    here = os.path.dirname(__file__)
    return appconfig('config:' + os.path.join(here, '../../', 'test.ini'))


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(get_settings(), prefix='sqlalchemy.')
        cls.Session = sessionmaker()

    def setUp(self):
        connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = connection.begin()

        # bind an individual Session to the connection
        DBSession.configure(bind=connection)
        self.session = self.Session(bind=connection)

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()


class UnitTestBase(BaseTestCase):
    def setUp(self):
        self.config = testing.setUp(request=testing.DummyRequest())
        super(UnitTestBase, self).setUp()

    def get_csrf_request(self, post=None):
        csrf = 'abc'

        if u'csrf_token' not in post.keys():
            post.update({
                'csrf_token': csrf
            })

        request = testing.DummyRequest(post)

        request.session = Mock()
        csrf_token = Mock()
        csrf_token.return_value = csrf

        request.session.get_csrf_token = csrf_token

        return request


class IntegrationTestBase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = main({}, **get_settings())
        super(IntegrationTestBase, cls).setUpClass()

    def setUp(self):
        self.app = TestApp(self.app)
        self.config = testing.setUp()
        super(IntegrationTestBase, self).setUp()

    def login(self, username, password, status=302):
        '''Will login the user with username and password. On default we we do
        a check on a successfull login (status 302).'''
        self.logout()
        response = self.app.post('/auth/login',
                                 params={'login': username,
                                         'pass': password},
                                 status=status)
        return response

    def logout(self):
        'Logout the currently logged in user (if any)'
        response = self.app.get('/auth/logout',
                                params={},
                                status=302)
        return response

    def check_list(self, model, data, user, check_callback=None, status=200):
        List(model, self).run(data, user=user,
                              check_callback=check_callback,
                              status=status)

    def check_create(self, model, data, user, check_callback=None, status=302):
        Create(model, self).run(data, user=user,
                                check_callback=check_callback,
                                status=status)

    def check_read(self, model, data, user, check_callback=None, status=200):
        Read(model, self).run(data, user=user,
                              check_callback=check_callback,
                              status=status)

    def check_update(self, model, data, user, check_callback=None,
                     relations=False, status=302):
        Update(model, self, relations=relations).run(
            data, user=user,
            check_callback=check_callback,
            status=status)

    def check_delete(self, model, data, user, check_callback=None, status=302):
        Delete(model, self).run(data, user=user,
                                check_callback=check_callback,
                                status=status)
