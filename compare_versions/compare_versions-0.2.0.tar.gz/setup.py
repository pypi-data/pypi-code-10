#!/usr/bin/env python

from setuptools import setup, find_packages
import os.path

# Get version
with open('compare_versions/version.py') as f:
    exec(f.read())

# Get documentation
def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name = 'compare_versions',
    version = __version__,
    author = 'Luke Yeager',
    author_email = 'luke.yeager@gmail.com',
    url = 'https://github.com/lukeyeager/compare-versions',
    description = 'Compare versions using various versioning schemes',
    long_description = readme(),
    scripts = [
        'bin/compare_versions',
    ],
    packages = find_packages(exclude=['tests', 'tests.*']),
    test_suite = 'tests',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
