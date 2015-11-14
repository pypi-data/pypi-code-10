#!/usr/bin/env python3

from setuptools import setup


setup(
    name="cproj",
    version="1.0.0",
    py_modules=["cproj"],
    description="A simple project template generator for C and C++",
    url="https://github.com/vitrig/cproj",
    author="Przemysław Czarnota",
    author_email="x2n404@gmail.com",
    license='MIT',
    
    classifiers = [
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers', 
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3', 
        'Programming Language :: Python :: 3.2', 
        'Programming Language :: Python :: 3.3', 
        'Programming Language :: Python :: 3.4', 
        'Programming Language :: Python :: 3.5'
    ],

    keywords='cproj project generator template',

    entry_points={
        'console_scripts': [
            'cproj=cproj:main'
        ]
    }
)
