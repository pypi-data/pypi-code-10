#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

import mock
from general import gs
import labkit.init_gs
from labkit.ensemble.ensemble import Ensemble
from labkit.conformer.conformer import Conformer



# import testscenarios

# mock.patch以及mock.patch.object只能对module对象使用, 不能直接对函数使用, 另外调用的时候也只有通过module对象调用的函数会被mock.
# mock.patch必须引用module全称, mock.patch.object可以用import进来的module别名, 此外, 修饰符只能引用全局函数,
# 因此最好用mock.patch.object + with + 类里面定义的fake函数.

# testscenarios在scenarios比较多并且完全平行的时候才有优势, 否则直接写几个函数得了.
class TestEnsemble(unittest.TestCase):
    def setUp(self):
        self.e=Ensemble()
        self.c=Conformer().loads('''28
1.out	Energy: -713807.4462872
H          0.77331        1.86613       -0.00062
S          2.00616        2.22090       -0.37382
C          2.93405        1.02341        0.63760
C          2.78619       -0.43223        0.18847
C          1.41386       -0.97478        0.58384
N          0.87560       -1.84954       -0.27177
C         -0.32931       -2.59162        0.02208
C         -1.61514       -1.80838       -0.22383
N         -1.81692       -0.78354        0.63737
C         -2.92836        0.09892        0.48327
C         -2.53526        1.46222       -0.02850
O         -3.60697        2.24037       -0.18306
H         -3.30002        3.09571       -0.50232
H          2.64240        1.11639        1.67592
H          3.97386        1.32263        0.54684
H          3.48639       -1.02079        0.78279
N          3.06940       -0.69701       -1.21009
H          4.06267       -0.72366       -1.37411
H          2.69266        0.05230       -1.77468
O          0.88593       -0.64980        1.63758
H          1.39380       -2.01616       -1.11581
H         -0.29785       -2.91214        1.06057
H         -0.36449       -3.46306       -0.61796
O         -2.39210       -2.12138       -1.09796
H         -1.05593       -0.53513        1.25090
H         -3.46107        0.23865        1.42236
H         -3.62405       -0.34836       -0.21870
O         -1.42097        1.83560       -0.25910

''')

        pass

    def tearDown(self):
        pass
    def test_xyz_energy(self):
        print self.c.xyz
        print self.c.energy


    def test_save(self):
        print self.c.to_xyz()
        print self.c.energy
        self.e.save(self.c)

    def test_find(self):
        self.s=self.e.find()
        self.assertEqual(dict,type(self.s.next()))


    def test_index(self):
        self.assertEqual('energy_1', self.e.index())

    def test___init__(self):
        e=Ensemble(db_name="labkit", collection_name="default")
        self.assertEqual(e.db.name,"labkit")
        self.assertEqual(e.collection.name,"default")


    def test_get_father(self):
        # todo: 回头再弄这个father的问题
        return
        self.c.father=None
        self.e.get_father(self.c)
        self.c.father=self.c._id
        self.e.get_father(self.c)


    def test_find_one(self):
        self.fetched=self.e.find_one()
        self.assertEqual(Conformer,type(self.fetched))

    def test_find_top_energy(self):
        for i in  self.e.find_top_energy(2):
            self.assertEqual(dict, type(i))

    def test_min_energy(self):

        print self.e.min_energy()


    # def test_is_needed_in_pool(self):
    #
    #     self.e.is_needed_in_pool(energy_cut=gs.CONF.energy_cut)


    # def test_needed_conformer_2(self):
    #
    #     self.e.needed_conformer_2(conformer,rmsd_range=gs.CONF.rmsd_range,energy_cut=gs.CONF.energy_cut)


    def test_duplicated_conformer(self):
        
        print self.e.duplicated_conformer(self.c,rmsd_range=gs.CONF.rmsd_range)


    def test_cut_conformer(self):
        
        print self.e.cut_conformer(self.c,energy_cut=gs.CONF.energy_cut)


    def test_need_conformer(self):
        
        self.e.need_conformer(self.c,rmsd_range=gs.CONF.rmsd_range,energy_cut=gs.CONF.energy_cut)

    def test_run(self):
        pass
        # ensemble.run(conf)



if __name__ == '__main__':
    unittest.main()



