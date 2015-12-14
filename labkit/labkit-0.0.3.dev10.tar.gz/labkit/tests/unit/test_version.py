#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

import mock
import testscenarios

from labkit import version


class TestVersion(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

class TestHelloSenario(testscenarios.TestWithScenarios):
    scenarios=[
    ("hello", dict(h="hello",b="1")),
    ("world", dict(h="world",b=2))
    ]
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hello(self):
        pass


    def test_nother(self):
        print self.h
        print self.b



if __name__ == '__main__':
    unittest.main()
