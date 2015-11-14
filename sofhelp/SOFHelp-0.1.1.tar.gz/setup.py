import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "SOFHelp",
    version = "0.1.1",
    author = "Arockia Arulnathan",
    author_email = "arockia.arulnathan@live.in",
    description = ("StackOverflow help for exception within program which will helpful to debug with proxy support.."),
    license = "BSD",
    keywords = "stackoverflow,debug",
    url = "http://packages.python.org/sofhelp",
    packages=['SOFHelp'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],)