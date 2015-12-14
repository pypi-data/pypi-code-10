#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

'''

dababase operation,
realize save, load, find
orm

'''



## 解决utf8的问题
import  six
if six.PY2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')


from labkit.init_gs import MONGO_SERVER,MONGO_PORT
from pymongo import MongoClient

connection = MongoClient(host=MONGO_SERVER,port=MONGO_PORT)

from pymongo.collection import Collection

class Pool(Collection):

    # (database, name, create=False, **kwargs)¶
    def __init__(self,name):
        connection=MongoClient(host=MONGO_SERVER,port=MONGO_PORT)
        database='gaussian'
        super(Pool,self).__init__(database,name)






# gaussianpool=Pool('calc2')


# database=MongoClient(host=MONGO_SERVER,port=MONGO_PORT)
import pymongo
gaussianpool=connection.gaussian.calc2
for i in gaussianpool.find({'energy':100}).sort('energy', pymongo.ASCENDING):
    #.sort({"energy":1}):
    print(i)


class Conformer():
    '''
    molecular conformer data structure
    '''

    structure = {
        '_type':basestring, # _type filed is for inherit
        'from_method' : basestring,
        'from_parameters' : basestring,
        'out_parameters' : basestring,
        'xyz' : basestring,
        'energy' : float,
        'father' : basestring,
        # self.calc_fun=''


    }
    indexes = [
        {
            'fields':['energy'],
            },
        ]
    required_fields = ['from_method', 'xyz', 'energy']
    default_values = {'from_method' : 'origin','from_parameters':'','out_parameters':'', 'father':''}



    # can not define __init__
    # def __init__(self):
    #     super(Conformer, self).__init__()
    def set_coll(self,db_name,coll_name):
        '''
        set the correct collection by db name and collection name
        :param db_name:
        :param coll_name:
        :return:
        '''
        self.collection=connection.__getattr__(db_name).__getattr__(coll_name)
        self.db=connection.__getattr__(db_name)
        # self.collection=get_coll(db_name,coll_name)
        # self.collection=get_coll(db_name,coll_name)
        # self.db=db_name

    @staticmethod
    def get_coll(db_name,coll_name):
        '''
        get the correct collection by db name and collection name
        :param db_name:
        :param coll_name:
        :return:
        '''
        coll=connection.__getattr__(db_name).__getattr__(coll_name)
        return coll




    def loads(self,string,from_format='xyz'):
        '''
        load conformer from a string, default xyz format
        :param string: conformer representation file content string
        :param from_format: conformer representation format: xyz, pdb, and so on
        :return: the conformer
        '''
        if from_format=='xyz':
            self['xyz']=string
            self.extract_energy_from_self()
            return self
        # 就算是来源是xyz也用babel处理, 可以检查正确性
        to_format='xyz'
        p=subprocess.Popen(['babel',"-i"+from_format,"-o"+to_format],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        output=p.communicate(input=string)[0]
        self['xyz']=output
        self.extract_energy_from_self()
        return self

    def load(self,filename,from_format='xyz'):
        # self.load(open(filename,'r').read(),in_file_format)
        # todo: load空文件的时候sh会卡住
        # out_file=StringIO.StringIO()
        # if not os.path.isfile(filename):
        #     print "Load file do not exist."
        #     raise IOError
        # try:
        #     sh.babel("-i"+in_file_format,filename,"-oxyz",_out=out_file,_err="/dev/null")
        #     # print out_file.getvalue()
        #     self['xyz']=out_file.getvalue()
        # except ErrorReturnCode:
        #     print "babel error", e
        #     raise IOError
        # finally:
        #     out_file.close()
        if from_format=='xyz':
            self['xyz']=open(filename,'r').read()
            self.extract_energy_from_self()
            return self
        to_format='xyz'
        p=subprocess.Popen(['babel',"-i"+from_format,filename,"-o"+to_format],stdout=subprocess.PIPE)
        output=p.communicate()[0]
        self['xyz']=output
        self.extract_energy_from_self()
        return self


    def dumps(self,out_format='xyz'):
        if out_format=='xyz':
            return self['xyz']
        # return sh.babel("-ixyz","-o"+out_format,_in=self['xyz']).stdout
        in_format='xyz'
        p=subprocess.Popen(['babel',"-i"+in_format,"-o"+out_format],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        output=p.communicate(input=self['xyz'])[0]
        return output

    def dump(self,filename,out_format='xyz'):
        # sh.babel("-ixyz","-o"+out_file_format,filename,_in=self['xyz'])
        in_format='xyz'
        p=subprocess.Popen(['babel',"-i"+in_format,"-o"+out_format,filename],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        output=p.communicate(input=self['xyz'])[0]
        return output
        # 加判断, 如果是xyz就直接输出, 但是总是使用babel有个好处就是可以检查xyz的值并标准化
        # if out_file_format=='xyz':
        #     open(filename,'w').write(self['xyz'])
        # else:
        #     sh.babel("-ixyz","-o"+out_file_format,filename,_in=self['xyz'])

    def extract_energy_from_self(self):
        re_energy=r'Energy: ?(.*) *\n'
        # print 'haha',self['xyz']
        match=re.search(re_energy,self['xyz'])
        if match:
            energy=float(match.group(1))
            self['energy']=energy
            # TODO: UN_CACULATED 和 从能量设置xyz域

    def get_father(self):
        if self['father']:
            return self.collection.find({_id:self['father']})
        else:
            return None

    def init(self,conformer_dict):
        for i in conformer_dict:
            self[i]=conformer_dict[i]
        # print self
        return self

    def find_one(self):
        # todo: 这里很有用, 可以抽象, db.name, collection.name 是db和collection相应的名字
        return self.collection.__getattr__(self.__class__.__name__)().from_dict(self.collection.find_one())
    def find(self,*args,**kwargs):
        for i in self.collection.find(*args,**kwargs):
            # print i
            yield  self.collection.__getattr__(self.__class__.__name__)().from_dict(i)


    def empty(self,xyz=''):

        self['xyz']=None
        self['energy']=None
    def is_needed_in_pool(self,energy_cut=30):
        energy=self['energy']
        min_energy=self.collection.find()
        # print(type(min_energy))
        # return
        min_energy=self.collection.find().sort({"energy":1}).limit(1)
        if hartree_to_kcal(energy-min_energy)>energy_cut:
            return False
        # todo: 判重
        # todo: 获得附近能量范围的构型列表
        around_conformers=self.find()
        # 一一判重, 如果不重复, 则save.
        for conformer in around_conformers:
            # print conformer
            # print conformer.get_atoms()
            if conformer_duplicated(self,conformer):
                return False
        return True

    # def save(self):
    #
    #     super(Conformer,self).save()
    #     return

    def get_atoms(self):
        xyz=self['xyz']
        atomlist=[]
        for i,atom in enumerate(xyz.strip().split('\n')):
            if i>1:
                atomlist.append(numpy.array(atom.split()[1:],numpy.float64))
        return atomlist



def get_atoms(self):
    # print self
    xyz=self['xyz']
    atomlist=[]
    for i,atom in enumerate(xyz.strip().split('\n')):
        if i>1:
            atomlist.append(numpy.array(atom.split()[1:],numpy.float64))
    return atomlist


import numpy

from Bio.SVDSuperimposer import SVDSuperimposer
from Bio.PDB.PDBExceptions import PDBException


def conformer_duplicated(conformer1,conformer2):
    '''
    Judge whether two conformer are same in our durable range.
    :param conformer1:
    :param conformer2:
    :return: True or False whether the two conformer are the same.
    '''
    if rmsd(conformer1,conformer2)<0.2:
        return True
    else:
        return False

def rmsd(conformer1,conformer2):
    "计算两个构型的rmsd"
    # 提取坐标
    fixed_coord=numpy.array(get_atoms(conformer1))
    moving_coord=numpy.array(get_atoms(conformer2))
    # fixed_coord=conformer1
    # moving_coord=conformer2
    # print fixed_coord
    # print moving_coord

    if not (len(fixed_coord)==len(moving_coord)):
        raise PDBException("Fixed and moving atom lists differ in size")
    # l=len(fixed)
    # fixed_coord=numpy.zeros((l, 3))
    # moving_coord=numpy.zeros((l, 3))
    # for i in range(0, len(fixed)):
    #     fixed_coord[i]=fixed[i].get_coord()
    #     moving_coord[i]=moving[i].get_coord()
    sup=SVDSuperimposer()
    sup.set(fixed_coord, moving_coord)
    sup.run()
    return sup.get_rms()
    # self.rotran=sup.get_rotran()

