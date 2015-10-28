#!/usr/bin/env python

from distutils.core import setup

setup(name='mindsensorsUI',
    version='1.0',
    description='mindsensorsUI library',
    author='mindsensors.com',
    author_email='support@mindsensors.com',
    url='http://www.mindsensors.com',
    py_modules=['mindsensorsUI'],
    install_requires=['mindsensors_i2c'],
    )