#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

import importlib
# from __future__ import print_function
import os
import jinja2
import yaml

from general import gs
from general.reflection import get_script_location

log=gs.get_logger(__name__,level='INFO')

self_location = get_script_location(__file__)

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
    :param conf: 参数字典
    :return: run的返回值
    '''
    print("hello world this is loader")

# ROOT
# 可以使用import module & inspect 的方法获取func_name和func_definition

def load_module(name):
    '''
    load a module by lib name
    :param name:
    :return:
    '''
    try:
        # 暂时不允许使用root包以外的模块, 否则容易冲突.
        if name == 'general.interpreter.runner':
            lib=importlib.import_module(name)
            return lib
        else:
            raise ImportError
        # lib.run(load(i+'.yml'))
    except:
        try:
            name=gs.CONF.root_package_name+'.'+name
            log.debug("name is: "+name)
            lib=importlib.import_module(name)
            return lib
        except:
            return 0


def load_conf(libname,args={}):
    '''
    load conf by lib name
    优先加载当前目录下的module_settings, 否则加载默认的. args用来更新.
    :param libname:
    :param args:
    :return:
    '''

    conf={}
    root=gs.CONF.root_package_folder
    # print os.path.abspath(os.path.curdir)
    # log.debug("root_package_folder is: "+root)
    module_setting_folder_name='module_settings'
    try:
        if os.path.exists(module_setting_folder_name) and os.path.isdir(module_setting_folder_name):
            conf_file=os.path.join(module_setting_folder_name,libname+'.yml')
            conf=load(conf_file)
        elif os.path.exists(os.path.join(root,module_setting_folder_name)) and os.path.isdir(os.path.join(root,module_setting_folder_name)):
            conf_file=os.path.join(root,module_setting_folder_name,libname+'.yml')
            log.debug("conf_file is: "+conf_file)
            conf=load(conf_file)
    except:
        pass
    finally:
        conf.update(args)

    return conf

def load_self_conf(filename,args={}):
    '''
    filename should be __file__
    in a module itself, load conf by the arguments __file__
    same with load_conf_by_filename, but this is special for a in-module self load.
    :param filename:
    :return:
    '''
    # print os.path.realpath(filename)
    # print get_module_name(os.path.realpath(filename))
    return load_conf(get_module_name(os.path.realpath(filename)))


def load_conf_by_filename(filename):
    '''
    load_conf's arg is lib name, this function can load conf by filename
    :param filename:
    :return:
    '''
    return load_conf(get_module_name(filename))


def get_module_name(filename):
    '''
    get module/lib name by filename
    :param filename:
    :return:
    '''

    module_name=filename
    root=gs.CONF.root_package_name
    splited=module_name.split(root+'/')
    log.debug("splited is: "+str(splited))
    ans= splited[-1].split('/')
    ans[-1]=ans[-1].replace('.pyc','')
    ans[-1]=ans[-1].replace('.py','')
    ans='.'.join(ans)
    return ans

from general.interpreter.context import get_context

# ----------
def call(libname,args):
    '''
    call a lib's run function with args.
    根据模块名字调用模块的run函数, 并且加载同名配置文件, 并合并传入的参数

    :param libname: 模块名
    :param args: 传入的参数字典, dict
    :return: 模块run函数的返回值
    '''
    lib=load_module(libname)

    # 用context更新args, 在push_to_compute里面更新
    # args.update(get_context())
    # print get_context()

    # 用args更新conf
    conf=load_conf(libname,args)
    print (conf)
    log.info("calling %s..."%libname)
    print (lib)
    return lib.run(conf)


def callrun(filename,args={}):
    '''
    in a module itself, call the 'run' entry point in the argument 'filename', __file__
    根据__file__得到脚本的模块名字. 然后用call调用它.
    :param filename: full file path and name, please simplely use __file__
    :param args:
    :return:
    '''
    ans=get_module_name(filename)


    log.debug("ans is: "+ans)
    call(ans,args)


if __name__ == '__main__':
    import general.init_gs
    # from general.interpreter.loader import callrun
    print __file__
    callrun(__file__)
