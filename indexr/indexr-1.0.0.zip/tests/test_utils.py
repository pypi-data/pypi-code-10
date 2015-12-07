#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
----------------------------------

Tests for `utils` module.
"""

from indexr.utils import *
import unittest


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tokenize(self):
        """
        Test whether the tokenizr submodule is capable of converting a text to tokens.
        """

        text = 'This is a test.'
        expected_tokens = ['This', 'is', 'a', 'test', '.']
        tokens = tokenize(text)
        self.assertEqual(expected_tokens, tokens)

        text = 'Is this a test? Yes it "is"!'
        expected_tokens = ['Is', 'this', 'a', 'test', '?', 'Yes', 'it', '"', 'is', '"', '!']
        tokens = tokenize(text)
        self.assertEqual(expected_tokens, tokens)


if __name__ == '__main__':
    import sys

    sys.exit(unittest.main())
