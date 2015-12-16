#!/usr/bin/env python
# -*- coding: utf-8 -*-

#The console_scripts Entry Point

#The second approach is called an ‘entry point’. 
#Setuptools allows modules to register entrypoints which other packages can hook into to provide certain functionality. 
#It also provides a few itself, including the console_scripts entry point.


import pyfun

def main():
        print pyfun.joke()
