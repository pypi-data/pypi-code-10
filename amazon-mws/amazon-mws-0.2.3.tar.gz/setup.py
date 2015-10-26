# -*- coding: utf-8 -*-
from distutils.core import setup

version = '0.2.3'

REQUIRES = ['requests']

setup(
    name="amazon-mws",
    version=version,
    install_requires=REQUIRES,
    description="A python interface for Amazon MWS",
    long_description=open('README.md', 'rt').read(),
    author="Juozas Kaziukenas",
    author_email="juozas@juokaz.com",
    url="https://github.com/juokaz/python-amazon-mws",
    packages=['mws'],
    platforms=['OS Independent'],
    license='LICENSE.txt'
)
