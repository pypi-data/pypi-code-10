#!/usr/bin/env python

import os
from setuptools import setup
from spanner import __version__


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt'), 'r') as f:
        required = f.read().splitlines()

setup(
    name='spanner',
    version=__version__,
    description='An accumulation of utilities / convenience functions for python',
    author='Bryan Johnson',
    author_email='d.bryan.johnson@gmail.com',
    packages=['spanner'],
    url='https://github.com/dbjohnson/python-utils',
    download_url='https://github.com/dbjohnson/spanner/tarball/%s' % __version__,
    install_requires=required
)
