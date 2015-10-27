#!/usr/bin/env python

### setup.py

from setuptools import setup, find_packages
import sys, os

setup(name='Watershed',
      version='2.0',
      author='Avinash Kak',
      author_email='kak@purdue.edu',
      maintainer='Avinash Kak',
      maintainer_email='kak@purdue.edu',
      url='https://engineering.purdue.edu/kak/distWatershed/Watershed-2.0.html',
      download_url='https://engineering.purdue.edu/kak/distWatershed/Watershed-2.0.tar.gz',
      description='An image segmentation algorithm based on the watershed paradigm',
      long_description='''

**Version 2.0** is a Python 3.x compliant version of the module.  This version should work with both Python 3.x and Python 2.7. 

**version 1.1.2** fixes the module packaging errors that had crept into the previous version. 

**Version 1.1** fixes a bug in the dilate() and erode()
methods of the module that caused these methods to misbehave
for non-square images.  Version 1.1 also includes
improvements in the explanatory comments included in the
scripts in the Examples directory.

This module is a Python implementation of the Watershed
algorithm for image segmentation.  The goal of this module
is not to compete with the popular OpenCV implementation of
the watershed algorithm.  On the other hand, the goal here
is to provide an alternative framework that is more amenable
to experimentation with the logic of watershed segmentation.

Typical usage syntax:

::

        from Watershed import *
        shed = Watershed(
                   data_image = "orchid0001.jpg",
                   binary_or_gray_or_color = "color",
                   size_for_calculations = 128,
                   sigma = 1,
                   gradient_threshold_as_fraction = 0.1,
                   level_decimation_factor = 16,
               )
        shed.extract_data_pixels()
        shed.display_data_image()
        shed.mark_image_regions_for_gradient_mods()                     #(A)
        shed.compute_gradient_image()
        shed.modify_gradients_with_marker_minima()                      #(B)
        shed.compute_Z_level_sets_for_gradient_image()
        shed.propagate_influence_zones_from_bottom_to_top_of_Z_levels()
        shed.display_watershed()
        shed.display_watershed_in_color()
        shed.extract_watershed_contours()
        shed.display_watershed_contours_in_color()

    The statements in lines (A) and (B) are needed only for marker-assisted
    segmentation with the module.  For a fully automated implemented of the
    BLM algorithm, you would need to delete those two statements.
          ''',

      license='Python Software Foundation License',
      keywords='image processing, image segmentation, computer vision',
      platforms='All platforms',
      classifiers=['Topic :: Scientific/Engineering :: Image Recognition', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3.4'],
      packages=['Watershed']
)
