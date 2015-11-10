#!/usr/bin/env python

# $Id: setup.py,v 546c6d3e03eb 2015/11/10 13:03:03 jon $

from distutils.core import setup

setup(name="jonpy",
      version="0.12",
      description="Jon's Python modules",
      author="Jon Ribbens",
      author_email="jon+jonpy@unequivocal.co.uk",
      url="http://jonpy.sourceforge.net/",
      packages=['jon', 'jon.wt']
)
