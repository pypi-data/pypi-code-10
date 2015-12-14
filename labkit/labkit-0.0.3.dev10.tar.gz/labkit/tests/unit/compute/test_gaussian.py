#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from labkit.compute import gaussian

class TestGaussian(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_count_words_at_url(self):
        return
        gaussian.count_words_at_url(url)


    def test_gaussian_conformer(self):
        return
        gaussian.gaussian_conformer(conformer,method='pm3 opt',charge=0,mutiplicity=1)


    def test_gaussian(self):
        return
        gaussian.gaussian(xyz,energy_cut=3000000000,database='gaussian',collection='default',method='pm3 ',charge=0,mutiplicity=1)


    def test_test(self):
        return
        gaussian.test()


    def test_run(self):
        return
        gaussian.run(conf)


    def test_selfrun(self):
        return
        gaussian.selfrun()



if __name__ == '__main__':
    unittest.main()




import unittest

from labkit.common import smartlog
from labkit.compute import gaussian


print SEQ


class Testgaussian(unittest.TestCase):

    def setUp(self):
        # 载入测试样例
        # todo: config 的namespace的问题.
        self.logger=smartlog.get_logger(level="DEBUG")


        self.cc=Conformer()
        # self.cc.load_from_file('all_aa.pdb','pdb')
        self.seq='C'
        self.pep=pep_from_seq(self.seq)
        self.cc.loads(self.pep.dumps())
        print self.cc.dumps()
        # print type(self.pep)
        # self.pep=TEMPLATE
        # print TEMPLATE

    def tearDown(self):
        smartlog.clear_logger(self.logger)

    def test_gaussian(self):
        new=gaussian(self.cc)
        print new



if __name__ == '__main__':
    unittest.main()



