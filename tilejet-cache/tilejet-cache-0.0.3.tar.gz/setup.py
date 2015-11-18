#!/usr/bin/env python

from setuptools import setup

setup(
    name='tilejet-cache',
    version='0.0.3',
    install_requires=[],
    author='TileJet Developers',
    author_email='tilejet.dev@gmail.com',
    license='MIT License',
    url='https://github.com/tilejet/tilejet-cache/',
    keywords='python gis tilejet',
    description='A performant python library for caching tiles in-memory using memcached.',
    long_description=open('README.md').read(),
    download_url="https://github.com/tilejet/tilejet-cache/zipball/master",
    packages=["tilejetcache"],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
