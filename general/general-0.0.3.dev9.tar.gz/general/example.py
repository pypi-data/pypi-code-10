#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


# 项目结构, general, module_config 和模块
# 三步走, 1. import gs和log, 2. 设置run, 3. 运行时import init_gs一次, 然后callrun
# debug 在模块种独立设置, 默认的level都是info           //maybe_todo:debug 设置有两档, 一档是默认跟全局, 另一档是, 自己设置

# # log的标准用法,配合callrun使用. (因为需要被导入才能够正确识别模块名)
# from general import gs
# log=gs.get_logger(__name__,debug=False)
#
# class Example(object):
#     def __init__(self):
#         pass
#
#     def run(self):
#         print "hello world"
#
# # run的标准定义
# def run(conf):
#     # 从这里开始可以用gs.CONF, 初始化log
#     app=Example()
#     app.run()
#
# # main的标准定义
# if __name__ == '__main__':
#     # 可以试着把init放在每个模块的开头, 虽然没有必要.
#     import general.init_gs
#     from general.interpreter.loader import callrun
#     callrun(__file__)
#


# 去掉注释的最简化版本

from general import gs
log=gs.get_logger(__name__,debug=False)

def run(conf):
    print "hello world"

if __name__ == '__main__':
    import general.init_gs
    from general.interpreter.loader import callrun
    callrun(__file__)

