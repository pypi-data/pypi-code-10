#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='yaghurl',
    description='Create comment links into github repositories.',
    version='0.1.dev1',
    author='Nathan Wilcox',
    author_email='nejucomo@gmail.com',
    license='GPLv3',
    url='https://github.com/nejucomo/yaghurl',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'yaghurl = yaghurl.main:main',
            ],
        },
    )
