#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

"""
Usage:

    tmpelate.py  [-q | --quiet] [-l | --log] [-d | --debug]
    tmpelate.py (-h | --help)
    tmpelate.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   my tmpelate
"""

from docopt import docopt
import os, sys, re, sh
from glob import glob
import yaml, logging

import mypub, labkitpath
import crash_on_ipy
import mylog

from Bio.PDB.Structure import *

class Structure(Structure):
    def echo_methods(self):
        """ 输出类中所有的方法，以及doc 文档 """
        print "\n Method List: "
        for attrName in dir(self):
            attr = getattr(self,attrName)
            if callable(attr):
                print attrName,"():",attr.__doc__

    def echo_attributes(self):
        print "\n Attributes"

        for name in dir(self):
            attr = getattr(self,attr)
            if not callable(attr):
                print name,":",attr
