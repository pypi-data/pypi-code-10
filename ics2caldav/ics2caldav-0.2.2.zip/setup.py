# -*- coding:utf-8 -*-
'''
Created on Nov 15, 2015

@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

from codecs import open
from os import path

from setuptools import setup, find_packages

import ics2caldav


BASE = path.abspath(path.dirname(__file__))

with open(path.join(BASE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ics2caldav',
    version=ics2caldav.__version__,
    url='https://github.com/wtayyeb/ics2caldav/',

    author='w.Tayyeb',
    author_email='tayyeb@tsaze.com',

    license='MIT',
    description=('Module to help importing .ics files to CalDAV server.'),
    long_description=long_description,

    packages=find_packages(),
    include_package_data=True,
    install_requires=['ics', 'caldav'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='ics caldav dav calendar',
)
