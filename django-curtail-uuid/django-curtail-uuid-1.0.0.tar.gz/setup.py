# -*- coding: utf-8 -*-
from __future__ import with_statement
from setuptools import setup


version = '1.0.0'


setup(
    name='django-curtail-uuid',
    version=version,
    keywords='django-curtail-uuid',
    description="Curtail UUID Appointed Length",
    long_description=open('README.rst').read(),

    url='https://github.com/Brightcells/django-curtail-uuid',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    py_modules=['curtail_uuid'],
    install_requires=[],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
)
