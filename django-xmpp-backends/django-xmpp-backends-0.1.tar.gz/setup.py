#!/usr/bin/env python

from setuptools import setup

setup(
    name='django-xmpp-backends',
    version='0.1',
    description='Convenience utilities for using xmpp-backends in Django.',
    author='Mathias Ertl',
    author_email='mati@jabber.at',
    url='https://github.com/mathiasertl/django-xmpp-backends',
    packages=['django_xmpp_backends'],
    license="GNU General Public License (GPL) v3",
    install_requires=[
        'Django',
        'xmpp-backends>=0.1',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP",
    ],
    long_description="""A set of convenience utilities if you want to use xmpp-backends in Django.
This includes convenience imports to get the currently configured backend, an authentication
backend and a subclass of AbstractBaseUser to handle passwords via xmpp-backends."""
)
