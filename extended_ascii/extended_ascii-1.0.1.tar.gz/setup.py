from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import extended_ascii

import sys
import codecs


class PyTest(TestCommand):
    def run_tests(self):
        import doctest
        sys.exit(doctest.testmod(extended_ascii))


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()

setup(
    name='extended_ascii',
    version=extended_ascii.__version__,
    description=extended_ascii.__doc__.strip(),
    long_description=long_description(),
    url='https://github.com/eddieantonio/isri-extended-ascii',
    download_url='https://github.com/eddieantonio/isri-extended-ascii',
    author=extended_ascii.__author__,
    author_email='easantos@ualberta.ca',
    license=extended_ascii.__license__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'extended_ascii = extended_ascii.__init__:extended_ascii',
            'to_utf8 = extended_ascii.__init__:to_utf8',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
)
