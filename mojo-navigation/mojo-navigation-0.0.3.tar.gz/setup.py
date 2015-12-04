#! /usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
import sys

# python2 and python3 support
try:
    reload
except NameError:
    # py3k has unicode by default
    pass
else:
    reload(sys).setdefaultencoding('utf-8')


setup(
    name='mojo-navigation',
    version='0.0.3',
    author='Guillaume Pousseo',
    author_email='guillaumepousseo@revsquare.com',
    description='Django app managing simple navigation.',
    long_description=open('README.rst').read(),
    url='http://www.revsquare.com',
    license='MIT License',
    platforms=['OS Independent'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=[
        'django-mptt==0.7.4',
        'django_mptt_admin==0.3.1'
    ],
)
