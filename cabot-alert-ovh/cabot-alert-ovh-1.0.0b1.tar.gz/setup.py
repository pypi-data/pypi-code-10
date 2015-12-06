#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='cabot-alert-ovh',
    version='1.0.0b1',
    description='An Ovh alert plugin for Cabot by Arachnys',
    url='http://cabotapp.com',
    author='Rachid Zarouali',
    author_email='rachid.zarouali@synolia.com',
    license='MIT',
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: System :: Monitoring',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            ],
    keywords='cabot ovh monitoring',
    packages=find_packages(),
    install_requires=['ovh']
    )
