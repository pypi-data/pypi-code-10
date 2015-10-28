# -*- coding: utf-8 -*-
# TODO: open source this thing?
"""
General handling of POSIX file locks (flocks).

This is meant to be entirely general purpose.
pgctl-specific functionality belongs elsewhere.

TODO: put this in its own package?
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import fcntl
import os
from contextlib import contextmanager

import six


class Locked(IOError):
    pass


def acquire(file_or_dir):
    """raises flock.Locked on failure"""
    try:
        fd = os.open(file_or_dir, os.O_CREAT)
    except OSError as error:
        if error.errno == 21:  # is a directory
            fd = os.open(file_or_dir, 0)
        else:
            raise

    try:
        # exclusive, nonblocking
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError as error:
        if error.errno == 11:
            release(fd)
            six.reraise(Locked, Locked(file_or_dir))
        else:
            raise

    return fd


def release(lock):
    os.close(lock)


@contextmanager
def flock(file_or_dir):
    """A context for flock.acquire()."""
    fd = acquire(file_or_dir)
    try:
        yield fd
    finally:
        os.close(fd)

# handy alias =X
flock.Locked = Locked
