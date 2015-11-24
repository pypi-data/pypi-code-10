import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

tests_path = os.path.join(os.path.dirname(__file__), 'tests')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        args = sys.argv[sys.argv.index('test')+1:]
        self.test_args = args
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'setuptools',
    'six >= 1.4',
    'docutils >= 0.11',
    'sphinx >= 1.3',
    ]

tests_require = [
    'pytest >= 2.0.3',
    'grok',
    'zope.schema',
    'BTrees',
    'sphinx-testing',
    ]

docs_require = [
    ]


setup(
    name="waeup.sphinx.autodoc",
    version="0.1",
    author="Uli Fouquet",
    author_email="uli@gnufix.de",
    description=(
        "More Zope compatible autodocumenters for Sphinx."),
    license="GPL 3.0",
    keywords="sphinx autodoc grok zope waeup documenter",
    url="http://pypi.python.org/pypi/waeup.sphinx.autodoc",
    packages=['waeup.sphinx'],
    namespace_packages=['waeup', ],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        (
            "License :: OSI Approved :: "
            "GNU General Public License v3 or later (GPLv3+)"),
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Documentation",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Utilities",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=dict(
        tests=tests_require,
        docs=docs_require,
        ),
    cmdclass={'test': PyTest},
    entry_points={
        }
)
