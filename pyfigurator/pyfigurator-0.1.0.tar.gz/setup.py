import versioneer

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import io
import codecs
import os
import sys

import pyfigurator

here = os.path.abspath(os.path.dirname(__file__))


# def read(*filenames, **kwargs):
#     encoding = kwargs.get('encoding', 'utf-8')
#     sep = kwargs.get('sep', '\n')
#     buf = []
#     # raise Exception(os.listdir(here))
#     for filename in filenames:
#         # raise Exception(os.path.join(here, filename))
#         try:
#             with io.open(os.path.join(here, filename), encoding=encoding) as f:
#                 buf.append(f.read())
#         except FileNotFoundError:
#             raise Exception(here)
#     return sep.join(buf)


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

long_description = read('README.rst')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def setup_package():
    # Assumple additional setup commands
    cmdclass = versioneer.get_cmdclass()
    cmdclass['test'] = PyTest

    setup(
        name='pyfigurator',
        version=versioneer.get_version(),
        url='http://github.com/boehemyth/pyfigurator/',
        license='GNU General Public License v3.0',
        author='Dan Boehm',
        tests_require=['pytest'],
        cmdclass=cmdclass,
        install_requires=['wheel>=0.24.0'],
        author_email='dboehm.dev@gmail.com',
        description='Make it simpler to implement basic INI configuration and CLI interfaces.',
        long_description=long_description,
        packages=['pyfigurator'],
        include_package_data=True,
        platforms='any',
        test_suite='pyfigurator.test',
        classifiers = [
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.3',
            'Development Status :: 3 - Alpha',
            'Natural Language :: English',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: User Interfaces',
            ],
        extras_require={
            'testing': ['pytest']
        }
    )

if __name__ == "__main__":
    setup_package()