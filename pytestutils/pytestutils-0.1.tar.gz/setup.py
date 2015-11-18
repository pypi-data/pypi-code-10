import codecs
import os
import re
import sys

from pip.req import parse_requirements
from setuptools import setup
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.rst')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

reqs = read('requirements.txt').split()
print reqs
setup(
    name='pytestutils',
    version=find_version('pytestutils', '__init__.py'),
    url='https://github.com/zancas/testutils-python',
    license='Apache Software License',
    author='Za Wilgustus',
    install_requires=reqs,
    cmdclass={'test': PyTest},
    author_email='Joshua.Wilcox@F5.com',
    description='A pytest plugin that patches imports and replaces them with mocks, when the imports are initially run.',
    long_description=long_description,
    packages=['pytestutils'],
    include_package_data=True,
    platforms='any',
    test_suite='pytestutils.test.test_imports',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    extras_require={
        'testing': ['pytest'],
      }
)

def main():
    print reqs

if __name__ == '__main__':
    main()
