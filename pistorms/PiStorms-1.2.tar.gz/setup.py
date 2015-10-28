#!/usr/bin/env python

from distutils.core import setup

setup(name='PiStorms',
    version='1.2',
    description='PiStorms libraries',
    author='mindsensors.com',
    author_email='contact@mindsensors.com',
    url='http://www.mindsensors.com',
    py_modules=['PiStorms', 'mindsensors', 'PiStormsBrowser', 'PiStormsCom', 'PiStormsDriver', 'ps_messenger_check'],
    install_requires=['mindsensors_i2c', 'mindsensorsUI'],
    )