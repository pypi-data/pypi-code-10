from Pythine import __version__
from setuptools import setup, find_packages

__author__ = 'zhengxu'

setup(
    name="Pythine",
    version=__version__,
    packages=find_packages(exclude=['tests']),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[],

    package_data={},

    # metadata for upload to PyPI
    author="Zheng Xu",
    author_email="xuzheng1111@gmail.com",
    description="Pythine is an extremely lightweight python multi-threaded framework for "
                "agile multi-thread programming. "
                "With a single decorator before the function, "
                "your function will automatically be executed in multiple threads. ",
    license="MIT",
    keywords="python, multi-thread programming",
    url="https://github.com/XericZephyr/Pythine",  # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)