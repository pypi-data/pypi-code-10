#!/usr/bin/env python
from __future__ import with_statement
import os
from setuptools import setup, find_packages

readme = 'README.md'
if os.path.exists('README.rst'):
    readme = 'README.rst'
with open(readme, 'rb') as f:
    long_description = f.read().decode('utf-8')

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(
    name='baidupy',
    version='0.0.5',
    author='hunter007',
    author_email='wentao79@gmail.com',
    url='https://github.com/hunter007/baidupy',
    packages=find_packages(),
    keywords='Baidu, baidu api, baidu SDK',
    description='baidupy: baidu SDK for Python',
    long_description=long_description,
    install_requires=requirements,
    include_package_data=True,
    tests_require=['nose', 'httmock'],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
