# Copyright (C) 2015 Okami, okami@fuzetsu.info

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import fnmatch
import glob
import os
import shutil
import sys

from setuptools import setup
from zipfile import ZipFile


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Code borrowed from wxPython's setup and config files
# Thanks to Robin Dunn for the suggestion.
# I am not 100% sure what's going on, but it works!
def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)


# https://wiki.python.org/moin/Distutils/Tutorial
def find_data_files(srcdir, *wildcards, **kw):
    # get a list of all files under the srcdir matching wildcards,
    # returned in a format to be used for install_data
    def walk_helper(arg, dirname, files):
        if '.svn' in dirname:
            return
        names = []
        lst, wildcards = arg
        for wc in wildcards:
            wc_name = opj(dirname, wc)
            for f in files:
                filename = opj(dirname, f)

                if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                    names.append(filename)
        if names:
            lst.append((dirname, names))

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper(
            (file_list, wildcards),
            srcdir,
            [os.path.basename(f) for f in glob.glob(opj(srcdir, '*'))])
    return file_list


setup_conf = {
    'name': 'pqpasswords',
    'version': '0.0.1',
    'author': 'Okami',
    'author_email': 'okami@fuzetsu.info',
    'description': 'PWSafe3 compatible Password Manager',
    'license': 'GPLv3',
    'keywords': 'pqpasswords password safe',
    'url': 'https://sf.net/p/pqpasswords',
    'long_description': 'Password Safe v3 compatible Password Manager',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security :: Cryptography',
    ],
    'packages': [
        'pqpw',
        'pqpw.media',
        'pqpw.twofish',
        'pqpw.widgets',
    ],
    'scripts': ['PQPasswords'],
    'data_files': (
        find_data_files('share/applications', '*.desktop', recursive=False) +
        find_data_files('share/icons', '*.svg', recursive=False) +
        find_data_files('share/mime/packages', '*.xml', recursive=False)),
    'package_data': {
        'pqpw': ['media/*.svg']
    },
    'include_package_data': True,
}


manefest = open('MANIFEST.in', 'w+')
# extra packages
manefest.write('include pqpw/media *.svg\n')
# data files
manefest.write('include share/applications/*.desktop\n')
manefest.write('include share/icons/*.svg\n')
manefest.write('include share/mime/packages/*.xml\n')


if sys.platform in ('win32', 'cygwin'):
    import py2exe

    # pyqt4 svg parsers
    if not os.path.exists('imageformats'):
        import PyQt4
        pyqt4_imageformats = os.path.join(
            os.path.dirname(PyQt4.__file__), 'plugins', 'imageformats')
        shutil.copytree(pyqt4_imageformats, 'imageformats')
    manefest.write('include imageformats *.dll\n')

    setup_conf.update({
        'setup_requires': ['py2exe'],
        'windows': [{
            'script':'PQPasswords',
            'icon_resources': [(1, 'pqpw/media/icon.ico')],
        }],
        'data_files': find_data_files('imageformats', '*.dll', recursive=False),
        'zipfile': 'pqpw.zip',
        'options': {
            'py2exe': {
                'bundle_files': 1,
                'compressed': True,
                'includes':  [
                    'pqpw',
                    'pqpw.media',
                    'sip',
                    'PyQt4.QtSvg',
                    'PyQt4.QtXml',
                ],
                'dll_excludes': [
                    'w9xpopen.exe',
                    'MSVCP90.dll',
                ],
            }
        }
    })


manefest.close()
setup(**setup_conf)

if sys.platform in ('win32', 'cygwin'):
    # add missing resources to zip
    z = ZipFile('dist/pqpw.zip', mode='a')
    for dir_, files in find_data_files('pqpw/media', '*.svg', recursive=False):
        z.write(dir_)
        for f in files:
            z.write(f)
    z.close()
