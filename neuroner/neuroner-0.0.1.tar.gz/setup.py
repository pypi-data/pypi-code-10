# to publish this as a pypi module:
# 1. change (increase) version id in `setup.py`
# 2. python setup.py sdist register upload

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding

#with open('README.rst') as f:
#    readme = f.read()

setup(
    name='neuroner',
    version='0.0.1',
    description='named entity recognition for neurons',
    long_description='named entity recognition for neurons',
    url='https://github.com/renaud/checktype',
    author='Renaud Richardet, Shreejoy Tripathy',
    author_email='renaud@apache.org, stripathy@chibi.ubc.ca',
    license='Apache License (2.0)',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
         'Operating System :: OS Independent',
         'Environment :: Console',
    ],
    keywords='neuroscience',
    py_modules=['similarity']
)
