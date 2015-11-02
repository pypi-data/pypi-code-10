#!/usr/bin/env python

from setuptools import setup

setup(
    name='journaler',
    version='1.0',
    author='Matt Bachmann',
    author_email='bachmann.matt@gmail.com',
    url='https://github.com/Bachmann1234/journaler',
    description="Tool to support logging of diet and mood",
    license='Apache 2.0',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python'],
    packages=['journaler'],
    install_requires=['pytz'],
    entry_points={
        'console_scripts': ['journaler = journaler.log:main']
    }
)
