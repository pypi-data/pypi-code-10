#!/usr/bin/env python

from setuptools import setup, find_packages
import setuptools.command.install

setup(
    name="jw.lognotify",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        'setuptools>=3',
        'future',
        'gevent',
        'PyYAML'
    ],
    package_data={
        '': ['*.rst', '*.txt']
    },
    entry_points={
        'console_scripts': [
            'lognotify = main.main:Main'
        ]
    },
    test_suite='nose.collector',
    tests_require=['Nose', 'mock'],
    author="Johnny Wezel",
    author_email="dev-jay@wezel.name",
    description="Notify about logfile events in real-time",
    long_description=open('README.rst').read(),
    license="GPL",
    platforms='Posix',
    keywords="logfile notifications",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring',
    ],
    url="https://pypi.python.org/pypi/jw.lognotify"
)
