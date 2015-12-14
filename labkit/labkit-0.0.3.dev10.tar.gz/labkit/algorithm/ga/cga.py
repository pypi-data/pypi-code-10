#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from docopt import docopt
import os, sys, re, sh
from glob import glob
import yaml, logging

import mypub, labkitpath
import crash_on_ipy
import mylog

from labkit.algorithm.ga.individual import Individual




class Cga():
    

    # 个体编码
    def encoding(self,conformer):
        #二面角
        #反编码


    # 初始群体的产生
    def first_generation(self):
        pass

    # 适应度汁算
    def score(self,individual):
        # 计算高斯
        individual.conformer.gaussian()
        # 获得能量
        energy=individual.conformer.energy
        # 额外得分
        plus_score=0
        return energy+plus_score


    # 选择运算
    def select(self,single_pop_count):

        cursor=self.collection.find().sort({"score":1}).limit(single_pop_count)
        gaussian_sample()

        return cursor

    # 交叉运算
    def cross(self,i,j):
        random()位点
        new=swap()code
        return



    # 变异运算
    # def mutate(self,coll,mutate_probability):
    #
    #     for i,tmp in enumerate(coll):
    #         if rand()<mutate_probability:
    #             #mutate
    #             coll[i].mutate

        #return coll

    def push(self):
        pass


    def filter(self,individual):
        flag=True
        if individual.conformer.engery 高:
            flag=False
        if 重复:
            flag=False
        return flag


    def new_generation(self,coll,coll_count,new_count):

        count=0
        while count<new_count:

            i,j=random.sample(coll,2)
            new_individual=self.cross(i,j)
            new_individual.mutate(mutate_probability)
            new_individual.decoding()
            new_individual.conformer.calc()
            new_individual.encoding()

            if self.filter(new_individual):
                count=count+1
                self.push(new_individual)




    def db_init(self):
        # clear_db
        # index
        self.collection.ensureIndex({"score":1})

    def __init__(self,config_file):

        #init conformer object
        self.pool=Cgapool(config)
        self.collection=config['COLLECTION']

        #read from config_file
        config=load_config("cga.config")
        self.max_generation_count=100
        self.selection_count=10
        self.mutate_probability=0.8
        self.new_generation_count=6


    def run(self):
        #read from config_file

        for generation_count in range(self.max_generation_count):
            if  generation_count==0:
                selection=self.first_generation()
            else:
                selection=self.select(self.selection_count)


            self.new_generation(selection,self.selection_count,self.new_generation_count)

from sigtools.modifiers import kwoargs
from clize import run

# @kwoargs('no_capitalize')

def cga_run():


    cga=Cga()
    cga.run()

# todo: 测试改变类的方法, 那么实例的方法是否改变.

if __name__ == '__main__':
    run(cga_run)
