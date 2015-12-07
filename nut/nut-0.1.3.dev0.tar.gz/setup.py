#!/usr/bin/python
from ast import literal_eval
from os import path
from setuptools import find_packages, setup

version = 'unknown'
with open(path.join('nut', '__init__.py'), 'r') as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = literal_eval(line.split('=', 1)[-1].strip())

if __name__ == '__main__':
    setup(
        name='nut',
        description='Network utility... things like a UDP/TCP relay.',
        author='Viet T. Nguyen',
        url='https://github.com/vietjtnguyen/nut',
        packages=find_packages(),
        version=version,
        entry_points={
            'console_scripts': [
                'nutrelay = nut.relay:main',
            ],
        },
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: Science/Research',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: MacOS',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Topic :: System :: Networking',
        ]
    )
