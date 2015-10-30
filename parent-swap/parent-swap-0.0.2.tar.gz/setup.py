# -*- coding: utf-8 -*-
import os
from setuptools import setup

name = 'parent-swap'
version = '0.0.2'

# allow setup.py to be run from any path
os.chdir(
    os.path.normpath(
        os.path.join(os.path.abspath(__file__), os.pardir)
    )
)


install_requires = [
    "django>=1.7,<1.9",
    "six"
]


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(
    name=name,
    version=version,
    description='Replace abstract parent classes of django objects',
    license='MIT',
    author='Cameron Lowe',
    author_email='clowe@theonion.com',
    include_package_data=True,
    install_requires=install_requires,
    test_suite='parent_swap.tests.runtests.main',
    packages=get_packages('parent_swap'),
)
