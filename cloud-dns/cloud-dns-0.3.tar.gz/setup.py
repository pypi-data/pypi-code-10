#!/usr/bin/env python
import os
import sys
from setuptools import setup
from textwrap import dedent

NAME = "cloud-dns"
GITHUB_ORG_URL = "https://github.com/cogniteev"
ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

exec(open('cloud_dns/version.py').read())

setup(
    name=NAME,
    version=version,
    author="Tristan Carel",
    author_email="tristan.carel@gmail.com",
    url= GITHUB_ORG_URL + '/' + NAME,
    download_url="{0}/{1}/tarball/v{2}".format(GITHUB_ORG_URL, NAME, version),
    description="DNS utilities over Apache libcloud",
    long_description=dedent("""
        Rationale
        ---------
        Using gcloud compute ssh ... commands are not user friendly.
    """),
    keywords="libcloud dns",
    packages=['cloud_dns'],
    install_requires=[
        'apache-libcloud>=0.17',
        'boto>=2.38.0',
        'dnslib>=0.9.6',
        'gcs-oauth2-boto-plugin==1.9',
        'keybase-api>=0.1.3',
        'pycrypto>=2.6.1',
        'PyYAML>=3.11',
    ],
    zip_safe=False,
    license="Apache license version 2.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points = """
        [console_scripts]
        cloud-dns = cloud_dns.entry_points:cloud_dns
    """
)
