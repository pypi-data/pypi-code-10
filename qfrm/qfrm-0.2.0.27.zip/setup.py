import setuptools

setuptools.setup(
name='qfrm',
version='0.2.0.27',      # MAJOR.MINOR[.PATCH[.sub]], http://semver.org/
description='Quantitative Financial Risk Management: awesome OOP tools for measuring, managing and visualizing risk of financial instruments and portfolios.',
#long_description=open('README.txt').read(),   # ReST source for PyPI QFRM package home page
url='http://oleg.rice.edu/stat-449-649-fall-2015/',
author='Oleg Melnikov',
author_email='xisreal@gmail.com',
maintainer='Oleg Melnikov',
maintainer_email='xisreal@gmail.com',
license='LICENSE.txt',
packages=setuptools.find_packages(exclude=['', '', '']),       # ['qfrm'],
zip_safe=False,
keywords='finance risk management bond duration yield curve duration PVCF present value of cash flows IRR TVM NPV interest rate ',
classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Financial and Insurance Industry',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Topic :: Office/Business :: Financial',
    'Topic :: Office/Business :: Financial :: Investment',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Utilities',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
],
    # Core modules: time, math, numbers, warnings, itertools, re,
install_requires=[
    'pandas>=0.16', 'numpy>=1.9', 'scipy>=0.16', 'matplotlib>=1.4', 'statistics>=1.0.3',
],
)

"""
TODO:
keyword, examples, platforms
from __future__ import...
remove dependencies: scipy, numpy
Move PDFs to rice.edu
Re-usable docstrings
Python 3.4
Python 2.x
Update qfrm PyPI page (how does it count number of matches when search is done?)
Inherit European
Inherit all equivalent option names
Finish Boston option
PerpetualAmerican: allow ignoring T value (set to inf)
yaml to convert array to tuple before dump
move rng_seed to parent class



Package tutorials
-----------------------
python-packaging-user-guide.readthedocs.org/en/latest/
https://docs.python.org/3.5/tutorial/modules.html#importing-from-a-package
docs.python.org/3.4/distutils/
packaging.python.org/en/latest/
pythonhosted.org/setuptools/setuptools.html
the-hitchhikers-guide-to-packaging.readthedocs.org/en/latest
thomas-cokelaer.info/tutorials/sphinx/docstring_python.html
pymotw.com/2/doctest
epydoc.sourceforge.net/fields.html
peterdowns.com/posts/first-time-with-pypi.html
pythonwheels.com/
thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html#images-and-figures
docutils.sourceforge.net/docs/user/rst/quickref.html#external-hyperlink-targets
stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip

Packaging commands
----------------------
python setup.py register      # save PyPI account login to local PC
python setup.py sdist         # create qfrm*.zip distribution file
python setup.py sdist -n      #-- dry run
python setup.py sdist upload
python setup.py bdist_wheel   #-- build a wheel (pre-built package, easier for end-user)
python setup.py sdist bdist_wininst upload  #-- build/upload windows installer
python setup.py sdist bdist_wheel upload    #-- build/upload package+ wheels

Installing from PyPI
----------------------
pip install -v qfrm         # pip may erroneousely use older version. delete old installation files manually
pip install --upgrade qfrm
pip install -v qfrm==0.2.0.4    # install specific version
pip uninstall qfrm

"""
