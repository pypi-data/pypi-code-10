#!/usr/bin/env python
from setuptools import setup


setup(
    name="clearnlp-converter",
    packages=["clearnlp", "clearnlp.tests"],
    version="0.1",
    author="Matthew Honnibal",
    author_email="honnibal@gmail.com",
    url="http://github.com/honnibal/py-clearnlp-converter",
    package_data={"clearnlp": ["ext/*.jar", "ext/*.txt"]},
    description="""A Python wrapper for Jin-ho Choi's ClearNLP constituency-to-dependency converter.""",
    classifiers=[
                'Environment :: Console',
                'Operating System :: OS Independent',
                'Intended Audience :: Science/Research',
                'Programming Language :: Python',
                'Topic :: Scientific/Engineering'],
)
