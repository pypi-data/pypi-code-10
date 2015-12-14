#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'aws-lambda-configurer',
          version = '0.1.0',
          description = '''aws-lambda-configurer - Resolve AWS lambda configuration from description field and other sources (e.g. s3)''',
          long_description = '''aws-lambda-configurer - Resolve AWS lambda configuration from description field and other sources (e.g. s3)''',
          author = "Jens Zastrow",
          author_email = "jens.zastrow_external@immobilienscout24.de",
          license = 'APACHE LICENSE, VERSION 2.0',
          url = 'https://github.com/Immobilienscout24/aws-lambda-configurer',
          scripts = [],
          packages = ['aws_lambda_configurer'],
          py_modules = [],
          classifiers = ['Development Status :: 4 - Beta', 'Environment :: Console', 'Intended Audience :: Developers', 'Intended Audience :: System Administrators', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Topic :: System :: Systems Administration'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "boto3", "isodate", "requests" ],
          
          zip_safe=True
    )
