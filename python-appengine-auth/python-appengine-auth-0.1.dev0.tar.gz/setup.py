# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

setup(
    name='python-appengine-auth',
    version=__import__('social_appengine_auth').__version__,
    author='Marc Hoersken',
    author_email='info@marc-hoersken.de',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/mback2k/python-appengine-auth',
    license='MIT',
    description=' '.join(__import__('social_appengine_auth').__doc__.splitlines()).strip(),
    install_requires=['python-social-auth>=0.2.1', 'oauthlib>=0.3.8'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.md'),
)
