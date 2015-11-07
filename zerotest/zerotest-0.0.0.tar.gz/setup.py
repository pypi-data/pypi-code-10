#!/usr/bin/env python

from setuptools import setup

setup(name='zerotest',
      version='0.0.0',
      description='Capture HTTP request/response and replay it for the test purpose',
      author='Hari Jiang',
      author_email='hari.jiang@outlook.com',
      license='MIT',
      packages=['zerotest'],
      install_requires=[
          'requests>=2.2.1',
          'Werkzeug>=0.10.4',
      ],
      entry_points={
          'console_scripts': [
              'zerotest=zerotest.cli:main',
          ],
      },
      )
