#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

setuptools.setup(
    name = "digitalriver",
    version = "0.1.2",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = "DigitalRiver",
    license = "Apache License, Version 2.0",
    keywords = "digitalriver pas deployment",
    url = "http://digitalriver.hive.pt",
    zip_safe = False,
    packages = [
        "digitalriver",
        "digitalriver.controllers",
        "digitalriver.models",
        "digitalriver.util"
    ],
    package_dir = {
        "" : os.path.normpath("src")
    },
    package_data = {
        "digitalriver" : [
            "static/css/*",
            "static/images/*",
            "static/js/*",
            "templates/*.tpl",
            "templates/droplet/*.tpl",
            "templates/partials/*.tpl"
            "templates/provision/*.tpl"
        ]
    },
    install_requires = [
        "appier",
        "digitalocean_api_python"
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
    ]
)
