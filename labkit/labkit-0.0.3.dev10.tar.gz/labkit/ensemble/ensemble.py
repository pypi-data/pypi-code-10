#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from general import gs
from general.unit import hartree_to_kcal
from pymongo import MongoClient
import pymongo
from labkit.conformer.conformer import Conformer
from general import gs
log=gs.get_logger(__name__,debug=False)

from general.interpreter.context import get_context,set_context,update_context

OPTS = [
    gs.cfg.FloatOpt('energy_cut',
                    default=30,
                    help='pool energy cut for conformer'),
    ]

gs.CONF.register_opts(OPTS)

import beanstalkc
import labkit.init_gs
import json
class Ensemble():
    '''
    ensemble 是 collection级别的
    '''
    def __init__(self, db_name="labkit", collection_name="default"):
        self.client = MongoClient(host=gs.CONF.mongo_server, port=gs.CONF.mongo_port)
        self.db=self.client[db_name]
        self.collection=self.db[collection_name]
        self.bq = beanstalkc.Connection(host=gs.CONF.beanstalk_server, port=gs.CONF.beanstalk_port)
        self.bq.use('compute')
        # self.index()

    ### ============ 数据库相关操作


    def save(self,conformer):
        '''
        save a conformer to the ensemble.

        :param conformer:
        :return:  return True is conformer is needed and saved, False if conformer is excluded.
        '''
        if self.need_conformer(conformer):
            self.collection.insert_one(conformer.to_dict())
            return True
        else:
            return False

    def index(self):
        '''
        create index for energy.
        index being created only once is ok.

        :return:
        '''
        return self.collection.create_index([('energy', pymongo.ASCENDING)])
        # print((self.collection.index_information()))
        # print(list(self.collection.index_information()))


    def get_father(self,conformer):
        if conformer.father:
            return self.collection.find({_id:conformer.father})
        else:
            return None

    def find_one(self):
        # done: 这里很有用, 可以抽象, db.name, collection.name 是db和collection相应的名字
        return Conformer().from_dict(self.collection.find_one())

    def find(self):
        return self.collection.find()

    def find_by_conformer(self,*args,**kwargs):
        '''
        return a generater with type of Conformer

        :param args:
        :param kwargs:
        :return: a generater for conformers
        '''
        for i in self.collection.find(*args,**kwargs):
            yield  Conformer().from_dict(i)

    def find_top_energy(self,count):
        '''
        find top count energy, return a dict cursor

        :param count:
        :return: top count dict cursor
        '''
        return self.collection.find().sort('energy', pymongo.ASCENDING).limit(count)

    def min_energy(self):
        '''
        find min energy of the ensemble, return the value

        :return: min energy value
        '''
        return self.collection.find().sort('energy', pymongo.ASCENDING).limit(1)[0]['energy']


    # 函数式操作, map, filter, reduce

    def map(self,module_name,args):
        # map a ensembel to another ensemble with module_name's run function
        all=self.find()

        task={}
        task['module_name']=module_name
        args.update(get_context())
        task['args']=args
        self.bq.use('compute')

        # 取出ensemble所有构型
        # ensemble_name=args['ensemble']
        # 应用单体命令

        for i in all:
            task['args']['xyz']=i['xyz']
            task['args']['code']=i['code']
            task['args']['current_ensemble']=args['current_ensemble']

            self.bq.put(json.dumps(task))

        # todo: 等待处理完成
        while bq.stats_tube('compute')['current-jobs-ready']!=0 or bq.stats_tube('compute')['current-jobs-reserved']!=0 :
            time.sleep(1)

        # todo: 刷新context
        # context=get_context()
        # context['running_job']
        update_context({'last_ensemble':args['current_ensemble']})

    def filter(self,module_name,args):
        pass

    def reduce(self,module_name,args):
        pass



    ## =============== 数据库池相关操作

    def is_needed_in_pool(self,energy_cut=gs.CONF.energy_cut):
        energy=self['energy']
        min_energy=self.collection.find()
        # print(type(min_energy))
        # return
        try:
            min_energy=self.collection.find().sort('energy', pymongo.ASCENDING).limit(1)[0]['energy']
        except:
            return True

        if hartree_to_kcal(energy-min_energy)>energy_cut:
            return False
        # todo: 判重
        # todo: 获得附近能量范围的构型列表
        around_conformers=self.find()
        # 一一判重, 如果不重复, 则save.
        for conformer in around_conformers:
            # print conformer
            # print conformer.get_atoms()
            if self.conformer_duplicated(conformer):
                return False
        return True

    def needed_conformer_2(self,conformer,rmsd_range=gs.CONF.rmsd_range,energy_cut=gs.CONF.energy_cut):
        energy=conformer.energy

        min_energy=self.collection.find()
        try:
            min_energy=self.collection.find().sort('energy', pymongo.ASCENDING).limit(1)[0]['energy']
        except:
            return True

        if hartree_to_kcal(energy-min_energy)>energy_cut:
            return False
        # todo: 判重
        # todo: 获得附近能量范围的构型列表
        around_conformers=self.find()
        # 一一判重, 如果不重复, 则save.
        for conformer in around_conformers:
            if self.conformer_duplicated(conformer):
                return False
        return True

    def duplicated_conformer(self,conformer,rmsd_range=gs.CONF.rmsd_range):
        '''
        to find if a conformer is duplicated in this ensemble.

        :param conformer:
        :param rmsd_range:
        :return: True if indeed duplicated, False in other cases.
        '''
        # todo: 判重
        # todo: 获得附近能量范围的构型列表
        around_conformers=self.collection.find()
        # print "hello"
        # 一一判重, 如果不重复, 则save.
        for compare_to in around_conformers:
            # print compare_to
            # print conformer.get_atoms()
            if conformer.conformer_duplicated(Conformer().from_dict(compare_to)):
                return True

        return False

    def cut_conformer(self,conformer,energy_cut=gs.CONF.energy_cut):
        '''
        return True表示需要cut, False表示不需要, 除非确切知道需要cut, 否则就是False
        energy 不存在的时候, 直接return False
        :param conformer:
        :param energy_cut:
        :return:
        '''

        energy=conformer.energy
        if energy == None:
            return False
        min_energy=self.collection.find()
        # print(type(min_energy))
        # return
        try:
            min_energy=self.collection.find().sort('energy', pymongo.ASCENDING).limit(1)[0]['energy']
        except:
            return False
        if hartree_to_kcal(energy-min_energy)>energy_cut:
            return True

    def need_conformer(self,conformer,rmsd_range=gs.CONF.rmsd_range,energy_cut=gs.CONF.energy_cut):
        if self.cut_conformer(conformer,energy_cut=energy_cut) or self.duplicated_conformer(conformer,rmsd_range=rmsd_range):
            return False
        else:
            return True





def test():
    e=Ensemble()
    c=Conformer().loads('''28
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
    print c.xyz
    # e.save(c)
    print c.get_atom_list()
    print c.get_atoms_cord()
    print c.extract_energy_from_self()

    # print c.
    return True



def run(args):
    pass


if __name__ == '__main__':
    import labkit.init_gs
    from general.interpreter.loader import callrun
    test()

    # callrun(__file__)













    # def set_coll(self,db_name,coll_name):
        #     '''
        #     set the correct collection by db name and collection name
        #     :param db_name:
        #     :param coll_name:
        #     :return:
        #     '''
        #     # self.collection=connection.__getattr__(db_name).__getattr__(coll_name)
        #     # self.db=connection.__getattr__(db_name)
        #     # self.collection=get_coll(db_name,coll_name)
        #     # self.collection=get_coll(db_name,coll_name)
        #     self.db=db_name
        #     self.collection=coll_name

        # @staticmethod
        # def get_coll(db_name,coll_name):
        #     '''
        #     get the correct collection by db name and collection name
        #     :param db_name:
        #     :param coll_name:
        #     :return:
        #     '''
        #     coll=connection.__getattr__(db_name).__getattr__(coll_name)
        #     return coll

