#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-19 18:02:41
# Filename        : setup.py
# Description     : 

from distutils.core import setup
import os

setup(
        name = 'cattle_qiniu',
        version = '0.0.2',
        author = 'tuxpy',
        author_email = 'q8886888@qq.com',
        license = 'GPL3',
        description = 'qiniu python sdk third party',
        url = '',
        packages = [
            'cattle',
            ]
        )

