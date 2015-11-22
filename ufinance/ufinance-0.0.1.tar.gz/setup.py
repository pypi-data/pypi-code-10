# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='ufinance',
    version='0.0.1',
    description='UNIST Finance Tool',
    author='Kyunghoon Kim',
    author_email='kyunghoon@unist.ac.kr',

    license = "MIT License",
    keywords = ['Finance', 'Stock', 'Pandas'],
    url = "https://github.com/koorukuroo/ufinance",
    packages=[
        'ufinance',
        ],
    install_requires=['pandas'],
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
