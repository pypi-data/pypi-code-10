from __future__ import absolute_import
from __future__ import print_function

"""
Updated BSM 10/23/2015
Cython extensions work-around adapted from simplejson setup script:
https://github.com/simplejson/simplejson/blob/0bcdf20cc525c1343b796cb8f247ea5213c6557e/setup.py#L110
"""

import sys
from os.path import join
import numpy as np
from setuptools import setup, Extension
from Cython.Distutils import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError

import Cython.Compiler.Options

Cython.Compiler.Options.annotate = False
ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)

NAME = 'PyKrige'
VERSION = '1.3.0'
AUTHOR = 'Benjamin S. Murphy'
EMAIL = 'bscott.murphy@gmail.com'
URL = 'https://github.com/bsmurphy/PyKrige'
DESC = 'Kriging Toolkit for Python'
LDESC = 'PyKrige is a kriging toolkit for Python that supports two- and ' \
        'three-dimensional ordinary and universal kriging.'
PACKAGES = ['pykrige']
PCKG_DAT = {'pykrige': ['README.md', 'CHANGELOG.md', 'LICENSE.txt', 'MANIFEST.in',
                        join('test_data', '*.txt'), join('test_data', '*.asc')]}
REQ = ['numpy', 'scipy', 'matplotlib', 'Cython']
CLSF = ['Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS']

if sys.version_info[0] == 3:
    print("**************************************************")
    print("WARNING: Currently, Cython extensions are not built when using Python 3. "
          "This will be changed in the future. Falling back to pure Python implementation.")
    print("**************************************************")
    try_cython = False
else:
    try_cython = True


class BuildFailed(Exception):
    pass


class TryBuildExt(build_ext):
    def build_extensions(self):
        try:
            build_ext.build_extensions(self)
        except ext_errors:
            print("**************************************************")
            print("WARNING: Cython extensions failed to build. Falling back to pure Python implementation.\n"
                  "See https://github.com/bsmurphy/PyKrige/issues/8 for more information.")
            print("**************************************************")
            raise BuildFailed()


# This is how I was originally trying to get around the Cython extension troubles...
# Keeping it here for reference...
#
# class BuildExtCompilerCheck(build_ext):
#     def build_extensions(self):
#         if sys.platform == 'win32' and ('MSC' in sys.version or 'MSVC' in sys.version):
#             print("-> COMPILER IS", self.compiler.compiler_type)
#             from distutils.msvccompiler import MSVCCompiler
#             if isinstance(self.compiler, MSVCCompiler):
#                 build_ext.build_extensions(self)
#             else:
#                 print("WARNING: The C extensions will not be built since the necessary compiler could not be found.\n"
#                       "See https://github.com/bsmurphy/PyKrige/issues/8")
#         else:
#             build_ext.build_extensions(self)

def run_setup(with_cython):

    if with_cython:

        if sys.platform != 'win32':
            compile_args = dict(extra_compile_args=['-O2', '-march=core2', '-mtune=corei7'],
                                extra_link_args=['-O2', '-march=core2', '-mtune=corei7'])
        else:
            compile_args = {}
        ext_modules = [Extension("pykrige.lib.cok", ["pykrige/lib/cok.pyx"], **compile_args),
                       Extension("pykrige.lib.lapack", ["pykrige/lib/lapack.pyx"], **compile_args),
                       Extension("pykrige.lib.variogram_models", ["pykrige/lib/variogram_models.pyx"], **compile_args)]
        cmd = {'build_ext': TryBuildExt}

        setup(name=NAME, version=VERSION, author=AUTHOR, author_email=EMAIL, url=URL, description=DESC,
              long_description=LDESC, packages=PACKAGES, package_data=PCKG_DAT, requires=REQ, classifiers=CLSF,
              ext_modules=ext_modules, include_dirs=[np.get_include()], cmdclass=cmd)

    else:

        setup(name=NAME, version=VERSION, author=AUTHOR, author_email=EMAIL, url=URL, description=DESC,
              long_description=LDESC, packages=PACKAGES, package_data=PCKG_DAT, requires=REQ, classifiers=CLSF)

try:
    run_setup(try_cython)
except BuildFailed:
    run_setup(False)