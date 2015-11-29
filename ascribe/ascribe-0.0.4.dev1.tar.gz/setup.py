# from codecs import open
from os import path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='ascribe',
    version='0.0.4.dev1',
    description='ascribe api',
    # long_description=long_description,
    url='https://github.com/ascribe/ascribe-api-wrapper',
    author='Oskar Paolini, Sylvain Bellemare',
    author_email='sylvain@ascribe.io',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords=(
        'intellectual property, attribution, ownership, art, blockchain, api '
        'digital work, provenance, spool'
    ),

    py_modules=["ascribe"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['requests'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        # 'dev': ['check-manifest'],
        'test': ['coverage', 'pytest'],
    },
)
