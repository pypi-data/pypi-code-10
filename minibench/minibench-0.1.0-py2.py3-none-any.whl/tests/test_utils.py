# -*- coding: utf-8 -*-


import unittest

from minibench.utils import humanize


class HumanizeTests(unittest.TestCase):
    def test_camel_to_human(self):
        self.assertEqual(humanize('Test'), 'Test')
        self.assertEqual(humanize('AnotherTest'), 'Another test')

    def test_dash_to_human(self):
        self.assertEqual(humanize('test'), 'Test')
        self.assertEqual(humanize('another_test'), 'Another test')
