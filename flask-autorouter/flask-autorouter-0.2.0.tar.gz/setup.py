#!/usr/bin/env python
"""
    Flask AutoRouter -- a utility for generating flask URL routing

    Copyright (c) 2015 Daniel Pepper

    The MIT License (MIT)

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

__author__ = 'dpepper'
__version__ = '0.2.0'

import setuptools


if __name__ == "__main__":
    setuptools.setup(
        name="flask-autorouter",
        version=__version__,
        url="https://github.com/d1hotpep/flask_autorouter",
        license="MIT",
        author="Daniel Pepper",
        author_email="pepper.daniel@gmail.com",
        description="a utility for generating flask URL routing",
        long_description=open('README.txt').read(),
        platforms="any",

        packages=[
            "flask_autorouter",
        ],

        install_requires=[
            "flask",
            "bson",
        ],

        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Development Status :: 2 - Pre-Alpha",
            "Programming Language :: Python",
            "Topic :: Utilities",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
            "Operating System :: OS Independent",
            "Natural Language :: English",
        ],
    )
