#!/usr/bin/env python

import unittest
import utils

class chainTest(unittest.TestCase):
    def test_map(self):
        self.assertEqual([1,4,9], [1,2,3].map(lambda x:x**2).toList())

    def test_filter(self):
        self.assertEqual([2,6], [1,2,6].filter(lambda x:not x&1).toList())

    def test_reduce(self):
        self.assertEqual(6, [1,2,3].reduce(lambda x,y: x+y))

    def test_take(self):
        self.assertEqual([1,2], [1,2,3].take(2).toList())


if __name__=="__main__":
    unittest.main()
