from setuptools import setup, find_packages

setup(
    # Application name:
    name="visci",

    # Version number (initial):
    version="0.5",

    # Application author details:
    author="Vanessa Sochat",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=find_packages(),

    # Data
    package_data = {'visci':['templates/*']},

    # Details
    url="http://www.github.com/vsoch/visci",

    license="LICENSE.txt",
    description="visualization standard file structure for continuous integration",

)
