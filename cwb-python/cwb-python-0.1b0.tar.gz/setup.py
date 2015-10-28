#!/usr/bin/env python
from setuptools import setup, Extension

class lazy_cythonize(list):
    def __init__(self, callback):
        self._list = None
        self.callback = callback
    def c_list(self):
        if self._list is None:
            self._list = self.callback()
        return self._list
    def __iter__(self):
        return iter(self.c_list())
    def __getitem__(self, ii):
        return self.c_list()[ii]
    def __len__(self):
        return len(self.c_list())

# for CWB 2.2
extra_libs = []
# for CWB >= 3.0
# extra_libs=['pcre','glib-2.0']

def extensions():
    try:
        from Cython.Build import cythonize
        incdirs=['src']
    except ImportError:
        cythonize = lambda x: x
        incdirs = []
    ext_modules= [Extension('CWB.CL', ['src/CWB/CL.pyx'],
                            include_dirs=['src'],
                            language='c++',
                            libraries=['cl'] + extra_libs)]
    return cythonize(ext_modules)

def read(fname):
    return open(fname).read()

setup(
    name='cwb-python',
    description='CQP and CL interfaces for Python',
    author='Yannick Versley / Jorg Asmussen',
    author_email='yversley@googlemail.com',
    url='https://bitbucket.org/yannick/cwb-python',
    version='0.1b',
    ext_modules=lazy_cythonize(extensions),
    py_modules=['PyCQP_interface'],
    packages=['CWB', 'CWB.tools'],
    long_description=read('README'),
    entry_points={
        'console_scripts': [
            'cqp2conll = CWB.tools.cqp2conll:main',
            'cqp_bitext = CWB.tools.make_bitext:main',
            'cqp_vocab = CWB.tools.cqp2vocab:cqp2vocab_main'
        ]},
    install_requires=['setuptools>=17', 'cython>=0.19', 'six'],
    package_dir={'': 'py_src'})
