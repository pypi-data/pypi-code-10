#!/usr/bin/env python

from setuptools import setup

import io
import os

here = os.path.abspath(os.path.dirname(__file__))

def read(fname):
    with io.open(os.path.join(here, fname), encoding='utf-8') as f:
        return f.read()

setup(
    name='pypi-rst-ref',
    version='0.0.2',
    description="A reference for how reStructuredText blocks are rendered by "
                "Github and PyPI.",
    long_description=read('README.rst') + read('CHANGES.rst'),

    url='https://github.com/moreati/pypi-rst-ref',

    author='Alex Willmer',
    author_email='alex@moreati.org.uk',

    license='Apache 2.0',

    py_modules=['pypi_rst_ref'],
)
