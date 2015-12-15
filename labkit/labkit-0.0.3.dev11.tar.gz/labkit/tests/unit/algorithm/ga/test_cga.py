#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from labkit.algorithm.ga import cga

class TestCga(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_encoding(self):
        return
        cga.encoding(self,conformer)


    def test_first_generation(self):
        return
        cga.first_generation(self)


    def test_score(self):
        return
        cga.score(self,individual)


    def test_select(self):
        return
        cga.select(self,single_pop_count)


    def test_cross(self):
        return
        cga.cross(self,i,j)


    def test_push(self):
        return
        cga.push(self)


    def test_filter(self):
        return
        cga.filter(self,individual)


    def test_new_generation(self):
        return
        cga.new_generation(self,coll,coll_count,new_count)


    def test_db_init(self):
        return
        cga.db_init(self)


    def test___init__(self):
        return
        cga.__init__(self,config_file)


    def test_run(self):
        return
        cga.run(self)


    def test_cga_run(self):
        return
        cga.cga_run()



if __name__ == '__main__':
    unittest.main()



