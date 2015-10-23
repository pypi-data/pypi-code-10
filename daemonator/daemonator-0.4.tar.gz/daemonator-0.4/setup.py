#!/usr/bin/env python
# encoding: utf-8
import sys
from os import path
from distutils.core import setup
from distutils.util import get_platform

from daemonator import __author__, __author_email__, __copyright__, __package__, __version__, __version_info__

"""Verify Python platform is Linux."""
platform = get_platform()
if platform.startswith('linux') == False:
    sys.stderr.write("Daemonator is not compatible with %s\n" % platform)
    sys.exit(1)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.txt')) as f:
    long_description = f.read()

setup(
    name='daemonator',
    version='0.4',
    description='Lightweight and no-nonsense POSIX daemon library for Python (2.x.x/3.x.x)',
    long_description=long_description,
    author='Flávio Pontes',
    author_email='flaviopontes@acerp.org.br',
    license='MIT/X11',
    platforms='Linux',
    url='https://github.com/flaviocpontes/daemonator',
    download_url='https://github.com/flaviocpontes/daemonator/tarball/0.4',
    package_dir={'daemonator': 'src/3.x.x'},
    package_data={'README': 'README.rst'},
    py_modules=[
        'daemon',
        ],
)