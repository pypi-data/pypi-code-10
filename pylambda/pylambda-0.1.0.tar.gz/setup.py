#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys

requires = [
    'awscli'
]

setup(
    name='pylambda',
    version='0.1.0',
    description='Run your local python AWS Lambda locally and deploy to S3.',
    url='https://github.com/PitchBook/PitchBook_Core/python_lambda',
    author='Nicholas Ames',
    author_email='nicholas.ames@pitchbook.com',
    license='MIT',
    keywords='aws lambda s3',

    packages=find_packages(exclude=['test/*']),
    install_requires=requires,

    entry_points={
        'console_scripts': [
            'pylambda=pylambda:main',
        ],
    },

    extras_require={
        'test': ['coverage', 'mock', 'unittest2'],
    }
)