#!/usr/bin/env python
"""Factorial project"""
from setuptools import find_packages, setup

setup(name = 'factorialexample',
    version = '1.0.0',
    description = "Factorial module.",
    long_description = "A test module for our book.",
    platforms = ["Linux"],
    author="yeching",
    author_email="yq08051035@163.com",
    url="http://pymbook.readthedocs.org/en/latest/",
    license = "MIT",
    packages=find_packages()
    )
