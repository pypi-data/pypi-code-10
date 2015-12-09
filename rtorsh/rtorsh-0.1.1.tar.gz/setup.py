#!/usr/bin/env python3

from distutils.core import setup

setup(name='rtorsh',
      version='0.1.1',
      description='CLI Interface to rtorrent',
      author='Seth Curry',
      author_email='seth@scurry.io',
      scripts=['rtorsh'],
      packages=['rtorshlib'],
      install_requires=['pyrtor']
      )
