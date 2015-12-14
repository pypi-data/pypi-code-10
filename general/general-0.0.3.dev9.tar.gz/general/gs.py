#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# global space. 所有的global的量存在这里, 包括CONF, LOG, 等等, 只要是全局的, 都在这里. 以及不同形式的config, 提供yml形式加载到config的全局变量, 也提供标准的CONF方式.

import importlib
import os

import oslo_i18n
import yaml
from oslo_config import cfg, types
from oslo_log import log

from general.reflection import get_package_name, get_script_location
from general.smartlog import get_logger,set_root_logger
CONF=cfg.ConfigOpts()
# log=get_logger(__name__,level='DEBUG')
import  sys
def init(__file__,OPTS,argv=None):
    '''
    标准的init, 初始化CONF和LOG
    :param __file__:
    :param OPTS:
    :return:
    '''

    root_package_name=get_package_name(__file__)
    # print root_package_name
    root_package_folder=get_script_location(__file__)
    # print root_package_folder
    ROOT_PACKAGE_OPTS = [
        cfg.StrOpt('root_package_name',
                   default=root_package_name,
                   help='the root package name'),
        cfg.StrOpt('root_package_folder',
                   default=root_package_folder,
                   help='the root package name'),
        ]

    # done: important! 这里暂时设置为空, oslo.config强制检查argv, 最好是让他不检查
    # done: 暂时使用backup_argv过后再还原的方式.
    backup_argv=[]
    backup_argv[:]=sys.argv
    sys.argv[1:]=[]


    CONF_FILE=root_package_name+'.conf'
    global get_logger
    # print __file__
    CONF.register_opts(ROOT_PACKAGE_OPTS)
    CONF.register_opts(OPTS)
    # which_log='oslo'
    which_log='smartlog'

    if which_log=='smartlog':
        OPTS = [
            # DEBUG False的时候会计算all.
            cfg.BoolOpt('debug',
                        default=True,
                        help='debug toggle')
        ]
        CONF.register_opts(OPTS)

        # todo: root level改了没用, 另外这一段需要在configfile之后才好.
        if CONF.debug:
            log_level="DEBUG"
        else:
            log_level="WARNING"
        # log的名字空间是全局的, 只根据名字来分级. 因此根log只要建立一下就行了.
        # LOG=get_logger(name=CONF.root_package_name,level=log_level,console=True)
        # 直接用root, 不然捕获不了general的信息. 默认的format在smartlg里面有. 需要的时候再在这里设置.
        set_root_logger(level=log_level)
    elif which_log=='oslo':
        oslo_i18n.enable_lazy()
        log.register_options(CONF)
        log_levels = (CONF.default_log_levels+
                      ['loader=ERROR'])
        # todo: oslo log格式如何调整. 以及如何设置各个log的级别.
        # done: 暂时使用自己的log
        log.set_defaults(default_log_levels=log_levels)
        log.setup(CONF, CONF.root_package_name)
        get_logger=log.getLogger
    else:
        print("please set which log system to use")
        exit(0)


    script_location=get_script_location(__file__)
    # log.debug(script_location)
    config_files=[os.path.join(script_location,CONF_FILE)]
    # importlib.import_module("stock.version")

    version=importlib.import_module(CONF.root_package_name+'.version')
    if argv is None:
        argv = sys.argv

    CONF(args=None,project=CONF.root_package_name, validate_default_values=False,
         version=version.version_info.version_string(),
         default_config_files=config_files)

    sys.argv[:]=backup_argv[:]

    # CONF.

def check_config(filename):
    '''
    非标准, 使用yml直接加载变量到config的名字空间
    :param filename:
    :return:
    '''

    CONFIG=yaml.load(open(filename,'r'))

    for keyword in CONFIG:
        globals()[keyword]=CONFIG[keyword]


# print 'gs loaded'

