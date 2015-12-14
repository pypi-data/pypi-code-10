#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# to use the live develop version of this lib, just add the path to the PYTHONPATH environment variable.


import os,sys
import time

def time_count(function, *args, **kwargs):
    tStart = time.time()#計時開始

    ans=function(*args,**kwargs)

    tEnd = time.time()#計時結束
    #列印結果
    print "[ %s ] cost %f sec" % (function.__name__,tEnd - tStart)#會自動做近位
    # print tEnd - tStart#原型長這樣
    return ans

def print_time(fun):
    start = time.clock()
    fun()
    elapsed = (time.clock() - start)
    print("Time used:",elapsed)

def import_path(path):
    '''import path to python's sys.path
    '''
    if not path in sys.path:
        sys.path.append(path)

if __name__ == '__main__':
    pass
