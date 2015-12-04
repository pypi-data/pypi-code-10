import os
import sys
from setuptools import setup, find_packages

# Utility function to read the README file used for the long_description
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Get current version from plotbox.version.py
exec(compile(open('plotbox/version.py').read(),
             'plotbox/version.py', 'exec'))

config = {
    'name': 'plotbox',
    'version': __version__,
    'author': 'Anmol Garg',
    'author_email': 'anmolgarg314@gmail.com',
    'description': 'Plotting library with a common API for static and interactive visualization',
    'license': 'MIT',
    'keywords': 'plotting visualization interactive',
    'url': 'https://github.com/anmolgarg/plotbox',
    'packages': find_packages(),
    'long_description': read('README.md'),
    'install_requires': [
        'matplotlib',
        'numpy',
        'pandas',
        'seaborn',
        'plotly',
    ], 
    'package_data': {'plotbox' : ['../README.md']},
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    'dependency_links': [],
    'scripts': []
}

setup(**config)
