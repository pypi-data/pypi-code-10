#!/usr/bin/env python

import django
import unittest
import modjango
from mongoengine.connection import get_connection, ConnectionError
from django.conf import settings
from django.apps.registry import Apps


class TestAppReady(unittest.TestCase):
    def setUp(self):
        setattr(settings, 'MONGO', {
            'MAIN': {
                'HOST': 'mongodb',
                'NAME': 'main'
                }
        })
        self.tearDown()

    def tearDown(self):
        try:
            connection = get_connection('MAIN')
            connection.drop_database('main')
            connection.drop_database('test_main')
            modjango.databases = {}
        except ConnectionError as err:
            pass
        setattr(settings, 'TEST_MODE', False)

    def test_setup_with_single_database(self):
        Apps(['modjango'])
        expected_result = {'MAIN': 'main'}
        self.assertEqual(modjango.databases, expected_result)

    def test_setup_in_testing_mode(self):
        setattr(settings, 'TEST_MODE', True)
        Apps(['modjango'])
        expected_result = {'MAIN': 'test_main'}
        self.assertEqual(modjango.databases, expected_result)

    def test_setup_with_insufficient_settings(self):
        delattr(settings, 'MONGO')
        Apps(['modjango'])
        expected_result = {}
        self.assertEqual(modjango.databases, expected_result)


class TestModjangoTest(unittest.TestCase):
    def setUp(self):
        setattr(settings, 'MONGO', {
            'MAIN': {
                'HOST': 'mongodb',
                'NAME': 'main'
                }
        })
        setattr(settings, 'DATABASES', {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
                }
        })
        Apps(['modjango'])

    def test_the_test_class(self):
        modjango.ModjangoTestCase.setUpClass()
        testcase = modjango.ModjangoTestCase()
        testcase.setUp()
        testcase.tearDown()

if __name__ == '__main__':
    settings.configure()
    unittest.main()
