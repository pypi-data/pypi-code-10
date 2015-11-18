"""
Tutorial: http://python-packaging.readthedocs.org/en/latest/minimal.html

After editing setup.py,

To build a package locally:

    $ python setup.py install

    or

    $ python setup.py develop

To publish your package on Pypi:

    $ python setup.py register
    $ python setup.py sdist
    $ python setup.py sdist upload

    or one line command

    $ python setup.py register sdist upload
"""

from setuptools import setup

setup(
    name='okgtreg',
    version='0.13',
    description='Implementation of Optimal Kernel Group Optimization for regression',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Programming Language :: Python :: 2.7',
    ],
    keywords='OKGT regression exploratory data analysis',
    url='http://www.stat.purdue.edu/~panc',
    author='Pan Chao',
    author_email='panc@purdue.edu',
    packages=['okgtreg'],
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn'
    ],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose']
)