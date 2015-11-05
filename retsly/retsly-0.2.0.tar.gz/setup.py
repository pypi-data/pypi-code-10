from setuptools import setup
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'retsly'))


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='retsly',
    version='0.2.0',
    description="A Python wrapper for the Retsly API (https://rets.ly)",
    long_description=readme(),
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