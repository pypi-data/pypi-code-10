#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'ktail',
          version = '0.1.2',
          description = '''AWS Kinesis tail''',
          long_description = '''ktail - A tail for AWS Kinesis streams decoding JSON messages.''',
          author = "Marco Hoyer",
          author_email = "marco_hoyer@gmx.de",
          license = 'APACHE LICENSE, VERSION 2.0',
          url = 'https://github.com/marco-hoyer/ktail',
          scripts = ['scripts/ktail'],
          packages = ['kinesis_tail'],
          py_modules = [],
          classifiers = ['Development Status :: 4 - Beta', 'Environment :: Console', 'Intended Audience :: Developers', 'Intended Audience :: System Administrators', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Topic :: System :: Systems Administration'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "asyncio", "boto3", "click" ],
          
          zip_safe=True
    )
