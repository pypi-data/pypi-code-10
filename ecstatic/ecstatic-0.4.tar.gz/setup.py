#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='ecstatic',
      version='0.4',
      description='A small flask application to serve files.',
      long_description=read('README.rst'),
      author='Marc Brinkmann',
      author_email='git@marcbrinkmann.de',
      url='https://github.com/mbr/ecstatic',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      install_requires=['flask', 'flask-appconfig<0.12'],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ])
