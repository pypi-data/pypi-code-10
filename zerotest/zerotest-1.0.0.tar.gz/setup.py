#!/usr/bin/env python

import sys

from setuptools import Command
from setuptools import find_packages, setup

with open('README.md') as fd:
    long_description = fd.read()


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(['tests'])
        sys.exit(errno)


setup(name='zerotest',
      version='1.0.0',
      long_description=long_description,
      description='Capture HTTP request/response and convert to test code.',
      author='Hari Jiang',
      author_email='hari.jiang@outlook.com',
      url='https://github.com/jjyr/zerotest',
      license='MIT',
      cmdclass={'test': TestCommand},
      platforms=['unix', 'linux', 'osx'],
      packages=find_packages(),
      install_requires=[
          'requests>=2.2.1',
          'Werkzeug>=0.10.4',
          'jinja2>=2.8',
          'pytest>=2.8.2',
      ],
      entry_points={
          'console_scripts': [
              'zerotest=zerotest.cli:main',
          ],
      },
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
      ],
      )
