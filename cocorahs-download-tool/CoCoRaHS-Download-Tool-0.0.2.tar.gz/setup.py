# Standard Library Imports
import os

# Setuptools Package Imports
from setuptools import setup

# Local Package Imports
from cocorahs_dlt import __version__


# Open the README file for inclusion in the setup metadata.
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name = 'CoCoRaHS-Download-Tool', 
    version = __version__, 
    py_modules = ['cocorahs_dlt'], 
    license = 'BSD License', 
    description = 'Tool to download CoCoRaHS data.',
    long_description = README,
    url = 'https://bitbucket.org/nmclimate/cocorahs-download-tool',
    author = 'Stanley Engle',
    author_email = 'sengle@nmsu.edu',
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)


