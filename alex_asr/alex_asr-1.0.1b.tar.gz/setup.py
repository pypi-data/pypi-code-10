#!/usr/bin/env python
# encoding: utf-8
# cython: embedsignature=True

from __future__ import print_function
from setuptools import setup, find_packages
from sys import version_info as python_version
import os
from distutils.extension import Extension
from Cython.Distutils import build_ext
from os import environ
from sys import stderr
from sys import platform


install_requires = ['cython>=0.21', 'pystache>=0.5', 'pyyaml>=3.11']
if python_version < (2, 7):
    new_27 = ['ordereddict', 'argparse']
    install_requires.extend(new_27)

extra_link_args = []
extra_objects = []
#environ.get('ADDLIBS', '').split()
extra_compile_args = []
#environ.get('CXXFLAGS', '').split()
kaldi_dir = environ.get('KALDI_DIR', 'libs/kaldi')
library_dirs = ['/usr/lib']
libraries = ['lapack_atlas', 'cblas', 'atlas', 'f77blas', 'm', 'pthread', 'dl']


def kaldi_path(path):
    return os.path.join(kaldi_dir, path)


class build_ext_with_make(build_ext):
    def run(self):
        os.system('bash prepare_env.sh')
        os.system('make')
        with open('setup.py.add_libs') as f_in:
            extra_objects.extend(f_in.read().split())
        with open('setup.py.cxxflags') as f_in:
            extra_compile_args.extend(f_in.read().split())
        build_ext.run(self)


setup(
    name='alex_asr',
    packages=find_packages(exclude=["alex_asr/decoder.cpp"]),
    include_package_data=True,
    cmdclass={'build_ext': build_ext_with_make},
    version='1.0.1b',
    install_requires=install_requires,
    setup_requires=['cython>=0.19.1', 'nose>=1.0'],
    ext_modules=[
        Extension('alex_asr.decoder',
            language='c++',
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            include_dirs=[
                '.',
                kaldi_path('tools/openfst/include'),
                kaldi_path('src'),
            ],
            library_dirs=library_dirs,
            libraries=libraries,
            extra_objects=extra_objects,
            sources=['alex_asr/decoder.pyx', ],
        ),
        Extension(name='alex_asr.fst._fst',
            extra_compile_args=extra_compile_args + ['-std=c++11'],
            extra_link_args=extra_link_args,
            include_dirs=[
                '.',
                kaldi_path('tools/openfst/include'),
                kaldi_path('src'),
            ],
            extra_objects=extra_objects,
            sources=['alex_asr/fst/_fst.pyx'],
            language='c++'
        )
    ],
    author='Charles University in Prague (Lukas Zilka)',
    author_email='lukas@zilka.me',
    url='https://github.com/UFAL-DSG/alex-asr',
    license='Apache Software License 2.0',
    keywords='asr, speech recognition, decoder, speech',
    description='Incremental speech recognition decoder for Kaldi NNET2 and GMM models.',
    download_url='https://github.com/UFAL-DSG/alex-asr/archive/v1.0.0b.tar.gz',
    long_description='',
    classifiers='''
        Programming Language :: Python :: 2
        Programming Language :: Python :: 3
        License :: OSI Approved :: Apache Software License
        Operating System :: POSIX :: Linux
        Topic :: Multimedia :: Sound/Audio :: Speech
        Topic :: Scientific/Engineering
        Intended Audience :: Developers
        Intended Audience :: Science/Research
        Intended Audience :: Telecommunications Industry
        Environment :: Console
        '''.strip().splitlines(),
)
