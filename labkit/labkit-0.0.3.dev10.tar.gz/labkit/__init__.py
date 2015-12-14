#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
# todo:
'''
#############################
原则:
开发基础组件和算法的时候, 全部import base_conformer, //错误, base是类继承的做法, monkey_patch只需要保留唯一的一个类就行了, 不要搞base了. 主体多放点, 然后需要什么import什么
如果需要别的模块的时候, 再import进来别的模块, 需要什么import什么
不要直接import conformer类, 只有在最外层功能实现的时候, 采用成品.

整体的架构以名词(数据)为核心, conformer, ensemble, 可以动态的加载模块.
实现开发测试模块化, 运行整体化, 解耦并且合体

解耦一个是要实现开发的解耦, 还有一个是实现不相关的独立的运行时之间用SOA解耦.
聚合是要把需要的功能封装, 内部要内聚. 不要放多余的功能在外部. 同时内部开发模块化.
有聚合才有分离. 就像聚类一样.
#############################
done:
docs, project document's base framework is done.
api, apache2 and mod_wsgi are needed, using pecan.deploy, it works. apache config file is in etc/apache2/labkit
接口设计补全, 见staruml
db. 目前是紧耦合.

-------------
todo:
api,config(oslo_config?)
conformer, gaussian, rq, 调节, 测试.
sys

frontend
前端参考re-com, re-frame, rt
chemdoodle(见_ref/markdown)

提供一些列的命令行工具.

------
next:
oslo_config, log
测试mock, fake90在bin目录下

wsme docs, paste

阅读: contact, markdown

'''
