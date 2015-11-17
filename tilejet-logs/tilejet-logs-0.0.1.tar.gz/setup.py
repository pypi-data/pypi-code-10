#!/usr/bin/env python

from setuptools import setup

setup(
    name='tilejet-logs',
    version='0.0.1',
    install_requires=[],
    author='TileJet Developers',
    author_email='tilejet.dev@gmail.com',
    license='MIT License',
    url='https://github.com/tilejet/tilejet-logs/',
    keywords='python gis tilejet',
    description='A python utility library containing functions for logging tile service usage.',
    long_description=open('README.md').read(),
    download_url="https://github.com/tilejet/tilejet-logs/zipball/master",
    packages=["tilejetlogs"],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
