#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()

requirements = [
    # TODO: put package requirements here
]

setup(
    name='json_url_rewriter',
    version='0.1.1',
    description='Helpers for rewriting links in JSON.',
    long_description=readme,
    author='Eric Larson',
    author_email='eric@ionrock.org',
    url='https://github.com/ionrock/json_url_rewriter',
    packages=[
        'json_url_rewriter',
    ],
    package_dir={'json_url_rewriter':
                 'json_url_rewriter'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='json_url_rewriter',
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
)
