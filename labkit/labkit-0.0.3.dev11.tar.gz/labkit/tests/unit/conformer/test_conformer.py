#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import sys
import unittest
from labkit.conformer.conformer import Conformer,TEMPLATE
from labkit.ensemble.ensemble import Ensemble
from general import time_count
import labkit.init_gs
import os

import testscenarios

# class TestConformer(unittest.TestCase):
class TestConformer(testscenarios.TestWithScenarios):

    scenarios=[
        ("case1", dict(case_folder="case1")),
        # ("case2", dict(case_folder='case2'))
    ]
    # file_name='cggg'

    def setUp(self):

        from  labkit.tests.test_sample import TEST_SAMPLE_LOCATION
        self.origin_path=os.path.abspath(os.curdir)

        os.chdir(os.path.join(TEST_SAMPLE_LOCATION,self.case_folder))

        self.c=Conformer()
        self.e=Ensemble()

        self.sample_xyz='''28
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

'''
        return

        # refresh的时间很短, 0.001s
        print time_count(self.c.from_seq,self.seq)
        print time_count(self.c.to_xyz)

        # loads的时间最长, 0.1s, build时间长, build最长在babel或者在pandas, 应该在babel
        print time_count(Conformer().loads,self.sample_xyz)

    def tearDown(self):
        os.chdir(self.origin_path)
        pass

    def test_empty_xyz(self):
        self.c.empty_xyz()
        self.assertIsNone(self.c.dumps())

    def test_empty_list(self):
        self.c.empty_list()
        self.assertIsNone(self.c.dumps())

    def test_load_and_dump(self):
        self.c.dump("cggg.pdb",'pdb')
        TEMPLATE.dump("template.pdb",'pdb')
        return
        self.c.dumps()


        self.c.loads(self.sample_xyz)
        self.c.dumps()

        # 从out文件转的时候, 需要能量
        self.c.load('1.out','out')
        self.c.energy
        self.c.dump('new.xyz')
        self.c.dumps()

        self.c.load('template_test.xyz3')
        self.c.dumps()
        # print TEMPLATE[1].segid

    def test_from_dict(self):

        conformer_dict=self.e.collection.find_one()
        self.assertEqual(Conformer,type(self.c.from_dict(conformer_dict)))

        # print self.c.from_dict(conformer_dict).conf

        conformer_dict=Ensemble(collection_name='cggg_sample_generate').collection.find_one()
        print conformer_dict
        self.c.from_dict(conformer_dict)

    def test_to_dict(self):

        # print self.c.to_dict()
        self.assertEqual(dict,type(self.c.to_dict()))

    def test_template_and_load_dump(self):
        
        # todo: 格式不对, 或者空文件, 会卡住
        self.c.dump('template_text2.xyz')
        self.c.load('template_test2.xyz','xyz')
        print self.c.dumps()
        self.c.loads(TEMPLATE.dumps())
        self.c.dump('template_test3.xyz')
        self.c.dump('template_test.pdb','pdb')


    def test_add(self):
        
        c1=Conformer().from_seq('C')
        c2=Conformer().from_seq('GG')
        print "c1 is: ",c1
        print list(c1.get_atoms())
        print c1.get_atom_list()
        print c2.get_res_list()
        # for i in c2:
        #     print i
        print "c1 is: ",c1.get_ca_list()
        print "c2 is: ",c2.get_ca_list()
        print "c1+c2 is: ",(c1+c2).get_ca_list()

        print "now c1 is: ",c1.get_ca_list()
        print "now c2 is: ",c2.get_ca_list()


    def test_set_dihedral(self):
        

        # 测试set_dihedral
        # open('cggg1.xyz','w').write(self.pep.dumps())
        # self.pep=pep_from_seq(self.seq)
        # c=Conformer()

        self.c.set_dihedral(self.c.conf['BACKBONE_TEMPLATE'][0],60)

        self.c.dump('cggg_60.xyz')


    def test_is_legit(self):

        print self.c.is_legit()
        print self.c.is_legit(1)


    def test_extract_bonds(self):

        print self.c.extract_inner_bonds()

    def test_main(self):
        pass
        # main()

    def test_encoding(self):

        # code=encoding(self.pep,self.backbone_template)
        # Polypeptide.logger.debug(Conformer().loads(self.pep.dumps()).dump('test.pdb','pdb'))
        # print Conformer.loads(self.pep.dumps())
        cc=Conformer().load("1.xyz")

        code=self.c.encoding(self.c.conf['BACKBONE_TEMPLATE'])
        print code
        return
        firstcode=self.c.first_code(self.c.conf['BACKBONE_TEMPLATE'],self.c.conf['SIDE_TEMPLATE'])
        print firstcode


    def test_generate(self):
        # print self.c.conf
        # print self.c.encoding()
        # return
        from itertools import product
        # backbone_coding,side_coding=self.c.generate()
        # for i in product(backbone_coding,side_coding):
        #     print i

        # self.c.load('cggg.xyz')
        # return
        code=self.c.generate()
        for i in code:
            print Conformer().decoding(i).dump(str(i)+".pdb",'pdb')


    def test_decoding(self):
        code=(0,0,0),()

        c=Conformer().decoding(code)
        print c


    def test_combine(self):

        pep1=TEMPLATE[:10]
        pep2=TEMPLATE[10:]
        pep1+pep2

    def test_vector(self):
        from Bio.PDB.Vector import Vector
        import math
        PI=math.pi


        start=Vector(0,0,0)
        end=Vector(0,0,1)
        trans= (end-start).get_array()
        # self.c.refresh()
        print self.c.dumps()
        self.c.moving(trans)
        print self.c.dumps()


        return

        angle=PI/3
        p=Vector(0,1,0)

        # should be <Vector -0.87, 0.50, 0.00>
        print self.c.axis_rotate_with_start_end(p,start,end,angle)
        # should be <Vector -0.87, 0.50, 0.00>
        print p.axis_rotate_with_origin(end,angle)

        # should be (1,1,0)
        print self.c.calc_coord_from_z(p,start,end,1,PI/2,PI/2)

    def test_moving(self):
        self.c.moving()


    def test_refresh(self):
        
        self.c.refresh()

    def test_extract_energy_from_self(self):
        
        self.c.extract_energy_from_self()


    def test_get_atoms_cord(self):
        self.c.get_atoms_cord()


    def test_rmsd(self):
        print self.c.rmsd(self.c)



    def test_conformer_duplicated(self):
        
        self.c.conformer_duplicated(self.c)


    def test_build(self):
        return
        self.c.build()



    def test_neutralize(self):
        self.c.neutralize()


    def test_addH3(self):
        
        self.c.addH3()


    def test_addOXH(self):
        
        self.c.addOXH()


    def test_atom_list(self):
        for res in self.c:
            self.c.atom_list(res)


    def test_get_atom_list(self):
        self.c.get_atom_list()




    def test_load_top(self):
        self.c.load_top()


    def test_get_four_atoms(self):
        
        self.c.get_four_atoms(dihedral_name)



    def test_moving(self):
        
        self.c.moving(from_atom, target_atom)


    def test_moving_atom(self):
        
        self.c.moving_atom(atom_serial_number)


    def test_get_phi_psi_list(self):
        
        print self.c.get_phi_psi_list()



    def test_moving_pep(self):
        
        self.c.moving_pep(pep,residue)


    def test_get_dihedral(self):
        
        self.c.get_dihedral(dihedral_selector)


    def test___add__(self):
        
        self.c.__add__(self.c)


    def test_get_atoms(self):
        print self.c.get_atoms()



    def test_bebonding(self):
        atoms=self.c.get_atoms()
        atom1=atoms.next()
        atom2=atoms.next()
        # print atom1,atom2
        self.c.bebonding(atom1, atom2)


    def test_is_peptide_bond(self):
        
        self.c.is_peptide_bond(atom1, atom2)


    def test_extract_inner_bonds(self):
        
        print self.c.extract_inner_bonds()






    def test_first_code(self):
        
        self.c.first_code(backbone_template,side_template)




    def test_cross(self):
        return
        self.c.cross(code1,code2)


    def test_metacalc(self):
        return
        self.c.metacalc(calc_func)



    def test_run(self):
        return

        run(conf)


    def test_selfrun(self):
        return
        conformer.selfrun()



if __name__ == '__main__':
    unittest.main()
