#!/usr/bin/env python

from distutils.command.build_ext import build_ext
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

from ttyprompt import ttyprompt


_classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: ISC License (ISCL)',
    'Operating System :: OS Independent',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: Mathematics',
]

with open('README.rst', 'r') as rst_file:
    _long_description = rst_file.read()

_setup_args = {
    'author':           ttyprompt.__author__,
    'author_email':     ttyprompt.__email__,
    'classifiers':      _classifiers,
    'description':      ttyprompt.__doc__,
    'license':          ttyprompt.__license__,
    'long_description': _long_description,
    'name':             'TTYprompt',
    'url':              'https://bitbucket.org/eliteraspberries/ttyprompt',
    'version':          ttyprompt.__version__,
}

_requirements = [
]

_setup_args['install_requires'] = _requirements

tty_module = Extension(
    'ttyprompt.tty',
    sources=['getline.c', 'ttyprompt.c', 'ttyprompt/tty.c'],
    include_dirs=['.'],
)

extensions = [
    tty_module,
]

cython_sources = [
    'ttyprompt/tty.pyx',
]


class BuildExtCommand(build_ext):

    user_options = build_ext.user_options + [
        ('use-cython', None, 'compile Cython sources'),
    ]

    boolean_options = build_ext.boolean_options + [
        'use-cython',
    ]

    def initialize_options(self):
        build_ext.initialize_options(self)
        self.use_cython = False

    def finalize_options(self):
        build_ext.finalize_options(self)

    def run(self):
        if self.use_cython:
            self.compile_cython()
        build_ext.run(self)

    def compile_cython(self):
        global cython_sources
        try:
            from Cython.Build import cythonize
            cythonize(cython_sources)
        except ImportError:
            pass


if __name__ == '__main__':

    setup(
        packages=['ttyprompt'],
        ext_modules=extensions,
        cmdclass={
            'build_ext': BuildExtCommand,
        },
        **_setup_args
    )
