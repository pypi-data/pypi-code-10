#!/usr/bin/env python
from setuptools import setup


setup(
    name='start',
    version='0.1',
    description='Very simple command to start a single process from a Procfile',
    author='Divio AG',
    author_email='aldryn@divio.ch',
    url='https://github.com/aldryncore/start',
    license='BSD',
    platforms=['OS Independent'],
    py_modules=['start'],
    install_requires=[
        'pyaml',
    ],
    entry_points="""
    [console_scripts]
    start = start:cli
    """,
)
