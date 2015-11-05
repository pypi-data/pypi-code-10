#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

__VERSION__ = '0.0.9'

setup(name='Flask-INIConfig',
      version=__VERSION__,
      author='Wampeter Foma',
      author_email='foma@wampeter.org',
      url='https://bitbucket.org/wampeter/flask-iniconfig/',
      license='BSD',
      description='A flask extension to load ini files via config',
      long_description=open('README.rst').read(),
      zip_safe=False,
      py_modules=['flask_iniconfig'],
      platforms='any',
      install_requires=['Flask'],
      setup_requires=['nose'],
      tests_require=['nose', 'coverage'],
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
