#!/usr/bin/python
from setuptools import setup, find_packages
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = None

setup(name='ionize',
      version='0.13.0',
      author='Lewis A. Marshall',
      author_email='lewis.a.marshall@gmail.com',
      url="http://lewisamarshall.github.io/ionize/",
      classifiers=[
          "Programming Language :: Python",
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Scientific/Engineering :: Chemistry",
          ],
      use_2to3=True,
      license='LICENSE',
      description='A package for calculating electrolyte properties.',
      long_description=long_description,
      packages=find_packages(),
      requires=['numpy', 'scipy', 'biopython'],
      package_data={'ionize': ['Database/ion_data.json'],
                    },
      test_suite="ionize.tests",
      )
