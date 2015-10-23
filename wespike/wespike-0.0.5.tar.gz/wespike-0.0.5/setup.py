import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "wespike",
    version = "0.0.5",
    author = "Wespike",
    author_email = "dev@wespike.com",
    description = ("Coming soon."),
    license = "BSD",
    keywords = "wespike",
    url = "http://packages.python.org/wespike",
    packages=[],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License"
    ],
)
