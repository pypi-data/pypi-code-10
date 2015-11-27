#!/usr/bin/env python3

import os
import sys


try:
    from setuptools import setup
except:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

setup(
    name='memegen',
    version='0.0.3',
    description='Caption images, from command line, using ImgFlip or MemeGenerator APIs.',
    author='Cristian Cabrera',
    author_email='surrealcristian@gmail.com',
    url='https://github.com/surrealcristian/memegen',
    keywords='caption images memes cli terminal command line imgflip memegenerator service api',
    install_requires=['requests>=2'],
    license='MIT',
    py_modules=['memegen'],
    scripts=['memegen.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities',
    ],
)
