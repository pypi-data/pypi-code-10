#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='secondguard',
      version='1.1.10',
      description='SecondGuard API & Encryption Library',
      author='Michael Flaxman',
      author_email='mflaxman+secondguard@gmail.com',
      url='https://github.com/secondguard/secondguard-python/',
      install_requires=[
          'requests==2.8.1',
          'pycrypto==2.6.1',
          ],
      packages=['secondguard'],
      include_package_data=True,
      package_data={"": ["LICENSE"]},
      )
