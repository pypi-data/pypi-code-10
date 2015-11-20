#!/usr/bin/env python

from setuptools import setup

setup(

name='CME',
version='1.0',
author='Jennifer Karr',
maintainer='Jennifer Karr',
author_email='jkarr@asiaa.sinica.edu.tw',
maintainer_email='jkarr@asiaa.sinica.edu.tw',
url="",
description="GUI for interactive plotting of colour-magnitude and colour-colour diagrams",
long_description="GUI for interactive plotting of colour-colour and colour-magnitude diagrams of astronomical catalogues, compatible with common catalogue formats (IRSA/GATOR, SDSS). ",
license="GNU public license",

packages = ['CME'],

package_dir={'CME':'script'},
package_data={'CME':['calibration_files/*.txt']},

entry_points= {'console_scripts': ['cme_script = CME.commands:cme_script']}
           

#data_files=[('calibration_files', ['*.txt'])]


)
