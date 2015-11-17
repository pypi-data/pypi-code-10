#!/usr/bin/env python
import os
from setuptools import setup, find_packages


def version():
    v = os.getenv('PYTHON_PACKAGE_VERSION')
    if v is None:
        from package_version import PackageVersion
        pv = PackageVersion()
        v = pv.generate_next_stable(package_name='package-version')
    return v

setup(name='package-version',
      version=version(),
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
      url='https://github.com/Yuav/python-package-version',
      packages=find_packages(),
      install_requires=[
          'semantic_version',
          'flexmock'
      ],
      setup_requires=[
          'package_version'
      ]
      )
