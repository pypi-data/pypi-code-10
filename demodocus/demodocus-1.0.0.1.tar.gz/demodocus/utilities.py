#!/usr/bin/env python
# coding=utf-8

"""
This file contains a collection of miscellaneous utility functions.
"""

from __future__ import absolute_import
from __future__ import print_function
import os
import shutil
import stat
import tempfile

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"

def print_error(msg):
    print(u"[ERRO] %s" % msg)

def print_info(msg):
    print(u"[INFO] %s" % msg)

def create_temp_file(extension=None):
    tmp_handler, tmp_path = tempfile.mkstemp(suffix=extension)
    return (tmp_handler, tmp_path)

def create_temp_directory():
    return tempfile.mkdtemp()

def delete_file(handler, path):
    """
    Safely delete file.

    :param handler: the file handler (as returned by tempfile)
    :type  handler: obj
    :param path: the file path
    :type  path: string (path)
    """
    if handler is not None:
        try:
            os.close(handler)
        except:
            pass
    if path is not None:
        try:
            os.remove(path)
        except:
            pass

def delete_directory(path):
    """
    Safely delete a directory.

    :param path: the file path
    :type  path: string (path)
    """
    def remove_readonly(func, path, _):
        """
        Clear the readonly bit and reattempt the removal

        Adapted from https://docs.python.org/3.5/library/shutil.html#rmtree-example

        See also http://stackoverflow.com/questions/2656322/python-shutil-rmtree-fails-on-windows-with-access-is-denied
        """
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except:
            pass
    if path is not None:
        shutil.rmtree(path, onerror=remove_readonly)



