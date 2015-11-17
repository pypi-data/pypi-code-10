import subprocess

from distutils.core import setup
from distutils.extension import Extension

import numpy

import versioneer

VERSION='1.0.0'

def compile_args(packages):
	p = subprocess.Popen('pkg-config {} --cflags'.format(' '.join(packages)).split(), stdout=subprocess.PIPE)
	return p.communicate()[0].decode('utf-8').split()

def link_args(packages):
	p = subprocess.Popen('pkg-config {} --libs'.format(' '.join(packages)).split(), stdout=subprocess.PIPE)
	return p.communicate()[0].decode('utf-8').split()

cmdclass = versioneer.get_cmdclass()

try:
	from Cython.Distutils import build_ext
	ext = 'pyx'
	cmdclass['build_ext'] = build_ext
except ImportError:
	ext = 'cpp'



ext_modules = [Extension(
    name         = 'fastlearners.fastlearners_pyx',
    sources      = ['cpppyx/fastlearners.' + ext,
                    'cpppyx/nnset_brute.cpp',
                    #'cpppyx/nnset_flann.cpp',
                    'cpppyx/lwlr.cpp',
                    'cpppyx/predict.cpp'],
    # add your path to where the eigen3 include dir resides.
    include_dirs = [numpy.get_include()],
    language     = 'c++',
    # libraries=
    extra_compile_args = compile_args(['flann', 'eigen3']) + ['-O3'],
    extra_link_args    = link_args(['flann', 'eigen3'])
    )]


setup(
    name         = 'fastlearners',
    version      = VERSION,
    cmdclass     = cmdclass,
    author       = 'Fabien Benureau',
    author_email = 'fabien.benureau@gmail.com',
    url          = 'github.com/humm/fastlearners.git',
    download_url = 'https://github.com/humm/fastlearners/tarball/{}'.format(VERSION),
    maintainer   = 'Fabien Benureau',
    description  = 'C++ implementation of some algorithms for the python learners package',
    license      = 'Open Science License (see fabien.benureau.com/openscience.html)',
    keywords     = 'learning algorithm',
    packages     = ['fastlearners'],
    requires     = ['numpy', 'cython'],
    ext_modules  = ext_modules,
)
