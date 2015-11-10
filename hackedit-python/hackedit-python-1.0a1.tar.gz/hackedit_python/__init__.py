"""
This package contains a set of plugins that add basic python support to
HackEdit.
"""
import os
import sys


__version__ = '1.0a1'


BASE = os.path.join(sys.prefix, 'share/hackedit_python/')
if not os.path.exists(BASE):
    BASE = os.path.join(sys.prefix, 'local/share/hackedit_python/')
if not os.path.exists(BASE):
    BASE = '/usr/local/share/hackedit_python/'
ZIP_PATH = os.path.join(BASE, 'extlibs.zip')

if not os.path.exists(ZIP_PATH):
    # running from bootstrap.py
    ZIP_PATH = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'data', 'share', 'extlibs.zip'))

# append insead of prepend to allow user to
# install another version if they want to...
sys.path.insert(0, ZIP_PATH)


try:
    # make sure our icons are imported
    from .forms import hackedit_python_rc
except ImportError:
    # not generated yet
    hackedit_python_rc = None
