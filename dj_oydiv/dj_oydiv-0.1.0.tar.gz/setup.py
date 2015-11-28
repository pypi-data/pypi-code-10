from setuptools import setup, find_packages
import itertools
import os
import sys

PKGNAME = 'dj_oydiv'
DIR = os.path.dirname(__file__)


def version():
    """Single source version information without importing the main project"""
    l = {}
    g = {}
    with open(os.path.join(DIR, PKGNAME, 'version.py'), 'rb') as f:
        code = compile(f.read(), 'version.py', 'exec')
        exec(code, g, l)

    return l['VERSION']


with open(os.path.join(DIR, 'README.rst'), 'r') as readme:
    long_description = readme.read()


install_requires = ['django<1.9','pyCrypto', 'arrow', 'oydiv_rpc']
if sys.version_info < (3, 4):
    install_requires.append('enum34')


setup(
    packages=find_packages(exclude=['tests']),
    name=PKGNAME,
    version=version(),
    licence='MIT',
    author_email='dev@ajenta.net',
    url='https://github.com/ajenta/dj-oydiv',
    author='ajenta',
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'wsauth': ['spyne', 'lxml'],
    },
    tests_require=['tox', 'coverage', 'flake8']
)
