#!/usr/bin/python
# -*- coding: UTF-8 -*-

from setuptools import setup
import moddump

setup(name='moddump',
      version=moddump.__version__,
      description='Dota2 Reborn command line utility to generate a localized JSON of your mod.',
      url='https://github.com/muZk/moddump',
      author='Nicolás Gómez',
      author_email='neeco.gmz@gmail.com',
      license='MIT',
      packages=['moddump'],
      scripts= ['bin/moddump'],
      data_files=[('moddump/locales', moddump.__locales__)],
    	classifiers = [
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Programming Language :: Python"
          ],
      install_requires=[
      	'steamodd',
      ],
      zip_safe=False)