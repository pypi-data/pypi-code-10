#!/usr/bin/env python
# The MIT License (MIT)
#
# Copyright (c) 2015 Robin Wilson (robin@rtwilson.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from setuptools import setup

reqs = ['numpy', "python-dateutil"]

setup(
        name                  = "vanHOzone",
        packages              = ['vanHOzone'],
        install_requires      = reqs,
        version               = "1.0.0",
        author                = "Robin Wilson",
        author_email          = "robin@rtwilson.com",
        description           = ("An implementation of the van Heuklon (1979) Ozone model, for estimating atmospheric ozone concentration given a latitude, longitude and datetime."),
        license               = "MIT",
        url                   = "https://pypi.python.org/pypi/vanHOzone",
        long_description      = ("An implementation of the van Heuklon (1979) Ozone model, for estimating atmospheric ozone concentration given a latitude, longitude and datetime."),
        classifiers           =[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2"
        ],
)
