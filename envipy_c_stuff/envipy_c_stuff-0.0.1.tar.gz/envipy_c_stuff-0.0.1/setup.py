# encoding: utf-8

from setuptools import setup
from setuptools.extension import Extension
import numpy

pkg_name = "envipy_c_stuff"

ext_modules = [
    Extension("%s.meandel" % pkg_name,
              ["%s/meandel.c" % pkg_name, "%s/_meandel.c" % pkg_name],

              )
]

version = "0.0.1"

setup(name=pkg_name,
      version=version,
      author="Uwe Schmitt",
      author_email="mail@uweschmitt.info",
      description="binary extensions for envip",
      license="BSD",
      packages=[pkg_name],
      zip_safe=False,
      include_dirs=[numpy.get_include()],
      ext_modules=ext_modules)
