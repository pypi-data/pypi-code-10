#!/usr/bin/env python

"""
This is a setup script for pyROSE -- A Python Package for Rank Ordering of Super-Enhancers

This code is free software; you can redistribute it and/or modify it under the terms of the 
BSD License (see the file COPYING included with the distribution).

@version: 1.0
@author: Aziz Khan
@email: khana10@mails.tsinghua.edu.cn
"""
import os
from distutils.core import setup
from setuptools import find_packages

#VERSION = __import__("ipsea").__version__

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
]

setup(
    name="pyrose",
    description="A Python Package for Rank Ordering of Super-Enhancers",
    version=1.04,
    author="Aziz Khan",
    Keywords= "bioinformatics,genomics",
    author_email="khana10@mails.tsinghua.edu.cn",
    url="https://github.com/asntech/pyrose",
    package_dir={'pyrose': 'pyrose'},
    packages=['pyrose'],
    scripts=['pyrose/pyrose','pyrose/geneMapper','pyrose/bamToGFF','pyrose/callSuper.R',
                   ],
    package_data={'annotation': ['annotation/*.ucsc'], 'readme':['README.md']},
    include_package_data=True,
    classifiers=CLASSIFIERS,
)
