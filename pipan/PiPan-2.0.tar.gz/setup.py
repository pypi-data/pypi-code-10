#!/usr/bin/env python

from distutils.core import setup

setup(name='PiPan',
    version='2.0',
    description='Mindsensors Pi-Pan library',
    author='mindsensors.com',
    author_email='contact@mindsensors.com',
    url='http://www.mindsensors.com/rpi/33-pi-pan',
    py_modules=['pilight', 'pipan'],
    install_requires=['mindsensors_i2c'],
    )