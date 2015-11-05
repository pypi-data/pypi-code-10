from setuptools import setup
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'retsly'))

try:
    from pypandoc import convert
    README = convert('README.md', 'rst')
except ImportError:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
    print("warning: pypandoc module not found, could not convert Markdown to RST")

setup(
    name='retsly',
    version='0.2.1',
    description="A Python wrapper for the Retsly API (https://rets.ly)",
    long_description=README,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='retsly python sdk',
    url='https://github.com/retsly/python-sdk',
    author='Retsly Software Inc.',
    author_email='support@rets.ly',
    license='MIT',
    packages=[
        'retsly'
    ],
    install_requires=[
        'requests',
        'jsonurl'
    ]
)