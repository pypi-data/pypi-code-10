"""Setup script of django-bsync"""
from setuptools import setup
from setuptools import find_packages

import bsync

setup(
    name='django-bsync',
    version=bsync.__version__,

    description='bsync with the Django development server',
    long_description=open('README.rst').read(),

    keywords='django, server, runserver, browser-sync',

    author=bsync.__author__,
    author_email=bsync.__email__,
    url=bsync.__url__,

    packages=find_packages(),
    classifiers=[
        'Framework :: Django',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'],

    license=bsync.__license__,
    include_package_data=True,
    # install_requires=['beautifulsoup4>=4.3.2'],
)
