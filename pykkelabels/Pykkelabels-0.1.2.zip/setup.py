import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Pykkelabels",
    version = "0.1.2",
    author = "Anders Brandt",
    author_email = "anderswb at gmail dot com",
    description = ("Provides access to the pakkelabels.dk web service."),
    license = "GPLv2",
    keywords = "pakke labels pakkelabels pakkelabels.dk",
    url = "https://github.com/anderswb/PykkeLabels",
    packages=['pykkelabels', 'test'],
    long_description=read('README.md'),
    package_data={'': ['README.md', 'test/reference_label.pdf']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)