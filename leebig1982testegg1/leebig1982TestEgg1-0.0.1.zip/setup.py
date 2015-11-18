# coding=utf-8
from setuptools import setup, find_packages

setup(
    name = 'leebig1982TestEgg1',
    version = '0.0.1',
    keywords = ('lucas', 'egg'),
    description = 'a simple egg',
    license = 'Taiwan License',

    url = 'http://leebig1982.org',
    author = 'leebig1982',
    author_email = 'leebig1982@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)