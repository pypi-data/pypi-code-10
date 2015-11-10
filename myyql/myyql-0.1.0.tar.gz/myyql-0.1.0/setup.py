#!/usr/bin/env python
from setuptools import setup, find_packages
VERSION = '0.1.0'

read_md = lambda f: open(f, 'r').read()

setup(
        name='myyql',
        version=VERSION,
        description="YQL(Yahoo Query Language) client written in python3",
        # see http://pypi.python.org/pypi?:action=list_classifiers
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Utilities",
            "License :: OSI Approved :: MIT License",
            ],
         keywords='python3,yql',
         author='chikyukotei',
         author_email='chikyukotei1122@gmail.com',
         url='https://github.com/chikyukotei/myyql',
         packages=find_packages('myyql', exclude=['examples', 'test']),
         include_package_data=True,
         zip_safe=True,
         long_description=read_md('README.md'),
         install_requires=[],
         )
