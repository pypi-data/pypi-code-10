from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='condor',

    version='0.0.4',

    description='Condor - Grunt-like automation system',
    long_description='',

    url='https://bivanov.bitbucket.org/condor',

    author='Bohdan Ivanov',
    author_email='bogdanivanov@live.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='build development',

    packages=find_packages(exclude=['tests']),

    include_package_data=True,

    install_requires=['watchdog', 'colorama'],

    entry_points={
        'console_scripts': [
            'condor=condor:main',
            'condor_config=condor_config:main'
        ],
    },
)
