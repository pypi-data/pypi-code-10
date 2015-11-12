#!/usr/bin/env python
'''
Setup for devops
'''
from setuptools import setup, find_packages

setup(name='the_devops',
      version='1.0.0',
      description='A magic devops package',
      author='A shameful project by @davidjohngee',
      author_email='david.john.gee@gmail.com',
      url='https://github.com/davidjohngee/devops',
      packages=find_packages(),
      install_requires=[],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Networking'
      ])
