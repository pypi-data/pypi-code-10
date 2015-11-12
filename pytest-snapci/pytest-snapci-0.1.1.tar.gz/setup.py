import textwrap

from setuptools import setup

from pytest_snapci import __version__
from pytest_snapci import plugin

setup(
    name="pytest-snapci",
    version=__version__,
    description="py.test plugin for Snap-CI",
    long_description=textwrap.dedent(plugin.pytest_collection_modifyitems.__doc__),
    author="Omer Katz",
    author_email="omer.drow@gmail.com",
    url="https://github.com/thedrow/pytest-snapci",
    packages=["pytest_snapci"],
    entry_points={
        'pytest11': [
            'snapci = pytest_snapci.plugin'
        ],
    },
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        # "Programming Language :: Python :: 3",  Not tested yet
    ),
)
