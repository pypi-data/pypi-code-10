#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dbus2any
----------------------------------

Tests for `dbus2any` module.
"""

import unittest

from dbus2any import xml2any, read_template
from os import path

from types import SimpleNamespace


class TestDbus2any(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.xml_dir = path.join(path.dirname(__file__), 'xml')
        self.expected_dir = path.join(path.dirname(__file__), 'expected')

    def test_000_something(self):
        expected = self.read_expected('openobex.py')
        tpl = read_template('pydbusclient.tpl')
        xml = self.read_xml('openobex.xml')
        args = self.get_args()
        mpris2 = xml2any(tpl, xml, args)
        self.assertEqual(expected, mpris2)


    def read_xml(self, name):
        with  open(path.join(self.xml_dir, name)) as xml:
            return xml.read()


    def read_expected(self, name):
        with  open(path.join(self.expected_dir, name)) as expected:
            return expected.read()

    def get_args(self):
        return SimpleNamespace(
            template="pydbusclient.tpl",
            xml='openobex.xml',
            busName='org.openobex.Manager',
            objectPath='/org/openobex/Manager',
            interface=None
        )

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
