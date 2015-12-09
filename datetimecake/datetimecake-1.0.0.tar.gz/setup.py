# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'datetimecake',
    'datetimecake.cake'
]

setup(
    name='datetimecake',
    version='1.0.0',
    description='This is datetimecake',
    author_email='mr.zhuqipeng@gmail.com',
    packages=packages,
    author='Mr.zhu'
)
