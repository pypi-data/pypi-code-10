#!/usr/bin/env python
from distutils.core import setup
from clefstorm import __version__

setup(name='clefstorm',
      version=__version__,
      description='Asnychronous two factor authentication client for Clef with Tornado',
      long_description="""Provides a simple module that can be used from a Tornado server to authenticate users """ +
                       """ with Clef (www.getclef.com)""",
      author='László Zsolt Nagy',
      author_email='nagylzs@gmail.com',
      license="LGPL v3",
      py_modules=['clefstorm'],
      requires=['tornado (>=4.3)'],
      url="https://bitbucket.org/nagylzs/clefstorm",
      classifiers=[
            'Topic :: Security', 'Topic :: Internet :: WWW/HTTP',
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: Implementation :: CPython",
            ],
      )
