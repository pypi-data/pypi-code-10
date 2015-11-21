#!/usr/bin/env python
from setuptools import setup


def read_readme(filename):
    try:
        import pypandoc
        return pypandoc.convert(filename, 'rst')
    except (IOError, ImportError):
        return ''


setup(
    name='json_compare',
    version='0.2.3',
    description='Json comparison tool',
    author='Chris Saxey',
    author_email='chrissaxey@gmail.com',
    url='https://github.com/darthghandi/jsoncompare',
    packages=['json_compare', 'json_compare.test'],
    test_suite="json_compare.test.test_json_compare",
    keywords='json comparison compare order',
    long_description=read_readme('README.md'),
    install_requires=['python-rapidjson', 'future']
)
