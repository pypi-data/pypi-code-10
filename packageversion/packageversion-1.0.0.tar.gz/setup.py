#!/usr/bin/env python
import os
from setuptools import setup, find_packages
try:
    from packageversion import PackageVersion
    pv = PackageVersion()
    v = pv.generate_next_stable(package_name='packageversion')
except ImportError:
    v = '1.0.0'

version = os.getenv('PYTHON_PACKAGE_VERSION', v)

setup(name='packageversion',
      version=version,
      description='Library to generate python package version for CI',
      author='Jon Skarpeteig',
      author_email='jon.skarpeteig@gmail.com',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      url='https://github.com/Yuav/python-packageversion',
      packages=find_packages(),
      install_requires=[
          'semantic_version',
          'flexmock'
      ]
      )
