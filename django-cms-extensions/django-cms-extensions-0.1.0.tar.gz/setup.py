#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='django-cms-extensions',
      version='0.1.0',
      description='Useful extensions for Django CMS',
      url='https://github.com/fscherf/django-cms-extensions',
      author='Florian Scherf',
      author_email='f.scherf@pengutronix.de',
      license='BSD',
      packages=['cms_extensions', 'cms_extensions/management'],
      zip_safe=False)
