#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

import importlib
# from __future__ import print_function
import os
import re
import sys

from general import gs
from general.interpreter.loader import call, load, load_module
from general.reflection import get_script_location
from general.interpreter.context import get_context,set_context,update_context

log=gs.get_logger(__name__,debug=True)

# filename=sys.argv[1]

def eval_tree_local(tree):
    '''
    parse a conf(dict) and run it

    :param tree:
    :return:
    '''

    # print type(conf)
    # 如果什么都不是则返回自身
    if type(tree)!=dict and type(tree)!=list:
        if load_module(tree):
            # return conf
            return call(tree,{})
        else:
            return tree
    # 如果是list则递归解析
    if type(tree)==list:
        ans=[]
        for item in tree:
            # print item
            ans.append(eval_tree(item))
        return ans
    # 如果是dict递归解析, 如果key是module, 执行
    else:
        ans={}

        # 分类讨论repeat和until
        if tree.has_key('repeat'):
            repeat=tree['repeat']
            if tree.has_key('until'):
                until=tree['until']
            else:
                until=False
        elif tree.has_key('until'):
            repeat=1000000
            until=tree['until']
        else:
            repeat=1
            until=True

        # until=conf.get('until',True)
        # repeat=conf.get('repeat',1)

        for loop in range(repeat):
            for key in tree.keys():
                child=tree[key]
                # print key, child

                # if type(child)!=dict and type(child)!=list:
                    # print child
                    # ans.update({key,child})
                    # return child
                # if type(child)==list:
                    # ans.update(key,run(child))
                # else:
                if load_module(key):
                    print key ,child
                    # print call(key,parse(child))

                    return call(key,eval_tree(child))
                    # ans.update({key:call(key,eval_conf(child))})

                else:
                    ans.update({key:eval_tree(child)})
            until=eval_tree(until)
            if until:
                break

        return ans

from labkit.scheduler.push import bq
# from labkit.scheduler.push import deal_with_line
import  time

from labkit.ensemble.ensemble import Ensemble

def deal_with_line(module_name, args):
    '''
    对于compure中的模块调用map, 推送队列
    对于filter中的模块调用filter
    其他的就直接执行

    :param module_name:
    :param args:
    :return:
    '''

    if 'compute' in module_name:

        args['current_ensemble']=args['ensemble']+'_'+module_name.replace('.','_')
        ensemble=Ensemble(collection_name=args['last_ensemble'])
        ensemble.map(module_name,args)
    elif 'filter' in module_name:
        collection_name=args['ensemble']+'_'+module_name.replace('.','_')
        ensemble=Ensemble(collection_name=collection_name)
        ensemble.filter(module_name,args)
    else:
        call(module_name,args)

    return True

    task={}
    task['module_name']=module_name
    args.update(get_context())
    task['args']=args
    bq.use('compute')
    # 取出ensemble所有构型
    # ensemble_name=args['ensemble']
    # 应用单体命令
    bq.put(json.dumps(task))
    # todo: 等待处理完成
    while bq.stats_tube('compute')['current-jobs-ready']!=0 or bq.stats_tube('compute')['current-jobs-reserved']!=0 :
        time.sleep(1)
    # todo: 刷新context
    # context=get_context()
    # context['running_job']
    return True


def eval_tree(tree):
    '''
    parse a conf(dict) and run it

    :param tree:
    :return:
    '''

    # print type(conf)
    # 如果什么都不是则返回自身
    if type(tree)!=dict and type(tree)!=list:
        if load_module(tree):
            # return conf
            # return call(tree,{})
            return deal_with_line(tree,{})

        else:
            return tree
    # 如果是list则递归解析
    if type(tree)==list:
        ans=[]
        for item in tree:
            # print item
            ans.append(eval_tree(item))
        return ans
    # 如果是dict递归解析, 如果key是module, 执行
    else:
        ans={}

        # 分类讨论repeat和until
        if tree.has_key('repeat'):
            repeat=tree['repeat']
            if tree.has_key('until'):
                until=tree['until']
            else:
                until=False
        elif tree.has_key('until'):
            repeat=1000000
            until=tree['until']
        else:
            repeat=1
            until=True

        for loop in range(repeat):
            for key in tree.keys():
                child=tree[key]
                if load_module(key):
                    print key ,child
                    # 主动的推送
                    # return call(key,eval_tree(child))
                    # 自动的推送
                    return deal_with_line(key,eval_tree(child))


                else:
                    # 用一般参数更新context
                    if type(child)!=dict and type(child)!=list:
                        update_context({key:child})

                    # path 放在参数里面
                    ans.update({key:eval_tree(child)})
            until=eval_tree(until)
            if until:
                break

        return ans


def run_file(args):
    '''
    run a yml file. parse the file to dict and run it

    :param filename:
    :return:
    '''
    filename=args['filename']
    algorithm= load(filename)

    # 开始和结束都重置context
    set_context({})

    ans=eval_tree(algorithm)
    print ans

    set_context({})

    return ans


def run(args):
    run_file(args)
    return True

