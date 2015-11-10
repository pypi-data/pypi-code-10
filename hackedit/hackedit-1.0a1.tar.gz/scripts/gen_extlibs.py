"""
This script creates the extlibs.zip archive which contains the 3rd party
libraries use by HackEdit.

This is done in order to simplify the life of the linux maintainers and the
users. You don't need to know about the dependencies (or package) them. Only
the core major depedencies need to be packaged (python3, pyqt5, pip and
setuptools -> most distro already have those packages)

Here is the list of the emedded python packages:
    - all pyqode packages (qt, core, cobol, python, json)
    - future
    - jedi
    - pep8
    - pyflakes
    - boss
    - cement
    - qdarkstyle
    - pygments (maybe this one should be left out so that user can install
                color scheme plugins using pip?)
"""
import os
import shutil

# packages to embed
import pyqode.core
import pyqode.python
import pyqode.cobol
import pyqode.qt

import future

import jedi
import pep8
import pyflakes

import boss
import cement

import qdarkstyle

import pygments


BUILD = '../build'
ZIP = '../data/share/extlibs'


def zipdir(source, destination):
    shutil.make_archive(destination, 'zip', source)


def embed_packages(packages):
    def copy_tree(src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError:
            pass
        else:
            print('copied')

    destination = BUILD
    print('copy packages to build dir')
    for package in packages:
        print('copying package: %s' % package)
        if package.__file__.endswith('__init__.py'):
            # package
            src = os.path.dirname(package.__file__)
            dirname = os.path.split(os.path.dirname(package.__file__))[1]
            dest = os.path.join(destination, dirname)
            if 'pyqode' in package.__file__:
                dest = os.path.join(destination, 'pyqode', dirname)
            print('copying %s to %s' % (src, dest))
            copy_tree(src, dest)
            if 'pyqode' in package.__file__:
                with open(os.path.join(
                        destination, 'pyqode', '__init__.py'), 'w'):
                    pass
        else:
            # single module package, copy it directly
            src = package.__file__
            dest = destination
            shutil.copy(src, dest)

    print('creating zip file')


def create_zip():
    zipdir(BUILD, ZIP)


try:
    os.mkdir(BUILD)
except FileExistsError:
    shutil.rmtree(BUILD)
    os.mkdir(BUILD)
embed_packages([
    # all pyqode packages and deps
    pyqode.qt, pyqode.core, pyqode.python, pyqode.cobol, future, pygments,
    # pyqode python dependencies
    jedi, pep8, pyflakes,
    # boss
    boss, cement,
    # dark stylesheet
    qdarkstyle
])
create_zip()
