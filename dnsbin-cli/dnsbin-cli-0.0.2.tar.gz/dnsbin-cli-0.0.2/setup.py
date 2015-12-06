#!/usr/bin/env python

import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

setup(
    name='dnsbin-cli',
    version='0.0.2',
    description='Distribute and retrieve files using DNS',
    long_description=readme,
    author='Thomas Maurice',
    author_email='thomas@maurice.fr',
    url='https://github.com/thomas-maurice/dnsbin-cli',
    platforms='any',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'dnspython==1.12.0',
        'clifactory==0.1.1',
        'requests==2.8.1',
    ],
    scripts = ["bin/dnsbin"], 
    license="WTFPL",
)
