from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension("lreplay",
                sources=["lreplay.pyx"],
                language="c++")

# setup(name="lreplay",
#       ext_modules=cythonize(ext),
#
#
#
#
#
#
#       )
#
#
# from setuptools import setup
# from setuptools import find_packages


setup(name='lreplay',
      version='0.1.1',
      description='lreplay',
      url='http://bitbucket.com/fingul/loudness_replay',
      author='fingul',
      author_email='fingul@gmail.com',
      license='MIT',
      # packages=['funniest'],
      zip_safe=False,
      install_requires = ['cython'],

      ext_modules=cythonize(ext)
      )
