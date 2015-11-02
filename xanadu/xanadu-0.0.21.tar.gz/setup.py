#!/usr/bin/env python
# encoding=utf-8


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'xlzd'


with open('VERSION', 'r') as v_file:
    VERSION = v_file.read()


with open('README.rst', 'rb') as f_readme:
    README = f_readme.read().decode('utf-8')

PACKAGES = ['xanadu']


setup(
    name='xanadu',
    version=VERSION,
    keywords=['xlzd', 'xanadu', 'webframework'],
    description=u'xanadu: a new web framework. - by xlzd',
    long_description=README,
    author='xlzd',
    author_email='i@xlzd.me',
    license='GPLv2',
    url='https://github.com/xlzd/xanadu',
    download_url='https://github.com/xlzd/xanadu',
    install_requires=[],
    extras_require={},
    packages=PACKAGES,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        # 'License :: GPLv2 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
