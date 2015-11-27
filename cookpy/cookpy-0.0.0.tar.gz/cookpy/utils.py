# -*- coding: utf-8 -*-

import glob as _glob
import sys
import os


def make_tree(path):
    """Make all intermediate directories and the leaf directory itself.

    Similar to `os.makedirs`, but does not raise an exception if the
    leaf directory already exists.
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def glob(pathname):
    """Return an iterator which yields the paths matching a pathname pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.

    Note: The recursive glob was introduced in Python 3.5. This is more
    or less a straight back-port in order to support older versions.
    """
    dirname, basename = os.path.split(pathname)
    if not _glob.has_magic(pathname):
        if basename:
            if os.path.lexists(pathname):
                yield pathname
            else:
                raise FileNotFoundError
        else:
            if os.path.isdir(dirname):
                yield pathname
            else:
                raise NotADirectoryError
        return
    if not dirname:
        if basename == '**':
            for name in _glob2(dirname, basename):
                yield name
        else:
            for name in _glob.glob1(dirname, basename):
                yield name
        return
    if dirname != pathname and _glob.has_magic(dirname):
        dirs = glob(dirname)
    else:
        dirs = [dirname]
    if _glob.has_magic(basename):
        if basename == '**':
            glob_in_dir = _glob2
        else:
            glob_in_dir = _glob.glob1
    else:
        glob_in_dir = _glob.glob0(dirname, basename)
    for dirname in dirs:
        for name in glob_in_dir(dirname, basename):
            yield os.path.join(dirname, name)


def _glob2(dirname, pattern):
    if dirname:
        yield pattern[:0]
    for name in _rlistdir(dirname):
        yield name


def _rlistdir(dirname):
    if not dirname:
        dirname = os.curdir
    try:
        names = os.listdir(dirname)
    except os.error:
        return
    for x in names:
        if not _glob._ishidden(x):
            yield x
            path = os.path.join(dirname, x) if dirname else x
            for y in _rlistdir(path):
                yield os.path.join(x, y)


def disable_stdout():
    sys.stdout = open(os.devnull, 'w')


def enable_stdout():
    sys.stdout = sys.__stdout__
