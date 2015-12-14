# -*- coding: utf-8 -*-
import inspect
import os
from contextlib import contextmanager

import sys

from dkfileutils.changed import changed

join = os.path.join


def switch_extension(fname, ext="", old_ext=None):
    """Usage::
    
            switch_extension('a/b/c/d.less', '.css')
    
    """
    name, _ext = os.path.splitext(fname)
    if old_ext:
        assert old_ext == _ext
    return name + ext


def filename(fname):
    return os.path.split(fname)[1]


def min_name(fname, min='.min'):
    name, ext = os.path.splitext(fname)
    return name + min + ext


def version_name(fname):
    if '.min.' in fname:
        pre, post = fname.split('.min.')
        return pre + '-{version}.min.' + post
    else:
        return min_name(fname, '-{version}')
    

@contextmanager
def cd(directory):
    cwd = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(cwd)


class changed_dir(object):
    """Has `glob` changed in `dirname` or `force`
    """
    class NoChange(ValueError):
        pass

    def __init__(self,
                 dirname,
                 glob='**/*',
                 filename='.md5',
                 force=False,
                 msg="nothing to do"):
        self.dirname = dirname
        self.glob = glob
        self.filename = filename
        self.force = force
        self.msg = msg
        self._trace = None

    def __enter__(self):
        if self.force or changed(self.dirname, self.glob, self.filename):
            return
        else:
            print self.msg
            # this horrid hack is just barely ok in task.py code...
            # (expect debuggers/pylint/coverage/etc. to be unhappy)
            self._trace = sys.gettrace()
            sys.settrace(lambda *args, **kw: None)
            frame = inspect.currentframe(1)
            # set the trace function below on parent frame
            frame.f_trace = self.trace

    def trace(self, frame, event, arg):
        # we just entered the with block.. cleanup and exit immediately
        sys.settrace(self._trace)
        raise changed_dir.NoChange()

    def __exit__(self, type, value, traceback):
        return isinstance(value, changed_dir.NoChange)
