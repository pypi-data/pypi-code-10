#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="taiga-plugin-iframe",
    version=":versiontools:taiga_plugin_iframe:",
    description="The Taiga plugin for custom iframe with menu icons",
    long_description="",
    keywords="taiga, iframe, menu, plugin",
    author="Max Sinelnikov",
    author_email="msiniy@gmail.com",
    url="https://github.com/msiniy/taiga-plugin-iframe",
    license="AGPL",
    include_package_data=False,
    packages=find_packages(),
    install_requires=[
        "django >= 1.8.5",
    ],
    setup_requires=[
        "versiontools >= 1.8",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
