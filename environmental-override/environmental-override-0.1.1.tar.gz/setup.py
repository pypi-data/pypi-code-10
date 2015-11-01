from setuptools import setup, find_packages

from environmental_override import __version__ as version_string


setup(
    name='environmental-override',
    version=version_string,
    url='https://github.com/coddingtonbear/environmental-override',
    description=(
        'Easily configure apps using simple environmental overrides.'
    ),
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
)
