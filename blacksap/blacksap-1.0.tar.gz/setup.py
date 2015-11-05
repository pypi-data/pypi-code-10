#!/usr/bin/env python
# coding=utf-8
"""Setup script for blacksap project"""

from setuptools import setup
from distutils.util import get_platform

setup(name='blacksap',
      version='1.0',
      description='Watch Torrent RSS feeds and download new files',
      author='Jesse Almanrode',
      author_email='jesse@almanrode.com',
      url='https://bitbucket.org/isaiah1112/blacksap',
      py_modules=['blacksap'],
      license='GNU General Public License v3 or later (GPLv3+)',
      install_requires=['Click>=5.1',
                        'feedparser>=5.2.1',
                        'requests>=2.8.1',
                        'colorama>=0.3.3',
                        ],
      platforms=get_platform(),
      entry_points="""
            [console_scripts]
            blacksap=blacksap:cli
      """,
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Development Status :: 5 - Production/Stable',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          ],
      )
