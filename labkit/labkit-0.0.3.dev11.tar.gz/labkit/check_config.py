#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from copy import deepcopy
import os

import yaml

from general import smartlog
from labkit.conformer.conformer import Conformer
from general.reflection import get_script_location

script_location=get_script_location(__file__)
config_location=os.path.join(script_location,'config.yaml')

def load_config(filename=config_location):
    # todo: 读取配置文件
    # todo: 读取模板分别放在inner和inter里面, 然后去判断. 调试load
    # todo: 全局变量还有一些问题, 在模块组合的时候如何处理配置的名字空间, 以及函数如何引用配置选项

    CONFIG=yaml.load(open(filename,'r'))

    conf={}
    for keyword in CONFIG:
        conf[keyword]=CONFIG[keyword]

    newbackbone=[]
    for item in conf['BACKBONE_TEMPLATE']:
        newitem={}
        newitem['dihedral_name']=item[2]
        newitem['residue']=item[0]
        newitem['residue_number']=int(item[1])
        # todo: config字符串和数字的处理.
        newitem['dihedral_list']=item[3]
        newbackbone.append(deepcopy(newitem))
        # del newitem

    conf['BACKBONE_TEMPLATE']=newbackbone

    if conf.get('USE_BOND_TEMPLATE',False):

        standard_pdb_filename=conf.get('USE_BOND_TEMPLATE')
        cc=Conformer().load(standard_pdb_filename,'xyz')

        INNER_RESIDUE_BONDING_TEMPLATE=cc.extract_inner_bonds()
        print INNER_RESIDUE_BONDING_TEMPLATE




def check_config(filename=config_location):
    # todo: 读取配置文件
    # todo: 读取模板分别放在inner和inter里面, 然后去判断. 调试load
    # todo: 全局变量还有一些问题, 在模块组合的时候如何处理配置的名字空间, 以及函数如何引用配置选项
    global CONFIG,SEQ,BACKBONE_TEMPLATE,SIDE_TEMPLATE,DIHEDRAL_DEFINITION,INNER_RESIDUE_BONDING_TEMPLATE,INTER_RESIDUE_BONDING_TEMPLATE
    global CONFIG
    Polypeptide.logger=smartlog.get_logger(level='DEBUG')

    CONFIG=yaml.load(open(filename,'r'))

    for keyword in CONFIG:
        globals()[keyword]=CONFIG[keyword]

    newbackbone=[]
    for item in BACKBONE_TEMPLATE:
        newitem={}
        newitem['dihedral_name']=item[2]
        newitem['residue']=item[0]
        newitem['residue_number']=int(item[1])
        # toso: config字符串和数字的处理.
        newitem['dihedral_list']=item[3]
        newbackbone.append(deepcopy(newitem))
        # del newitem
    BACKBONE_TEMPLATE=newbackbone
    print globals().get('USE_BOND_TEMPLATE',False)
    if globals().get('USE_BOND_TEMPLATE',False):

        standard_pdb_filename=globals().get('USE_BOND_TEMPLATE')
        cc=Conformer().load(standard_pdb_filename,'xyz')
        print cc.dumps()
        pep=Polypeptide.build_from_conformer(cc)
        Polypeptide.logger.debug(pep)
        INNER_RESIDUE_BONDING_TEMPLATE=pep.extract_inner_bonds()
        print INNER_RESIDUE_BONDING_TEMPLATE
        # fefe
# print TEMPLATE.dumps()
# print TEMPLATE.dumps()

# check_config()

# print BACKBONE_TEMPLATE



#
#
# CONNECTION_STRING = "mongodb://210.45.66.91"  # replace it with your settings
# CONNECTION = pymongo.MongoClient(CONNECTION_STRING)
#
# '''Leave this as is if you dont have other configuration'''
# DATABASE = CONNECTION.databank
# POSTS_COLLECTION = DATABASE.posts
# APPLICATIONS_COLLECTION = DATABASE.applications
# USERS_COLLECTION = DATABASE.users
# SETTINGS_COLLECTION = DATABASE.settings
# MOLECULES_PATH='databank'
#
# MAIL_SERVER = 'mail.ustc.edu.cn'
# MAIL_PORT =  25
# MAIL_USE_TLS = False
# MAIL_USE_SSL = False
# MAIL_USERNAME = 'lhrkkk@mail.ustc.edu.cn'
# MAIL_PASSWORD = 'starnada'
# DEFAULT_MAIL_SENDER = 'lhr'
#
#
# SECRET_KEY = ""
# basedir = os.path.abspath(os.path.dirname(__file__))
# secret_file = os.path.join(basedir, '.secret')
# if os.path.exists(secret_file):
#     # Read SECRET_KEY from .secret file
#     f = open(secret_file, 'r')
#     SECRET_KEY = f.read().strip()
#     f.close()
# else:
#     # Generate SECRET_KEY & save it away
#     SECRET_KEY = os.urandom(24)
#     f = open(secret_file, 'w')
#     f.write(SECRET_KEY)
#     f.close()
#     # Modeify .gitignore to include .secret file
#     gitignore_file = os.path.join(basedir, '.gitignore')
#     f = open(gitignore_file, 'a+')
#     if '.secret' not in f.readlines() and '.secret\n' not in f.readlines():
#         f.write('.secret\n')
#     f.close()
#
# LOG_FILE = "app.log"
#
# DEBUG = True  # set it to False on production
