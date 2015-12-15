#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry



from mongokit import *
import datetime

import labkitpath

# conformer用一样的, 每个用不同的db,手动继承conformer的接口!
# metacalc也和conformer统一起来, 然后接受字典. 只修改相应的项.

connection = Connection()


from conformermongo import Conformer

@connection.register
class Individual(Conformer):


    structure = {

        'code': int
        'generation': int

    }
    indexes = [
        {
            'fields':['energy'],

            },
        {
            'fields':['code'],
            'unique':True,
            },

        ]
    required_fields = ['from_method', 'xyz', 'energy','code','generation']
    default_values = {'from_parameters':'','out_parameters':'', 'father':''}

    def load_from_file(self,filename):
        file=open(filename)
        self['xyz']=file.read()
        self['from_method']='origin'
        self['energy']=0.0


    def set_coll(self,db_name,coll_name):
        '''set the correct collection by db name and collection name'''
        self.collection=connection.__getattr__(db_name).__getattr__(coll_name)
        self.db=connection.__getattr__(db_name)
        # self.collection=get_coll(db_name,coll_name)
        # self.collection=get_coll(db_name,coll_name)
        # self.db=db_name


    @classmethod
    def get_coll(self,db_name,coll_name):
        '''get the correct collection by db name and collection name'''
        coll=connection.__getattr__(db_name).__getattr__(coll_name)
        return coll


    rotation_position=[]
    rule=[[60,120],[]]
    def load_rule(self,loadrule):
        rule=loadrule

    def encoding(self):
        处理self.conformer



    def decoding(self):
        生成构型
    def mutate(self,mutate_probability):
        if random.random()<mutate_probability:
            #mutate
            self.code变异


def test():

    individual = connection.ga.population1.Individual()  # this uses the database "test" and the collection "example"
    individual['from_method'] = 'origin'
    individual['xyz'] ='''24
    0 1
    H	20.800000 7.440000 7.800000
    C	20.040000 8.160000 8.090000
    H	19.070000 7.680000 7.980000
    H	20.260000 9.070000 7.530000
    C	20.140000 8.560000 9.560000
    O	19.460000 8.000000 10.420000
    N	21.140000 9.340000 9.970000
    H	21.750000 9.750000 9.290000
    C	21.270000 9.810000 11.340000
    H	21.270000 8.930000 11.970000
    C	22.660000 10.410000 11.460000
    H	22.650000 11.320000 10.860000
    H	23.360000 9.780000 10.910000
    C	23.190000 10.500000 12.890000
    O	23.550000 9.470000 13.500000
    O	23.210000 11.590000 13.500000
    C	20.250000 10.840000 11.830000
    O	19.880000 10.750000 13.000000
    N	19.730000 11.680000 10.930000
    H	20.180000 11.800000 10.030000
    C	18.830000 12.770000 11.240000
    H	17.970000 12.370000 11.760000
    H	19.330000 13.560000 11.810000
    H	18.410000 13.130000 10.300000

    '''

    individual['energy'] = 100.0
    individual['code'] = 200

    individual.save()

    print individual

    individual=connection.ga.population1.find_one()

    new_individual=connection.ga.population1.Individual()
    new_individual['father']=individual['_id']
    new_individual['from_method'] = 'origin'
    new_individual['xyz'] ='''24
    0 1
    H	20.800000 7.440000 7.800000
    C	20.040000 8.160000 8.090000
    H	19.070000 7.680000 7.980000
    H	20.260000 9.070000 7.530000
    C	20.140000 8.560000 9.560000
    O	19.460000 8.000000 10.420000
    N	21.140000 9.340000 9.970000
    H	21.750000 9.750000 9.290000
    C	21.270000 9.810000 11.340000
    H	21.270000 8.930000 11.970000
    C	22.660000 10.410000 11.460000
    H	22.650000 11.320000 10.860000
    H	23.360000 9.780000 10.910000
    C	23.190000 10.500000 12.890000
    O	23.550000 9.470000 13.500000
    O	23.210000 11.590000 13.500000
    C	20.250000 10.840000 11.830000
    O	19.880000 10.750000 13.000000
    N	19.730000 11.680000 10.930000
    H	20.180000 11.800000 10.030000
    C	18.830000 12.770000 11.240000
    H	17.970000 12.370000 11.760000
    H	19.330000 13.560000 11.810000
    H	18.410000 13.130000 10.300000

    '''

    new_individual['energy'] = 13300.0
    new_individual['code'] = 2300

    print new_individual



if __name__ == '__main__':
    test()
