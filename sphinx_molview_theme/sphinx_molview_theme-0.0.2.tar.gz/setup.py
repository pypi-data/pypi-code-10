import os
from setuptools import setup

setup(
    name = 'sphinx_molview_theme',
    packages = ['sphinx_molview_theme'],
    version = '0.0.2',
    description = 'Sphinx theme for MolView',
    author = 'Herman Bergwerf',
    author_email = 'hermanbergwerf@gmail.com',
    license = 'MIT',
    url = 'https://github.com/molview/sphinx-molview-theme',
    keywords = ['sphinx', 'molview', 'theme'],
    classifiers = [],
    install_requires = [
        'setuptools',
        'sphinx_bootstrap_theme'
    ],
    include_package_data=True,
)
