#!/usr/bin/env python
# -*- coding: utf-8 -*-

install_requirements = [
    'numpy>=1.9.0',
    'scipy>=0.14.1',
    'matplotlib>=1.4.2',
]

#for requirement in install_requirements:
#    pip.main(['install'] + [requirement])

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='EB',
    version='0.1.2',
    description="Ensemble Builder",
    long_description=readme + '\n\n' + history,
    author="Rob Swift",
    author_email='robvswift@gmail.com',
    url='https://github.com/rvswift/EB',
    packages=[
        'EB', 'EB.builder', 'EB.builder.exhaustive', 'EB.builder.fastheuristic',
        'EB.builder.postanalysis', 'EB.builder.slowheuristic', 'EB.builder.utilities',
        'EB.builder.splitter',
    ],
    package_dir={'EB':
                 'EB'},
    include_package_data=True,
    license="BSD",
    zip_safe=False,
    keywords='EB',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    scripts = ['EB/ensemblebuilder'],
    test_suite='tests',
    tests_require=test_requirements
)
