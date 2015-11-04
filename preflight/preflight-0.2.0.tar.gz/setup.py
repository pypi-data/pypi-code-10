#!/usr/bin/env python3
"""
Install preflight using setuptools
"""

from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    readme = f.read()

with open('preflight/version.py', 'r') as f:
    version = None
    exec(f.read())

setup(
    name='preflight',
    version=version,
    description='Checks that a site has been deployed correctly',
    long_description=readme,
    author='Tim Heap',
    author_email='hello@takeflight.com.au',
    url='https://bitbucket.org/takeflight/preflight/',

    install_requires=[
        'requests==2.8.0',
        'accept-types==0.3.0',
        'requests==2.8.0',
        'beautifulsoup4==4.4.0',
    ],
    zip_safe=False,
    license='BSD License',

    packages=find_packages(),

    include_package_data=True,
    package_data={},

    entry_points={
        'console_scripts': [
            'preflight=preflight.__main__:main'
        ],
    },

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
