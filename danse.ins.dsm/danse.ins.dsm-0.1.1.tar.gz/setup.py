#!/usr/bin/env python

from distutils.core import setup
setup(name='danse.ins.dsm',
      version='0.1.1',
      description='Data stream model',
      author='Jiao Lin',
      author_email='jiao.lin@gmail.com',
      url='https://github.com/danse-inelastic/dsm',
      requires = ["danse.us(>=1.0)"],
      packages=['danse.ins.dsm'],
      package_dir = {'danse.ins.dsm': '.'},
     )
