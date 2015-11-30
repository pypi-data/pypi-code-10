#! /usr/bin/env python

import os

DESCRIPTION   = "Python plotting wrapper utilizing matplotlib and seaborn"

PKGNAME = 'plotenv'
MAINTAINER = 'Lento Manickathan'
MAINTAINER_EMAIL = 'lento.manickathan@gmail.com'
URL = 'https://github.com/lento234/plotenv',
LICENSE = 'GNU General Public License (GPL)'
VERSION = '0.0.2.dev1'

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

def check_dependencies():
    install_requires = []
    try:
        import numpy
    except ImportError:
        install_requires.append('numpy')
    try:
        import matplotlib
    except ImportError:
        install_requires.append('matplotlib')
    try:
        import seaborn
    except ImportError:
        install_requires.append('seaborn')

    return install_requires


if __name__ == "__main__":

    setup(name=PKGNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        keywords='python plotting wrapper',
        url=URL,
        version=VERSION,
        install_requires=check_dependencies(),
        packages=['plotenv'],
        classifiers=['Intended Audience :: Science/Research',
                     'License :: OSI Approved :: GNU General Public License (GPL)',
                     'Topic :: Scientific/Engineering :: Visualization',
                     'Operating System :: POSIX',
                     'Programming Language :: Python :: 2.7',
                     ])
