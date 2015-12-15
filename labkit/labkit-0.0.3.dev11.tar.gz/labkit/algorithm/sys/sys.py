#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


from labkit.scheduler.push_task_file import q


def wait():
    while len(q)>0:
        time.sleep(1)


sys_method_list=['pm3','hf 3/21G*', ]



class Sys():


    # 初始群体的产生
    def first_generation(self):
        pass


    def push(self):
        pass


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

    def sample_and_first_calc_enqueue(self,metemethod="pm3",energy_cut=30):
        # todo: 生成初始构型
        # for i in generate
        pass

    def run(self):
        #read from config_file

        sample_and_first_calc_enqueue(meta_method='')
        # 当算完了之后再处理, 暂时一步一步做.
        wait()
        findhf(energy_cut=20)

        for i in config.sys:
            next_generation_calc_enqueue(meta_method='')
            # 当算完了之后, 再处理
            wait()
            findhf(energy_cut=20)
        # 插入的时候就判重

        deal_with

def sys_run():


    cga=Cga()
    cga.run()


if __name__ == '__main__':
        pass
