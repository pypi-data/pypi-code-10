#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import os
import re
import codecs
def read_version():
    version_file = codecs.open(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'zadarest/__init__.py'),
            'r', 'utf-8' ).read()
    return re.search( r"^__version__ = ['\"]([^'\"]*)['\"]",
            version_file, re.M ).group(1)

version = read_version()


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    "requests"
]

test_requirements = [
    "pytest",
    "httpretty",
    "sure"
]

setup(
    name='zadarest',
    version=version,
    description="python client library for accessing Zadara API",
    long_description=readme + '\n\n' + history,
    author="naomi maekawa",
    author_email='nmaekawa@g.harvard.edu',
    url='https://github.com/nmaekawa/zadarest',
    packages=find_packages(exclude=["docs", "tests*"]),
    package_dir={'zadarest': 'zadarest'},
    include_package_data=True,
    keywords='zadarest',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=requirements,
    tests_require=test_requirements,
    zip_safe=False,
)





