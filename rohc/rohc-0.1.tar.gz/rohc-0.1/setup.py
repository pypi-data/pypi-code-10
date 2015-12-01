#!/usr/bin/env python

from distutils.core import setup, Extension
import sys

# check the system version because there was problems with version before
# 2.6
if sys.hexversion < 0x02060000:
    print "Version 2.6 or greater is recommended - edit setup.py to remove warning"
    sys.exit()

setup(name='ROHC',
      version='0.1',
      description='Python Robust Header Compression (ROHC) Module',
      author='Joseph Ishac',
      author_email='jishac@nasa.gov',
      ext_modules=[Extension('rohc', ['src/rohc.c'], libraries=['rohc'])],
      )

