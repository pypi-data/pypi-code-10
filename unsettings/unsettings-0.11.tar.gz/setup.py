#!/usr/bin/env python
#-*- coding: utf-8-*-


#
# Unsettings - a configuration frontend for the Unity desktop environment
#
# Copyright (C) 2012 Florian Diesch <devel@florian-diesch.de>
#
# Homepage: http://www.florian-diesch.de/software/unsettings/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import glob

from setuptools import setup, find_packages

try:
    from DistUtilsExtra.command import *
except ImportError:
    raise RuntimeError('To build Unsettings you need https://launchpad.net/python-distutils-extra')


def read_from_file(path):
    with open(path) as input:
        return input.read()

import  _meta

setup(
    name='unsettings',
    version=_meta.VERSION,

    packages=find_packages(),
    include_package_data=True,
    maintainer='Florian Diesch',
    maintainer_email='devel@florian-diesch.de',
    author = "Florian Diesch",
    author_email = "devel@florian-diesch.de",    
    description='A configuration frontend for the Unity desktop environment',
    long_description=read_from_file('README.txt'),
    license='GPLv3',
    url='http://www.florian-diesch.de/software/unsettings/',
    download_url='http://www.florian-diesch.de/software/unsettings/',
    data_files=[
        ('share/unsettings/ui/',
         glob.glob('data/ui/*.ui')),
        ('share/unsettings/icons/',
         glob.glob('data/icons/*.png')),
        ('share/applications',
         glob.glob('data/desktop/*.desktop')),
        ('/etc/X11/Xsession.d/',
          glob.glob('xsession/*')),
        ('share/mime/packages/',
          glob.glob('data/mime/*')),
        ],
    entry_points = {
        'console_scripts': ['unsettings=unsettings:main'],
        },
    keywords = "Ubuntu, Unity, Configuration, GUI, Frontend", 
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Gnome',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Desktop Environment :: Gnome',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Utilities',        
        ],
    cmdclass = { "build" : build_extra.build_extra,
                 "build_i18n" :  build_i18n.build_i18n,
                 "build_help" :  build_help.build_help,
                 "build_icons" :  build_icons.build_icons }
    )
