#!/usr/bin/env python
from __future__ import unicode_literals

import logging
import subprocess
import sys

from setuptools import Command
from setuptools import find_packages, setup

from zerotest.common import init_logging_config

init_logging_config()

LOG = logging.getLogger(__name__)

description = "Lazy guy's testing tool. Capture HTTP traffic and generate python integration test for your API server."

try:
    long_description = subprocess.check_output(["pandoc", "README.md", "-f", "markdown", "-t", "rst"]).decode('utf-8')
except (OSError, subprocess.CalledProcessError) as e:
    LOG.error("call pandoc error: %s", e)
    LOG.warning("failed convert README from markdown to rst, read as text")
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
      version='1.2.0',
      long_description=long_description,
      description=description,
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
          'pytest>=2.8.3',
          'six>=1.10.0',
      ],
      entry_points={
          'console_scripts': [
              'zerotest=zerotest.cli:main',
          ],
      },
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Testing',
          'Topic :: Utilities',
      ],
      )
