#!/usr/bin/env python

from setuptools import setup

requirements = open('../requirements.txt').read().split('\n')

setup(
    name="modjango",
    use_vcs_version=True,
    description="mongoengine integration for django",
    author="Philip Zerull",
    author_email="przerull@gmail.com",
    packages=['modjango'],
    provides=['modjango'],
    install_requires=requirements,
    setup_requires=['hgtools']
)
