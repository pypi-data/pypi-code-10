#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages


def read(filename):
    with open(filename, 'rt') as f:
        return f.read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit(0)


setup(
    name='aio_crud_store',
    version='0.0.2',

    description=('A small subset of dbs capabilities to write'
                 ' dbs-independent asyncio libs'),
    long_description=read('README.rst'),

    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database'
    ],

    author='Imbolc',
    author_email='imbolc@imbolc.name',
    license='ISC',
    url='https://github.com/imbolc/aio_crud_store',

    packages=find_packages(),
    include_package_data=True,
)
