#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


# Use semantic versioning: MAJOR.MINOR.PATCH
version = '0.1.0'


def get_requires():
    with open('requirements.txt', 'r') as f:
        requires = [i for i in map(lambda x: x.strip(), f.readlines()) if i]
    return requires


def get_long_description():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    # license='License :: OSI Approved :: MIT License',
    name='colordesk',
    version=version,
    author='reorx',
    author_email='novoreorx@gmail.com',
    description='A format & renderer for color palette',
    url='https://github.com/reorx/colordesk',
    long_description=get_long_description(),
    packages=find_packages(),
    install_requires=get_requires(),
    # package_data={}
    entry_points={
        'console_scripts': [
            'colordesk = colordesk.cli:main'
        ]
    }
)
