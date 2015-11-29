# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
from .baaya import Baaya, BOY, GIRL, ERROR


class TestStringMethods(unittest.TestCase):
    def test_age_by_height(self):
        # for boy
        assert Baaya.age_by_height(48.0) == ERROR
        assert Baaya.age_by_height(49.0) == 0.0
        assert Baaya.age_by_height(67.8) == 0.5
        assert Baaya.age_by_height(78.8) == 1.0
        self.assertAlmostEqual(Baaya.age_by_height(92.2), 2.5)
        assert Baaya.age_by_height(150.0) == ERROR

        # for girl
        assert Baaya.age_by_height(48.4, GIRL) == 0.0
        assert Baaya.age_by_height(78.7, GIRL) == 1.0
        assert Baaya.age_by_height(146.0, GIRL) == ERROR

    def test_height_by_age(self):
        # for boy
        assert Baaya.height_by_age(1.5) == ERROR
        assert Baaya.height_by_age(1) == 78.8
        assert Baaya.height_by_age(2) == 89.1

        # for girl
        assert Baaya.height_by_age(1.5, GIRL) == ERROR
        assert Baaya.height_by_age(1, GIRL) == 78.7
        assert Baaya.height_by_age(2, GIRL) == 87.3

if __name__ == '__main__':
    unittest.main()

