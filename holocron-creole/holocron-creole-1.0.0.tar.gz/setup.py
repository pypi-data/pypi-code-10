#!/usr/bin/env python
# coding: utf-8

import os

from io import open
from setuptools import setup, find_packages

from holocron_creole import __version__ as version
from holocron_creole import __license__ as license


here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='holocron-creole',
    version=version,

    description='A creole markup converter for Holocron',
    long_description=long_description,
    license=license,
    url='http://github.com/ikalnitsky/holocron-creole/',
    keywords='blog generator static creole wiki',

    author='Igor Kalnitsky',
    author_email='igor@kalnitsky.org',

    packages=find_packages(exclude=['tests*']),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'holocron >= 0.1.1',
        'python-creole >= 1.3.1',
    ],

    entry_points={
        'holocron.ext': [
            'creole = holocron_creole.converter:Creole',
        ],
    },

    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',

        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Terminals',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
