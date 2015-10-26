"""
DICEseq - Dynamic RNA splicing estimator via sequencing data
See:
http://diceseq.sourceforge.net
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
    
reqs = ['numpy', 'scipy', 'matplotlib','h5py','pysam']

setup(
    name='diceseq',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0',

    description='DICEseq',
    long_description=long_description,

    # The project's main homepage.
    url='http://diceseq.sourceforge.net',

    # Author details
    author='Yuanhua Huang',
    author_email='Y.Huang@ed.ac.uk',

    # Choose your license
    license='MIT',

    # What does your project relate to?
    keywords=['RNA splicing', 'RNA-seq', 'dynamics', 'probabilistic models'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),#['diceseq', 'diceseq.utils', 'diceseq.models'],#

    entry_points={
          'console_scripts': [
              'diceseq = diceseq.diceseq:main',
              'dice-static = diceseq.diceseq_static:main',
              'dice-count = diceseq.dice_count:main',
              'dice-simulate = diceseq.read_simulate:main',
              'dice-bias = diceseq.bias_estimate:main',
              'dice-biasplot = diceseq.bias_plot:main',
              'dice-biasmerge = diceseq.bias_merge:main',
              ],
          }, 

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    
    install_requires=reqs,

    py_modules = ['diceseq']

)