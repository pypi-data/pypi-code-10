# -*- coding: utf-8 -*-
"""Installer for the plonetrick.csrfworkarounds package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = "\n\n".join((
    read('README.rst'),
    read('docs', 'CHANGELOG.rst')
))

setup(
    name='plonetrick.csrfworkarounds',
    version='0.9.0',
    description="plonetrick.csrfworkarounds",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    keywords='Plone',
    author='Alessandro Pisa',
    author_email='alessandro.pisa@gmail.com',
    url='http://pypi.python.org/pypi/plonetrick.csrfworkarounds',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plonetrick'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
