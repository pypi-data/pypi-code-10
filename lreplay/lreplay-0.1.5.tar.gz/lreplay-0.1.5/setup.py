import sys

try:
    from setuptools import setup
    from setuptools.extension import Extension
except ImportError:
    print("Couldn't import setuptools. Install `pip` and rerun.")
    sys.exit(1)

#
# Force `setup_requires` stuff like Cython to be installed before proceeding
#
from setuptools.dist import Distribution
Distribution(dict(setup_requires='Cython'))

try:
    from Cython.Build import cythonize
except ImportError:
    print("Could not import Cython.Distutils. Install `cython` and rerun.")
    sys.exit(1)

ext = Extension("lreplay",
                sources=["lreplay.pyx"],
                language="c++")
ext_modules=cythonize(ext)
setup(name='lreplay',
      version='0.1.5',
      description='lreplay',
      url='http://bitbucket.com/fingul/loudness_replay',
      author='fingul',
      author_email='fingul@gmail.com',
      license='MIT',
      # packages=['funniest'],
      zip_safe=False,
      setup_requires=['Cython'],
      ext_modules=ext_modules
      )
