from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='octohat',
    version='0.1.9',
    description='octohat - no longer maintained. See: octohatrack',
    long_description=long_description,
    url='https://github.com/labhr/ye_olde_octohat',
    author='Katie McLaughlin',
    author_email='katie@glasnt.com',
    classifiers=[
        "Development Status :: 7 - Inactive", 
        "License :: OSI Approved :: MIT License"
    ],
    license='MIT',
    install_requires=['octohatrack']
)

