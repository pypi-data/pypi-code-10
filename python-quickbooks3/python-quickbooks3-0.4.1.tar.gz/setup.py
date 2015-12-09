import codecs
import os

from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


VERSION = (0, 4, 1)
version = '.'.join(map(str, VERSION))

setup(
    name='python-quickbooks3',
    version=version,
    author='Matt Long',
    author_email='matt@mattlong.org',
    description='A Python library for accessing the Quickbooks API. Forked from https://github.com/sidecars/python-quickbooks to improve Python 3 compatibility. Thanks to Edward Emanuel Jr.',
    url='https://github.com/mattlong/python-quickbooks',
    license='MIT',
    keywords=['quickbooks', 'qbo', 'accounting'],
    long_description=read('README.md'),

    install_requires=[
        'setuptools',
        'rauth>=0.7.1',
        'requests>=2.7.0',
        'simplejson>=2.2.0',
        'six>=1.4.0',
        'python-dateutil',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(),
)
