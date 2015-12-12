#!/usr/bin/env python

from setuptools import setup
import os
import sys

setup_path = os.path.dirname(__file__)
tests_require = ['nose', 'mock']

if sys.version_info < (2, 7):
    tests_require.append('unittest2')

setup(
    name="shushuo",
    version="0.0.12",
    description="Python Client for ShuShuo.com",
    author="Kerwin",
    author_email="piaoyuankui@gmail.com",
    url="https://github.com/shushuo/shushuo.py",
    packages=["shushuo"],
    install_requires=[
        "requests",
        "urllib3"
    ],
    tests_require=tests_require,
)
