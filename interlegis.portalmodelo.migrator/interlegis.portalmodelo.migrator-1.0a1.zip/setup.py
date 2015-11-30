# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0a1'
description = 'Portal Modelo: Migração de versões antigas do portal para a versão 3.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='interlegis.portalmodelo.migrator',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='interlegis plone portalmodelo transmogrifier migration',
    author='Programa Interlegis',
    author_email='ti@interlegis.leg.br',
    url='https://github.com/interlegis/interlegis.portalmodelo.migrator',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['interlegis', 'interlegis.portalmodelo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.jsonmigrator',
    ],
    entry_points='''
      [z3c.autoinclude.plugin]
      target = plone
      ''',
)
