#!/usr/bin/env python

### setup.py

#from distutils.core import setup

from setuptools import setup, find_packages
import sys, os

setup(name='ICP',
      version='2.0',
      author='Avinash Kak',
      author_email='kak@purdue.edu',
      maintainer='Avinash Kak',
      maintainer_email='kak@purdue.edu',
      url='https://engineering.purdue.edu/kak/distICP/ICP-2.0.html',
      download_url='https://engineering.purdue.edu/kak/distICP/ICP-2.0.tar.gz',
      description='A Python module for registering a photo with a database image of the same scene',
      long_description='''

**Version 2.0** is a Python 3.x compliant version of the ICP module.  This version should work with both Python 3.x and Python 2.7.

**Version 1.3** is a major rewrite of the ICP module. While the previous
versions of this module were useful primarily for binary images, the new
version should also work well for grayscale and color images.  The new
module also contains improvements to the implementation code for the core
ICP algorithm.  It should be more forgiving should there exist no
correspondents in one image for some of the pixels chosen for ICP
calculations in the other image.  Finally, this version gives you two
options for applying ICP to grayscale and color images: You can carry out
either edge-based ICP or corner-pixels based ICP.

An application scenario would be the registration of an image recorded by a
UAV-mounted camera flying over a terrain with an image extracted from a GIS
(Geographical Information System) database.

Typical usage syntax for a color or grayscale image when using edge-based
ICP:

::

        import ICP
        icp = ICP.ICP(
                   binary_or_color = "color",
                   corners_or_edges = "edges",
                   auto_select_model_and_data = 1,
                   calculation_image_size = 200,
                   max_num_of_pixels_used_for_icp = 300,
                   pixel_correspondence_dist_threshold = 20,
                   iterations = 24,
                   model_image =  "SydneyOpera.jpg",
                   data_image = "SydneyOpera2.jpg",
                 )
        icp.extract_pixels_from_color_image("model")
        icp.extract_pixels_from_color_image("data")
        icp.icp()
        icp.display_images_used_for_edge_based_icp()
        icp.display_results_as_movie()
        icp.cleanup_directory()


Here is example syntax for using corner-pixels based ICP:

::

        import ICP
        icp = ICP.ICP(
                   binary_or_color = "color",
                   corners_or_edges = "corners",
                   calculation_image_size = 200,
                   image_polarity = -1,
                   smoothing_low_medium_or_high = "medium",
                   corner_detection_threshold = 0.2,
                   pixel_correspondence_dist_threshold = 40,
                   auto_select_model_and_data = 1,
                   max_num_of_pixels_used_for_icp = 100,
                   iterations = 16,
                   model_image =  "textured.jpg",
                   data_image = "textured2.jpg",
                )
        icp.extract_pixels_from_color_image("model")
        icp.extract_pixels_from_color_image("data")
        icp.icp()
        icp.display_images_used_for_corner_based_icp()
        icp.display_results_as_movie()
        icp.cleanup_directory()

Yet another mode for using the module is for registering binary images. The
Examples directory contains six canned scripts that illustrate the
different ways of using this module.

          ''',

      license='Python Software Foundation License',
      keywords='image processing, image registration, computer vision',
      platforms='All platforms',
      classifiers=['Topic :: Scientific/Engineering :: Image Recognition', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3.4'],
      packages=['ICP']
)
