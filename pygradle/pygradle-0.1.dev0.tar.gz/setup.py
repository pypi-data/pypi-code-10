#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Setuptools script for building pytractor.
"""

from setuptools import setup, find_packages

setup(
    name='pygradle',
    version='0.1.dev0',
    description='Python gradle wrapper',
    url='https://github.com/mwalkowski/pygradle',

    author='Michal Walkowski',
    author_email='mi.walkowski@gmail.com',
    license='Apache 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Compilers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='java gradle',
    package_dir={'': 'src'},
    packages=find_packages('src'),

    tests_require=[
        'nose>=1.3.7',
    ],
    test_suite='nose.collector',
    use_2to3=True
)