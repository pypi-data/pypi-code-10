#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from general import gs
# from labkit.compute import gaussian
log=gs.get_logger(__name__,debug=False)

from general.interpreter.context import get_context,set_context,update_context

import beanstalkc
import labkit.init_gs
bq = beanstalkc.Connection(host=gs.CONF.beanstalk_server, port=gs.CONF.beanstalk_port)

import time
import json

def push_compute(module_name, args):
    '''
    push a task to the compute queue

    :param module_name: the module to call
    :param args: the args
    :return: True if succeed
    '''
    task={}
    task['module_name']=module_name
    args.update(get_context())

    task['args']=args
    bq.use('compute')
    bq.put(json.dumps(task))
    return True

import os
def push_task_file(yml_file):
    '''
    push a yml file to the task queue

    :param yml_file: the yml file
    :return: True if succeed
    '''
    import labkit.init_gs
    bq.use('tasks')
    task={}

    context=get_context()
    context['running_file']=yml_file
    context['running_job']=None
    context['work_dir']=os.path.dirname(yml_file)
    update_context(context)

    task['module_name']='general.interpreter.runner'
    task['args']={}
    task['args']['filename']=yml_file
    task['args'].update(context)

    print task
    bq.put(json.dumps(task))


# def deal_with_line(module_name, args):
#     task={}
#     task['module_name']=module_name
#     args.update(get_context())
#     task['args']=args
#     bq.use('compute')
#     # 取出ensemble所有构型
#     # ensemble_name=args['ensemble']
#     # 应用单体命令
#     bq.put(json.dumps(task))
#     # todo: 等待处理完成
#     while bq.stats_tube('compute')['current-jobs-ready']!=0 or bq.stats_tube('compute')['current-jobs-reserved']!=0 :
#         time.sleep(1)
#     # todo: 刷新context
#     # context=get_context()
#     # context['running_job']
#     return True
#

def test_bean():
    # for i in range(100000):
    #
    #     bq.put(str(i))
    # print "done"
    bq.use('new')
    bq.put('good')


def test():
    from labkit.conformer.conformer import Conformer

    # conformer.load(filename='/Users/lhr/lhrkits/labkit/test/cggg1.xyz')
    # cc=gaussian_conformer(conformer)
    # result = q.enqueue(count_words_at_url, "www.baidu.com")

    # cc.save()

    cc=Conformer()
    cc.from_seq('CGGGG')
    cc.refresh()
    print cc.dumps()
    # xyz=cc.dumps()
    # print xyz
    # gaussian(xyz)
    # result=q.enqueue(gaussian, xyz)

    cc=Conformer().loads('''28
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
    push_gaussian(cc)

    # while True:
    #     s=result.result
    #     if s:
    #         print s
    #         new_c=Conformer().loads(s)
    #         break
    # print new_c.dumps()
    # result = q.enqueue(gaussian, (conformer))


def run(conf):
    print "hello world"

def selfrun():
    import labkit.init_gs
    from general.interpreter.loader import callrun
    callrun(__file__)



if __name__ == '__main__':
    test_bean()
    # selfrun()








# from redis import Redis
# from rq import Queue



#
#
# import requests
# def word_count(url):
#     """Just an example function that's called async."""
#     resp = requests.get(url)
#     time.sleep(10)
#     return len(resp.text.split())
#
# def push_gaussian(conformer,conf):
#     redis_conn = Redis(host=gs.CONF.redis_server,port=gs.CONF.redis_port)
#     q = Queue('compute',connection=redis_conn)  # no args implies the default queue
#     q.enqueue(gaussian.gaussian,conformer.dumps(),conf)
#
#
# def push_wordcount():
#     redis_conn = Redis(host=gs.CONF.redis_server,port=gs.CONF.redis_port)
#     q = Queue('compute',connection=redis_conn)  # no args implies the default queue
#     q.enqueue(gaussian.count_words_at_url,'http://www.baidu.com')
#     # q.enqueue(word_count,'http://www.baidu.com')
# def push_count1():
#     redis_conn = Redis(host=gs.CONF.redis_server,port=gs.CONF.redis_port)
#     q = Queue('compute',connection=redis_conn)  # no args implies the default queue
#     q.enqueue(gaussian.count1)
#
#     # q.enqueue(word_count,'http://www.baidu.com')
#
# # 必须从其他模块import进来

#
# def push_task_file(yml_file):
#     import labkit.init_gs
#     redis_conn = Redis(host=gs.CONF.redis_server,port=gs.CONF.redis_port)
#
#     q = Queue('tasks',connection=redis_conn)  # no args implies the default queue
#     ans= q.enqueue(runner.run_file,yml_file)
#     print ans.result
#
#
#
#
# from general.cli import wrapper_decorator
# ## 用这个版本可以和clize一起正确处理*args, **kwargs, 另外函数不一定要return.
# @wrapper_decorator
# def push_compute_decorator(f,*args,**kwargs):
#     redis_conn = Redis(host=gs.CONF.redis_server,port=gs.CONF.redis_port)
#     q = Queue('compute',connection=redis_conn)  # no args implies the default queue
#     q.enqueue(f,*args,**kwargs)
#
#     # return f(*args,**kwargs)

#
#
# def push_compute(f,*args,**kwargs):
#     redis_conn = Redis(host=gs.CONF.redis_server,port=gs.CONF.redis_port)
#     q = Queue('compute',connection=redis_conn)  # no args implies the default queue
#     q.enqueue(f,*args,**kwargs)
#
#



    # push_compute()

# def test2():
#     # push_wordcount()
#     for i in range(10000):
#         push_count1()
#



