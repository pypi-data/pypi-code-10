#!/usr/bin/python
# coding=utf-8

import sys
import shutil
from setuptools import setup

from codecs import open
from os import path, environ

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tmblr',
    version='2015.12.11',
    description='a silly tumblr client',
    long_description=long_description,
    url='http://kyber.io/tmblr',
    author='bie',
    author_email='bie@kyber.io',
    license='MIT',
    package_data={
        'tmblr': ['doc/tmblr.1']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux'
    ],
    keywords='tumblr blog',
    py_modules=["tmblr"],
    install_requires=['pytumblr'],
    entry_points={
        'console_scripts': [
            'tmblr=tmblr:main',
        ],
    },
)

# Ugh, ganske fælt at det ikke finnes en fin måte å gjøre dette på...
if "install" in sys.argv and sys.platform == "linux2":
    man_path = environ.get("MANDIR") or "/usr/share/man/man1"
    if path.exists(man_path):
        print("Copying man page to %s" % man_path)
        shutil.copy2("doc/tmblr.1", man_path)

