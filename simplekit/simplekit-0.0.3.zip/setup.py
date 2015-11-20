#!/usr/bin/env python

__author__ = "benjamin.c.yan"

import os
import re
import sys

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'simplekit',
    'simplekit.objson'
]

requires = []

version = ''
with open('simplekit/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='simplekit',
    version=version,
    description='A simple and brief utility tools framework',
    long_description="A simple and brief utility tools framework",
    author='Benjamin Yan',
    author_email='ycs_ctbu_2010@126.com',
    url='https://github.com/by46/simplekit',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'simplekit': 'simplekit'},
    include_package_data=True,
    install_requires=requires,
    license='The MIT License',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)