#!/usr/bin/env python
# encoding: utf-8
import sys
from os import path
from setuptools import setup, find_packages
from distutils.util import get_platform

from daemonator import __author__, __author_email__, __copyright__, __package__, __version__

"""Verify Python platform is Linux."""
platform = get_platform()
if platform.startswith('linux') == False:
    sys.stderr.write("Daemonator is not compatible with %s\n" % platform)
    sys.exit(1)

if sys.version_info < (3,):
    sys.stderr.write("Daemonator is not compatible with Python %s.%s\n" % (sys.version_info[0], sys.version_info[1]))
    sys.exit(1)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='daemonator',
    version=__version__,
    description='Lightweight and no-nonsense POSIX daemon library for Python (2.x.x/3.x.x)',
    long_description=long_description,
    author=__author__,
    author_email=__author_email__,
    copyright=__copyright__,
    license='MIT/X11',
    packages=[__package__, ],
    platforms='Linux',
    url='https://github.com/flaviocpontes/daemonator',
    download_url='https://github.com/flaviocpontes/daemonator/tarball/0.4.1',
    package_data={'': ['README.rst',]},
)