#!/usr/bin/env python

from setuptools import setup

setup(
    name='colibri2trilegal',
    author='Phil Rosenfield',
    author_email='philip.rosenfield@cfa.harvard.edu',
    version='2.11',
    url='https://github.com/philrosenfield/colibri2trilegal',
    py_modules=['colibri2trilegal'],
    scripts=['colibri2trilegal'],
    install_requires=['matplotlib', 'numpy']
)
