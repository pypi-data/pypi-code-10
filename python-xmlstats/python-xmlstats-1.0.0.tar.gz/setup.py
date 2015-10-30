#!/usr/bin/env python
from setuptools import setup
from xmlstats import __version__

setup(
  name = 'python-xmlstats',
  packages = ['xmlstats'],
  version = __version__,
  description = 'Client for https://erikberg.com/api',
  author = 'Serbokryl Oleg',
  author_email = 'chezar1995@gmail.com',
  url = 'https://github.com/Krokop/python-xmlstats',
  download_url = 'https://github.com/Krokop/python-xmlstats/tarball/0.14',
  keywords = ['NBA stas api', 'xmlstats', 'NBA API', 'nba api stats'],
  classifiers = [],
  install_requires=[],
)
