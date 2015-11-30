# -*- coding: utf-8 -*-
"""Installer for the redturtle.prepoverlays package."""

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
    name='redturtle.prepoverlays',
    version='1.0.0',
    description="Trigger Plone overlays by using data attributes",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Plone',
    author='RedTurtle Technology',
    author_email='sviluppoplone@redturtle.it',
    url='http://pypi.python.org/pypi/redturtle.prepoverlays',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['redturtle'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Plone',
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
