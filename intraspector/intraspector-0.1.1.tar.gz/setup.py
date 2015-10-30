# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='intraspector',

    version='0.1.1',

    description='Intraspector decorator for python',
    long_description=long_description,

    url='https://github.com/BespokeInsights/python-intraspector',

    author='Aaron Hayes',
    author_email='aaron.hayes92@gmail.com',

    license='MIT',

    packages=['intraspector']
)
