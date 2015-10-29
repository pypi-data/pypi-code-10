# -*- coding: utf-8 -*-
"""PyQt doc"""

from distutils.core import setup
import os
import os.path as osp

def get_data_files(dirname):
    """Return data files in directory *dirname*"""
    flist = []
    for dirpath, _dirnames, filenames in os.walk(dirname):
        for fname in filenames:
            flist.append(osp.join(dirpath, fname))
    return flist

setup(name='PyQtdoc', version='4.8.4',
      description='PyQtdoc installs Qt documentation for PyQt4',
      long_description="""PyQtdoc installs Qt official documentation 
(.ch files, i.e. Qt assitant format) in PyQt4 directory""",
      data_files=[(r'Lib\site-packages\PyQt4\doc\qch', get_data_files('qch'))],
      requires=["PyQt4 (>4.3)",],
      author = "Pierre Raybaut",
      author_email = 'pierre.raybaut@gmail.com',
      url = 'http://code.google.com/p/winpython/',
      classifiers=['Operating System :: Microsoft :: Windows'])
