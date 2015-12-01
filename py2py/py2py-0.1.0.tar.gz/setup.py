# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup (
    name='py2py',
    version='0.1.0',
    description='Lightweight P2P in Python 3.4+ via HTTP POST',
    long_description=long_description,
    url='https://github.com/etkirsch/py2py',
    author='Evan Kirsch',
    author_email='etkirsch@gmail.com',
    license='MIT',
    scripts=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='p2p peer lightweight http post',
    packages=find_packages()
)
