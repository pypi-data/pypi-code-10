#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

import importlib
# from __future__ import print_function
import os
import re

import jinja2
import yaml

from general import gs
from general.reflection import get_script_location

self_location = get_script_location(__file__)

log=gs.get_logger(__name__,level='INFO')



def load(filename):
    '''
    根据文件名加载yml配置文件, 先调用jinja模板渲染, 然后再解析. 最后返回解析后的字典.
    :param filename: 配置文件名
    :return: 解析后的字典
    '''
    f=open(filename,'r')
    # rendered= jinja2.Template(f.read()).render(jinja='jinjia2')
    rendered=f.read()
    conf=yaml.load(rendered)
    return conf
def run(conf):
    '''
    run必须有一个参数conf, 作为传入的配置.
    run是模块的入口
    :param conf:
    :return:
    '''
    print("hello world this is loader")


def call(name,args):
    '''
    根据模块名字调用模块的run函数, 并且加载同名配置文件, 并合并传入的参数
    :param name: 模块名
    :param args: 传入的参数
    :return: 模块run函数的返回值
    '''
    try:
        name=gs.CONF.root_package_name+'.'+name
        # 可以使用import module & inspect 的方法获取func_name和func_definition
        lib=importlib.import_module(name)
    except:
        return 0
    # print "=============",lib
    conf={}
    try:
        if os.path.exists('default') and os.path.isdir('default'):
            conf_file=os.path.join('default',name+'.yml')
            conf=load(conf_file)
        else:
            conf_file=os.path.join(self_location,"../default",name+'.yml')
            conf=load(conf_file)
    except:
        pass
    finally:
        conf.update(args)

    log.info("calling %s..."%name)
    # print (lib)
    return lib.run(conf)

def callrun(filename,args={}):
    '''
    in a module itself, call the 'run' entry point in the argument 'filename', __file__
    根据__file__得到脚本的模块名字. 然后用call调用它.
    :param filename: full file path and name, please simplely use __file__
    :param args:
    :return:
    '''
    module_name=filename
    splited=module_name.split(gs.CONF.root_package_name+'/')
    log.debug(splited)
    ans= splited[-1].split('/')
    ans[-1]=ans[-1].strip('.py')
    ans='.'.join(ans)
    call(ans,args)


if __name__ == '__main__':
    callrun(__file__)
