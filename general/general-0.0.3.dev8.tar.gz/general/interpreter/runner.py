#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# from __future__ import print_function
import os
import re
import sys

from commutils.reflection import get_script_location
from labkit.task.loader import call, load

# filename=sys.argv[1]
filename="proto.yml"
folder=get_script_location(__file__)
filename=os.path.join(folder,filename)

conf= load(filename)
print conf
print "------------------"

# name="sample.ga"
# name='labkit.'+name
# __import__(name)


def ismodule(name):
    try:
        name='labkit.'+name
        lib=__import__(name)
        return lib
        # lib.run(load(i+'.yml'))
    except:
        return 0
    # return ['sample','cut','merge']

def parse(conf):
    # print type(conf)
    if type(conf)!=dict and type(conf)!=list:
        return conf
    if type(conf)==list:
        ans=[]
        for item in conf:
            # print item
            ans.append(parse(item))
        return ans
    else:
        ans={}
        for key in conf.keys():
            child=conf[key]
            # print key, child

            # if type(child)!=dict and type(child)!=list:
                # print child
                # ans.update({key,child})
                # return child
            # if type(child)==list:
                # ans.update(key,run(child))
            # else:
            if ismodule(key):
                print key ,child
                # print call(key,parse(child))
                ans.update({key:call(key,parse(child))})
            else:
                ans.update({key:parse(child)})

    return ans

a= parse(conf)
print "===================="
print a

# ans={}
# ans.update({1:2})
# ans.update({3:4})
# print ans
