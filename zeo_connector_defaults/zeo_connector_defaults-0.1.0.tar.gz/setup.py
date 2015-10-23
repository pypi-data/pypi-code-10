#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup
from setuptools import find_packages


# Variables ===================================================================
changelog = open('CHANGELOG.rst').read()
long_description = "\n\n".join([
    open('README.rst').read(),
    changelog
])


# Functions ===================================================================
def allSame(s):
    return not any(filter(lambda x: x != s[0], s))


def hasDigit(s):
    return any(char.isdigit() for char in s)


def getVersion(data):
    """
    Parse version from changelog written in RST format.
    """
    data = data.splitlines()
    return next((
        v
        for v, u in zip(data, data[1:])  # v = version, u = underline
        if len(v) == len(u) and allSame(u) and hasDigit(v) and "." in v
    ))


# Actual setup definition =====================================================
setup(
    name='zeo_connector_defaults',
    version=getVersion(changelog),
    description="Default conf. files and conf. file generator for `zeo_connector`.",
    long_description=long_description,
    url='https://github.com/Bystroushaak/zeo_connector_defaults',

    author='Bystroushaak',
    author_email='bystrousak@kitakitsune.org',

    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",

        "License :: OSI Approved :: MIT License",
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    scripts=[
        'bin/zeo_connector_gen_defaults.py',
    ],

    zip_safe=False,
    include_package_data=True,
)
