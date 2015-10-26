#!/usr/bin/env python
"""Setup script."""
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'Max Arnold <arnold.maxim@gmail.com>'
__version__ = '1.0.1'


setup(
    name='block-disposable-email',
    version=__version__,

    # Package dependencies.

    # Metadata for PyPI.
    author='Max Arnold',
    author_email='arnold.maxim@gmail.com',
    license='BSD',
    url='http://github.com/max-arnold/python-block-disposable-email',
    keywords='block disposable email domains',
    description='Python client for block-disposable-email.com',
    long_description=open(
        os.path.abspath(os.path.join(os.path.dirname(__file__),
                        'README.md')
                        ),
        'r'
        ).read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: System Administrators",
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet'
    ],
    packages=['bdea'],
    platforms='any',
)
