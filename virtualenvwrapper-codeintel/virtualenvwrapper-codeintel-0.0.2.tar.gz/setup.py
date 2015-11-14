#!/usr/bin/env python

__author__ = 'Jaume Martin'
__version__ = '0.0.2'

# Bootstrap installation of Distribute
from setuptools import setup,  find_packages

setup(
    name='virtualenvwrapper-codeintel',
    version=__version__,
    author=__author__,
    url='https://github.com/Xumeiquer/codeintel-local-config',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Console',
    ],
    platforms=['Any'],
    provides=['virtualenvwrapper.codeintel'],
    requires=['virtualenv', 'virtualenvwrapper (>=2.0)'],
    description=(
        '''It creates the local configuration folder for the codeintel
        as well as a config file customized so pointing to the virtualenv
        folder'''
    ),
    long_description=open('README.rst').read(),
    license='MIT License',
    namespace_packages=['virtualenvwrapper'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'virtualenvwrapper.project.post_mkproject': [
            'user_scripts = virtualenvwrapper.codeintel:post_mkproject',
        ]
    },
)
