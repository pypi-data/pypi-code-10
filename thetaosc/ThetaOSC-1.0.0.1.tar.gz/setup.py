#!python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import os

ext_modules = [  Extension("generate_map", ["generate_map.pyx"]),
                 ]
ext_modules=cythonize(ext_modules)

setup(
    name = 'ThetaOSC',
    version='1.0.0.1',
    description="Library to control Theta-S through WiFi",
    author="Noboru Yamamoto",
    author_email="noboru.yamamoto@kek.jp",
    #language="c++", # this causes Cython to create C++ source
    ext_modules = ext_modules,
    py_modules=["ThetaOSC"],
)
