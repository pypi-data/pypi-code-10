#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="py_release_tools",
    version="0.1.1",
    description="Python release tools",
    long_description=open("README.rst", "r").read(),
    author="Mike Crute",
    author_email="mcrute@gmail.com",
    url="https://github.com/mcrute/py_release_tools",
    packages=find_packages(),
    install_requires=[
        "pep8>=1.6.2",
        "mock>=1.0.1",
        "coverage>=4.0.3",
        "setuptools>=17.1",
    ],
    entry_points={
        "distutils.commands": [
            ("increment_semver = "
                "py_release_tools.commands:IncrementSemanticVersion"),
            "git_push = py_release_tools.commands:GitPush",
            "cover_tests = py_release_tools.commands:TestsWithCoverage",
            "pep8 = py_release_tools.commands:PEP8CheckStyle",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Setuptools Plugin",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
    ]
)
