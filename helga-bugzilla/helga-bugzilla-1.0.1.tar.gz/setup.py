import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '1.0.1'

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main('tests', self.pytest_args)
        sys.exit(errno)

setup(name="helga-bugzilla",
      version=version,
      description=('bugzilla plugin for helga'),
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      keywords='irc bot bugzilla',
      author='ken dreyer',
      author_email='ktdreyer [at] ktdreyer [dot] com',
      url='https://github.com/ktdreyer/helga-bugzilla',
      license='MIT',
      packages=find_packages(),
      py_modules=['helga_bugzilla'],
      install_requires=[
          'helga',
          'python-bugzilla',
      ],
      tests_require=[
          'helga',
          'pytest',
          'python-bugzilla',
      ],
      entry_points = dict(
          helga_plugins = [
              'bugzilla = helga_bugzilla:helga_bugzilla',
          ],
      ),
      cmdclass = {'test': PyTest},
)
