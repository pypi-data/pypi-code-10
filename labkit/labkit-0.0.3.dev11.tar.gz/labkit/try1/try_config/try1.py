#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from oslo_config import cfg


common_opts = [
    cfg.StrOpt('bind_host',
               default='0.0.0.0',
               help='IP address to listen on.'),
]
conf=cfg.ConfigOpts()

from oslo_config.cfg import *
# def add_parsers(subparsers):
#     list_action = subparsers.add_parser('list')
#     list_action.add_argument('id')
# conf.register_cli_opt(SubCommandOpt('action', handler=add_parsers))
# conf(args=['list', '10'])
# print(conf.action.name, conf.action.id)

# ==== 注册配置项
conf.register_opts(common_opts)

# === 设置配置文件, 初始设置, 可以设置多个, 后面的覆盖前面的.
conf(default_config_files=['try1.ini'])
# try.ini里面的DEFAULT一定要大写. 其他的分组类似, 区分大小写.
# 或者. conf(args=['--config-file','try.ini'])
# ==== 使用变量
print conf.bind_host
# print(conf.find_file('try1.ini'))   # find file 是获得绝对路径

# 组名和变量名重复的时候, 优先组名

# 全局的CONF 类似
CONF=cfg.CONF
CONF(default_config_files=['try1.ini'])
CONF.register_opts(common_opts)
# print CONF.bind_host




# === 设置组

conf.register_opts(common_opts,group='rabbit')
print conf.rabbit.bind_host





# ref:
# http://docs.openstack.org/developer/oslo.config/cfg.html#loading-config-files
# http://www.lihuai.net/program/python/1698.html
