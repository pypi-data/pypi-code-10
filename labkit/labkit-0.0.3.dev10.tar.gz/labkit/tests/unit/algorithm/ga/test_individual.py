#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from labkit.algorithm.ga import individual

class TestIndividual(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_load_from_file(self):
        return
        individual.load_from_file(self,filename)


    def test_set_coll(self):
        return
        individual.set_coll(self,db_name,coll_name)


    def test_get_coll(self):
        return
        individual.get_coll(self,db_name,coll_name)


    def test_load_rule(self):
        return
        individual.load_rule(self,loadrule)


    def test_encoding(self):
        return
        individual.encoding(self)


    def test_decoding(self):
        return
        individual.decoding(self)


    def test_mutate(self):
        return
        individual.mutate(self,mutate_probability)


    def test_test(self):
        return
        individual.test()



if __name__ == '__main__':
    unittest.main()



