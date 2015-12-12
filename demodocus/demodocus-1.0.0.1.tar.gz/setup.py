#!/usr/bin/env python
# coding=utf-8

"""
Set demodocus package up
"""

from setuptools import setup

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"

setup(
    name="demodocus",
    packages=["demodocus"],
    package_data={"demodocus": ["res/*"]},
    version="1.0.0.1",
    description="demodocus is Python CLI program to quickly check synchronization maps",
    author="Alberto Pettarin",
    author_email="alberto@albertopettarin.it",
    url="https://github.com/pettarin/demodocus",
    license="MIT License",
    long_description=open("README.rst", "r").read(),
    install_requires=["pyaudio"],
    scripts=["bin/demodocus"],
    keywords=[
        "JSON",
        "SSV",
        "SSVH",
        "aeneas",
        "audio",
        "demodocus",
        "ffmpeg",
        "portaudio",
        "pyaudio",
        "synchronization map",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Education",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Utilities"
    ],
)
