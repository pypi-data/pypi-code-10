#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='tinyrnnlm',
    version='0.1.0',
    author='m0rioka',
    author_email='miki16g@live.jp',
    url='https://bitbucket.org/m0rioka/tinyrnnlm',
    packages=['tinyrnnlm'],
    package_dir={
        'tinyrnnlm': 'tinyrnnlm'
    },
    install_requires=[
        'numpy',
        'scipy',
    ],
)
