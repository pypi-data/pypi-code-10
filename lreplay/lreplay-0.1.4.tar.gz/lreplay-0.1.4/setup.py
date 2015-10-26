from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension("lreplay",
                sources=["lreplay.pyx"],
                language="c++")
ext_modules=cythonize(ext)
setup(name='lreplay',
      version='0.1.4',
      description='lreplay',
      url='http://bitbucket.com/fingul/loudness_replay',
      author='fingul',
      author_email='fingul@gmail.com',
      license='MIT',
      # packages=['funniest'],
      zip_safe=False,
      setup_requires=['cython'],
      ext_modules=ext_modules
      )
