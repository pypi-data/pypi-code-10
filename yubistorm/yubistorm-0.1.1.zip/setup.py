#!/usr/bin/env python
from distutils.core import setup
from yubistorm import __version__

setup(name='yubistorm',
      version=__version__,
      description='Asnychronous two factor authentication client for YubiCloud with Tornado',
      long_description="""Provides a simple module that can be used from a Tornado server to authenticate users """ +
                       """ with YubiCloud (https://www.yubico.com/products/services-software/yubicloud/)""",
      author='László Zsolt Nagy',
      author_email='nagylzs@gmail.com',
      license="LGPL v3",
      py_modules=['yubistorm'],
      requires=['tornado (>=4.3)'],
      url="https://bitbucket.org/nagylzs/yubistorm",
      classifiers=[
            'Topic :: Security', 'Topic :: Internet :: WWW/HTTP',
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: Implementation :: CPython",
            ],
      )
