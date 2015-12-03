#!/usr/bin/env python

from utils.factor import factor
import unittest

class factorTest(unittest.TestCase):
    def test_factor(self):
        self.assertEqual([2,5,13], factor(130))
        self.assertEqual([3,41], factor(123))
        self.assertEqual([1,131], factor(131))
