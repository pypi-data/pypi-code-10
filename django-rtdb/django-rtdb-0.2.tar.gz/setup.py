#!/usr/bin/env python

from setuptools import setup

with open('README.rst') as README_FILE:
    long_description = README_FILE.read()

setup(
    name='django-rtdb',
    version='0.2',
    packages=['rtdb'],
    package_dir = {'': 'src',},
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    description='Simplified access to the Request Tracker 4 database',
    author_email='hanne.moa@uninett.no',
    url='https://github.com/UNINETT/django-rtdb',
    author='Hanne Moa',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
