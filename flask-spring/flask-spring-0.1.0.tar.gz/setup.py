__author__ = 'David Anderson'

"""
Flask-Flywheel
--------------

Adds Flywheel support to your Flask application.
"""
import codecs
import os
import re
from setuptools import setup, find_packages


def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_paths), 'r') as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="flask-spring",
    version=find_version("flask_spring", "__init__.py"),
    url="https://github.com/oggthemiffed/Flask-Spring",
    license="MIT",
    author="David Anderson",
    author_email="herbaliser1978@gmail.com",
    description="Adds the Spring framework support to your Flask application",
    long_description=__doc__,
    packages=find_packages( include=["flask_spring"], exclude=['contrib', 'docs', 'tests*']),
    zip_safe=False,
    install_requires=[
        "springpython",
        "flask",
        "pyyaml"
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    include_package_data=False,
)