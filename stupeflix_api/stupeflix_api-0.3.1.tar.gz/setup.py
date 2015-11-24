#!/usr/bin/env python
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.3.1'


setup(name='stupeflix_api',
    version=version,
    description="Stupeflix web services client libraries",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='',
    author='Francois Lagunas',
    author_email='francois@stupeflix.com',
    url='https://github.com/stupeflix/Stupeflix-API-Client',
    license='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts':
            ['stupeflix-api=stupeflix_api.commandline:main']
    }
)
