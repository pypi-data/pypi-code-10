#!/usr/bin/env python
import os
from setuptools import setup, find_packages

version = os.getenv('PYTHON_PACKAGE_VERSION')
if version is None:
    try:
        from packageversion import PackageVersion
        pv = PackageVersion()
        version = pv.generate_next_stable(package_name='packageversion')
    except ImportError:
        version = '1.0.0'

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
