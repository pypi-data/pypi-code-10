from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='OttawaCityJobs',

    version='0.1.3',

    description="Yet another ottawa city jobs scrapper",

    url='https://github.com/guinslym/ottawajobs',

    author='Guinslym',
    author_email='guinslym@gmail.com',

    license='GNU GPLv2',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
    ],
    install_requires=[
        'requests'
        ],
    keywords='json scrapper jobs city Ottawa',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),


)
