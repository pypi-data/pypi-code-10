# -*- coding: utf-8 -*-
"""
This module contains the tool of cykooz.recipe.patch
"""
from setuptools import setup, find_packages

version = '0.1'
long_description = '\n'.join([
    open('README.rst').read(), 'Download', '********'
])
entry_point = 'cykooz.recipe.patch:Recipe'
entry_points = {'zc.buildout': ['default = %s' % entry_point]}
tests_require = ['zope.testing', 'zc.buildout[test]']


setup(
    name='cykooz.recipe.patch',
    version=version,
    description='recipe for patching eggs',
    long_description=long_description,
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
    keywords='buildout recipe patch',
    author='Rok Garbas',
    author_email='rok.garbas@gmail.com',
    maintainer='Kirill Kuzminykh',
    maintainer_email='saikuz@mail.ru',
    url='https://github.com/cykooz/cykooz.recipe.patch',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['cykooz', 'cykooz.recipe'],
    include_package_data=True,
    install_requires=[
        'setuptools',
        'zc.buildout',
        # -*- Extra requirements: -*-
        'zc.recipe.egg',
    ],
    tests_require=tests_require,
    extras_require={'tests': tests_require},
    test_suite='cykooz.recipe.patch.tests.test_docs.test_suite',
    entry_points=entry_points,
    zip_safe=True,
)
