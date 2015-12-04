from setuptools import find_packages, setup

from rmsutil import __version__ as version

setup(
    name='rmsutil',
    version=version,
    description='Common utilities used in RMS projects',
    author='Rackspace',
    author_email='',
    url='',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=[
        'six',
    ],
)
