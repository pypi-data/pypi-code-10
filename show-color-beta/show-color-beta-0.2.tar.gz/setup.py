#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from distutils.core import setup  
from setuptools import setup, find_packages  

setup(name="show-color-beta",  
      version="0.2",  
      description="depurador de logs servidores de correo",  
      author="Kevin Franco",  
      author_email="sistemasnegros@gmail.com",  
      url="https://gitlab.com/sistemasnegros/sw",  
      license="GPL",  
      scripts=["sw.py"],
      #install_requires = ["argparse"]
      packages = find_packages()   
)  