#!/usr/bin/env python3

from setuptools import setup

setup(
    name='Sundowner',
    version='0.2',
    long_description=__doc__,
    packages=['sundowner'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.10.1',
        'ephem>=3.7.6',
        'itsdangerous>=0.24',
        'Jinja2>=2.8',
        'MarkupSafe>=0.23',
        'Werkzeug>=0.10.4',
        'python-dateutil>=2.4.2'
    ],
    test_suite='sundowner.test'
)
