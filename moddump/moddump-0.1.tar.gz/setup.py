#!/usr/bin/python
# -*- coding: UTF-8 -*-

from setuptools import setup

setup(name='moddump',
      version='0.1',
      description='Dota2 Reborn script to generate a JSON of your mod.',
      url='https://github.com/muZk/modjson',
      author='Nicolás Gómez',
      author_email='neeco.gmz@gmail.com',
      license='MIT',
      packages=['moddump'],
      scripts= ['bin/moddump'],
      data_files=[('locales', ['dota_english.json'])],
      install_requires=[
      	'steamodd',
      ],
      zip_safe=False)