#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from general import gs
log=gs.get_logger(__name__,debug=False)

# 所有操作都是对统一数据模型进行操作, 所以只需要定义新的模块和run函数就行了.
# monkey_patch的函数就是无法自动补全, 那么只好尽量不要使用. 另外monkey_patch就不要分base和非base的了. 用到什么就import什么就行. 对于新增模块对conformer的补充, 就用monkey_patch的方式.



# ----------------

def test():
    pass

def run(args):
    '''
    ga

    :param args:
    :return:
    '''
    print "hello world"
    return True

def selfrun():
    import labkit.init_gs
    from general.interpreter.loader import callrun
    callrun(__file__)

if __name__ == '__main__':
    # test()
    selfrun()

