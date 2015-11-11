#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'pybuilder_header_plugin',
          version = '0.1.0',
          description = '''PyBuilder Header Plugin''',
          long_description = '''Please visit https://github.com/cowst/pybuilder_header_plugin for more information!''',
          author = "Diego Costantini, Michael Gruber",
          author_email = "diego.costantini@gmail.com, aelgru@gmail.com",
          license = 'Apache License, Version 2.0',
          url = 'https://github.com/cowst/pybuilder_header_plugin',
          scripts = [],
          packages = ['pybuilder_header_plugin'],
          py_modules = [],
          classifiers = ['Development Status :: 4 - Beta', 'Environment :: Console', 'Intended Audience :: Developers', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.2', 'Programming Language :: Python :: 3.3', 'Programming Language :: Python :: 3.4'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "committer", "wheel" ],
          
          zip_safe=True
    )
