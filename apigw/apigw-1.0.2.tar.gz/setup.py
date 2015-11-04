#!/usr/bin/env python

from setuptools import setup

version = __import__("apigw").version

setup(
    name = "apigw",
    version = version,
    author = "NTT Communications APIGateway Teams",
    author_email = "apigateway@ntt.com",
    description = ("NTT Communications API SDK"),
    license = "Apache License, Version 2.0",
    keywords = "apigw api sdk B2B",
    url='https://github.com/nttcom/apigw-python-sdk',
    packages = ["apigw"],
    package_data = {
                'apigw': ['requirements.txt'],
    },
    install_requires = ['requests==2.7.0'],
)
