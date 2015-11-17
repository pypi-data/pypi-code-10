from setuptools import setup,find_packages
import os 
import sys
import shutil

setup(name='telomerecat',
	  description='Telomere Computational Analysis Tool',
      version='2.1.1',
      author="JHR Farmery",
      license='GPL',
      author_email = 'jhrf2@cam.ac.uk',
      packages = ['telomerecat'],
      package_dir = {'telomerecat':'telomerecat'},
      install_requires = ['parabam','argparse','numpy','pysam','scipy','sklearn'],
      include_package_data = True,
      scripts = ['./telomerecat/bin/telomerecat'],
      zip_safe = False
    )
