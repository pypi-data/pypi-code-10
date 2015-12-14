#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from labkit.algorithm.sys import sys

class TestSys(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_wait(self):
        return
        sys.wait()


    def test_first_generation(self):
        return
        sys.first_generation(self)


    def test_push(self):
        return
        sys.push(self)


    def test_new_generation(self):
        return
        sys.new_generation(self,coll,coll_count,new_count)


    def test_db_init(self):
        return
        sys.db_init(self)


    def test___init__(self):
        return
        sys.__init__(self,config_file)


    def test_sample_and_first_calc_enqueue(self):
        return
        sys.sample_and_first_calc_enqueue(self,metemethod="pm3",energy_cut=30)


    def test_run(self):
        return
        sys.run(self)


    def test_sys_run(self):
        return
        sys.sys_run()



if __name__ == '__main__':
    unittest.main()



