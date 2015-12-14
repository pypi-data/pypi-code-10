#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


'''
worker requirements:
环境变量:
export PYTHONPATH=/vagrant/labkit:$PYTHONPATH
export PATH=/vagrant/g09:$PATH

'''
# todo: redis 任务管理, 删除failed任务

import sys
from general import gs


# from rq import Queue, Connection, Worker
# from redis import Redis

# Preload libraries
# import library_that_you_want_preloaded

# Provide queue names to listen to as arguments to this script,
# similar to rqworker



#
# def start_worker(queue_names):
#
#     # import requests
#
#     redis_conn = Redis(host=gs.CONF.redis_server,port=gs.CONF.redis_port)
#     with Connection(redis_conn):
#         # qs = map(Queue, sys.argv[1:]) or [Queue()]
#         qs = map(Queue, queue_names) or [Queue()]
#
#         w = Worker(qs)
#         w.work()



import beanstalkc
import labkit.init_gs
from general.interpreter.context import get_context,set_context,update_context

bq = beanstalkc.Connection(host=gs.CONF.beanstalk_server, port=gs.CONF.beanstalk_port)

from general.interpreter.runner import call

import json
import traceback
def bean_worker():
    '''
    a single job deal circle

    :return:
    '''
    job=bq.reserve()
    try:

        # deal with the message
        task=json.loads(job.body)
        # result= task['module_name']
        print task
        result=call(task['module_name'],task['args'])
        # result=call(job.body)
        # done
        if result:
            print "==========",result

            job.delete()
        else:
            job.bury()


    except:
        traceback.print_exc()
        job.bury()

def start_worker(queue_names):
    '''
    start worker loop

    :param queue_names:
    :return:
    '''
    for i in queue_names:
        bq.watch(i)
    print bq.watching()
    context=get_context()
    while 1:
        bean_worker()
        # 退出worker的条件, 可以是file, 或者是数据库里的键
        if None:
            break



if __name__ == '__main__':
    start_worker(['compute'])

    # start_worker(["compute"])


