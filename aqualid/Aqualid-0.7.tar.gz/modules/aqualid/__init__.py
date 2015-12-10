#!/usr/bin/env python
#
# THIS FILE WAS AUTO-GENERATED. DO NOT EDIT!
#
# Copyright (c) 2011-2015 of the Aqualid project, site: https://github.com/aqualid
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import base64
import binascii
import cProfile
import errno
import fnmatch
import gc
import hashlib
import imp
import inspect
import io
import itertools
import locale
import logging
import marshal
import mmap
import multiprocessing
import operator
import os
import os.path
import pstats
import re
import shutil
import site
import sqlite3
import struct
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import traceback
import types
import weakref
import zipfile
try:
    import cPickle as pickle
except ImportError:
    import pickle
_KNOWN_TYPE_NAMES = {}
_KNOWN_TYPE_IDS = {}
class EntityPickler (object):
    __slots__ = ('pickler', 'unpickler', 'buffer')
    def __init__(self):
        membuf = io.BytesIO()
        pickler = pickle.Pickler(membuf, protocol=pickle.HIGHEST_PROTOCOL)
        unpickler = pickle.Unpickler(membuf)
        pickler.persistent_id = self.persistent_id
        unpickler.persistent_load = self.persistent_load
        self.pickler = pickler
        self.unpickler = unpickler
        self.buffer = membuf
    @staticmethod
    def persistent_id(entity, known_type_names=_KNOWN_TYPE_NAMES):
        entity_type = type(entity)
        type_name = _pickle_type_name(entity_type)
        try:
            type_id = known_type_names[type_name]
            return type_id, entity.__getnewargs__()
        except KeyError:
            return None
    @staticmethod
    def persistent_load(pid, known_type_ids=_KNOWN_TYPE_IDS):
        type_id, new_args = pid
        try:
            entity_type = known_type_ids[type_id]
            return entity_type.__new__(entity_type, *new_args)
        except KeyError:
            raise pickle.UnpicklingError("Unsupported persistent object")
    def dumps(self, entity):
        buf = self.buffer
        buf.seek(0)
        buf.truncate(0)
        pickler = self.pickler
        pickler.dump(entity)
        pickler.clear_memo()   # clear memo to pickle another entity
        return buf.getvalue()
    def loads(self, bytes_object):
        buf = self.buffer
        buf.seek(0)
        buf.truncate(0)
        buf.write(bytes_object)
        buf.seek(0)
        return self.unpickler.load()
def _pickle_type_name(entity_type):
    return entity_type.__module__ + '.' + entity_type.__name__
def pickleable(entity_type,
               known_type_names=_KNOWN_TYPE_NAMES,
               known_type_ids=_KNOWN_TYPE_IDS):
    if type(entity_type) is type:
        type_name = _pickle_type_name(entity_type)
        type_id = binascii.crc32(type_name.encode("utf-8")) & 0xFFFFFFFF
        other_type = known_type_ids.setdefault(type_id, entity_type)
        if other_type is not entity_type:
            raise Exception(
                "Two different type names have identical CRC32 checksum:"
                " '%s' and '%s'" % (_pickle_type_name(other_type), type_name))
        known_type_names[type_name] = type_id
    return entity_type
class AqlInfo (object):
    __slots__ = (
        'name',
        'module',
        'description',
        'version',
        'date',
        'url',
        'license',
    )
    def __init__(self):
        self.name = "Aqualid"
        self.module = "aqualid"
        self.description = "General purpose build system."
        self.version = "0.7"
        self.date = None
        self.url = 'https://github.com/aqualid'
        self.license = "MIT License"
    def dump(self):
        result = "{name} {version}".format(
            name=self.name, version=self.version)
        if self.date:
            result += ' ({date})'.format(date=self.date)
        result += "\n"
        result += self.description
        result += "\nSite: %s" % self.url
        return result
_AQL_VERSION_INFO = AqlInfo()
def get_aql_info():
    return _AQL_VERSION_INFO
def dump_aql_info():
    return _AQL_VERSION_INFO.dump()
try:
    u_str = unicode
except NameError:
    u_str = str
_TRY_ENCODINGS = []
for enc in [
    sys.stdout.encoding,
    locale.getpreferredencoding(False),
    sys.getfilesystemencoding(),
    sys.getdefaultencoding(),
    'utf-8',
]:
    if enc:
        enc = enc.lower()
        if enc not in _TRY_ENCODINGS:
            _TRY_ENCODINGS.append(enc)
def encode_str(value, encoding=None, _try_encodings=_TRY_ENCODINGS):
    if encoding:
        return value.encode(encoding)
    error = None
    for encoding in _try_encodings:
        try:
            return value.encode(encoding)
        except UnicodeEncodeError as ex:
            if error is None:
                error = ex
    raise error
def decode_bytes(obj, encoding=None, _try_encodings=_TRY_ENCODINGS):
    if encoding:
        return u_str(obj, encoding)
    error = None
    for encoding in _try_encodings:
        try:
            return u_str(obj, encoding)
        except UnicodeDecodeError as ex:
            if error is None:
                error = ex
    raise error
def to_unicode(obj, encoding=None):
    if isinstance(obj, (bytearray, bytes)):
        return decode_bytes(obj, encoding)
    return u_str(obj)
def is_unicode(value, _ustr=u_str, _isinstance=isinstance):
    return _isinstance(value, _ustr)
def is_string(value, _str_types=(u_str, str), _isinstance=isinstance):
    return _isinstance(value, _str_types)
if u_str is str:
    to_string = to_unicode
    cast_str = str
else:
    def to_string(value, _str_types=(u_str, str), _isinstance=isinstance):
        if _isinstance(value, _str_types):
            return value
        return str(value)
    def cast_str(obj, encoding=None, _ustr=u_str):
        if isinstance(obj, _ustr):
            return encode_str(obj, encoding)
        return str(obj)
class String (str):
    def __new__(cls, value=None):
        if type(value) is cls:
            return value
        if value is None:
            value = ''
        return super(String, cls).__new__(cls, value)
class IgnoreCaseString (String):
    def __hash__(self):
        return hash(self.lower())
    def _cmp(self, other, op):
        return op(self.lower(), str(other).lower())
    def __eq__(self, other):
        return self._cmp(other, operator.eq)
    def __ne__(self, other):
        return self._cmp(other, operator.ne)
    def __lt__(self, other):
        return self._cmp(other, operator.lt)
    def __le__(self, other):
        return self._cmp(other, operator.le)
    def __gt__(self, other):
        return self._cmp(other, operator.gt)
    def __ge__(self, other):
        return self._cmp(other, operator.ge)
class LowerCaseString (str):
    def __new__(cls, value=None):
        if type(value) is cls:
            return value
        if value is None:
            value = ''
        else:
            value = str(value)
        return super(LowerCaseString, cls).__new__(cls, value.lower())
class UpperCaseString (str):
    def __new__(cls, value=None):
        if type(value) is cls:
            return value
        if value is None:
            value = ''
        else:
            value = str(value)
        return super(UpperCaseString, cls).__new__(cls, value.upper())
class Version (str):
    __ver_re = re.compile(r'[0-9]+[a-zA-Z]*(\.[0-9]+[a-zA-Z]*)*')
    def __new__(cls, version=None, _ver_re=__ver_re):
        if type(version) is cls:
            return version
        if version is None:
            ver_str = ''
        else:
            ver_str = str(version)
        match = _ver_re.search(ver_str)
        if match:
            ver_str = match.group()
            ver_list = re.findall(r'[0-9]+|[a-zA-Z]+', ver_str)
        else:
            ver_str = ''
            ver_list = []
        self = super(Version, cls).__new__(cls, ver_str)
        conv_ver_list = []
        for v in ver_list:
            if v.isdigit():
                v = int(v)
            conv_ver_list.append(v)
        self.__version = tuple(conv_ver_list)
        return self
    @staticmethod
    def __convert(other):
        return other if isinstance(other, Version) else Version(other)
    def _cmp(self, other, cmp_op):
        self_ver = self.__version
        other_ver = self.__convert(other).__version
        len_self = len(self_ver)
        len_other = len(other_ver)
        min_len = min(len_self, len_other)
        if min_len == 0:
            return cmp_op(len_self, len_other)
        self_ver = self_ver[:min_len]
        other_ver = other_ver[:min_len]
        return cmp_op(self_ver, other_ver)
    def __hash__(self):
        return hash(self.__version)
    def __eq__(self, other):
        return self._cmp(other, operator.eq)
    def __ne__(self, other):
        return self._cmp(other, operator.ne)
    def __lt__(self, other):
        return self._cmp(other, operator.lt)
    def __le__(self, other):
        return self._cmp(other, operator.le)
    def __gt__(self, other):
        return self._cmp(other, operator.gt)
    def __ge__(self, other):
        return self._cmp(other, operator.ge)
SIMPLE_TYPES_SET = frozenset(
    (u_str, str, int, float, complex, bool, bytes, bytearray))
SIMPLE_TYPES = tuple(SIMPLE_TYPES_SET)
def is_simple_value(value, _simple_types=SIMPLE_TYPES):
    return isinstance(value, _simple_types)
def is_simple_type(value_type, _simple_types=SIMPLE_TYPES):
    return issubclass(value_type, _simple_types)
class ErrorFileLocked(Exception):
    def __init__(self, filename):
        msg = 'File "%s" is locked.' % (filename,)
        super(ErrorFileLocked, self).__init__(msg)
class GeneralFileLock (object):
    __slots__ = ('lockfilename', 'filename', 'retries', 'interval')
    def __init__(self, filename, interval=0.25, timeout=5 * 60):
        filename = os.path.normcase(os.path.abspath(filename))
        self.filename = filename
        self.lockfilename = filename + '.lock'
        self.interval = interval
        self.retries = int(timeout / interval)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.release_lock()
    def read_lock(self, wait=True, force=False):
        return self.write_lock(wait=wait, force=force)
    def write_lock(self, wait=True, force=False):
        if wait:
            index = self.retries
        else:
            index = 0
        while True:
            try:
                self.__lock(force=force)
                break
            except ErrorFileLocked:
                if index <= 0:
                    raise
            index -= 1
            time.sleep(self.interval)
        return self
    def __lock(self, force=False):
        try:
            os.mkdir(self.lockfilename)
        except OSError as ex:
            if ex.errno == errno.EEXIST:
                if force:
                    return
                raise ErrorFileLocked(self.filename)
            raise
    def release_lock(self):
        try:
            os.rmdir(self.lockfilename)
        except OSError as ex:
            if ex.errno != errno.ENOENT:
                raise
class UnixFileLock(object):
    __slots__ = ('fd', 'filename')
    def __init__(self, filename):
        filename = os.path.normcase(os.path.abspath(filename))
        self.filename = filename
        self.fd = None
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.release_lock()
    def __open(self):
        if self.fd is None:
            self.fd = os.open(self.filename, os.O_CREAT | os.O_RDWR)
    def __close(self):
        os.close(self.fd)
        self.fd = None
    def read_lock(self, wait=True, force=False):
        self.__lock(write=False, wait=wait)
        return self
    def write_lock(self, wait=True, force=False):
        self.__lock(write=True, wait=wait)
        return self
    def __lock(self, write, wait):
        self.__open()
        if write:
            flags = fcntl.LOCK_EX
        else:
            flags = fcntl.LOCK_SH
        if not wait:
            flags |= fcntl.LOCK_NB
        try:
            fcntl.lockf(self.fd, flags)
        except IOError as ex:
            if ex.errno in (errno.EACCES, errno.EAGAIN):
                raise ErrorFileLocked(self.filename)
            raise
    def release_lock(self):
        fcntl.lockf(self.fd, fcntl.LOCK_UN)
        self.__close()
class WindowsFileLock(object):
    def __init_win_types(self):
        self.LOCKFILE_FAIL_IMMEDIATELY = 0x1
        self.LOCKFILE_EXCLUSIVE_LOCK = 0x2
        if ctypes.sizeof(ctypes.c_ulong) != ctypes.sizeof(ctypes.c_void_p):
            ulong_ptr = ctypes.c_int64
        else:
            ulong_ptr = ctypes.c_ulong
        pvoid = ctypes.c_void_p
        dword = ctypes.wintypes.DWORD
        handle = ctypes.wintypes.HANDLE
        class _Offset(ctypes.Structure):
            _fields_ = [
                ('Offset', dword),
                ('OffsetHigh', dword)
            ]
        class _OffsetUnion(ctypes.Union):
            _anonymous_ = ['_offset']
            _fields_ = [
                ('_offset', _Offset),
                ('Pointer', pvoid)
            ]
        class OVERLAPPED(ctypes.Structure):
            _anonymous_ = ['_offset_union']
            _fields_ = [
                ('Internal', ulong_ptr),
                ('InternalHigh', ulong_ptr),
                ('_offset_union', _OffsetUnion),
                ('hEvent', handle)
            ]
        lpoverlapped = ctypes.POINTER(OVERLAPPED)
        self.overlapped = OVERLAPPED()
        self.poverlapped = lpoverlapped(self.overlapped)
        self.LockFileEx = ctypes.windll.kernel32.LockFileEx
        self.UnlockFileEx = ctypes.windll.kernel32.UnlockFileEx
    def __init__(self, filename):
        self.__init_win_types()
        filename = os.path.normcase(os.path.abspath(filename))
        self.filename = filename
        self.fd = None
        self.handle = None
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.release_lock()
    def __open(self):
        if self.fd is None:
            lockfilename = self.filename + ".lock"
            self.fd = os.open(
                lockfilename, os.O_CREAT | os.O_RDWR | os.O_NOINHERIT)
            self.handle = msvcrt.get_osfhandle(self.fd)
    def __close(self):
        os.close(self.fd)
        self.fd = None
        self.handle = None
    def __lock(self, write, wait):
        self.__open()
        if write:
            flags = self.LOCKFILE_EXCLUSIVE_LOCK
        else:
            flags = 0
        if not wait:
            flags |= self.LOCKFILE_FAIL_IMMEDIATELY
        result = self.LockFileEx(
            self.handle, flags, 0, 0, 4096, self.poverlapped)
        if not result:
            raise ErrorFileLocked(self.filename)
    def read_lock(self, wait=True, force=False):
        self.__lock(write=False, wait=wait)
        return self
    def write_lock(self, wait=True, force=False):
        self.__lock(write=True, wait=wait)
        return self
    def release_lock(self):
        self.UnlockFileEx(self.handle, 0, 0, 4096, self.poverlapped)
        self.__close()
try:
    import fcntl
    FileLock = UnixFileLock
except ImportError:
    try:
        import msvcrt
        import ctypes
        import ctypes.wintypes
        FileLock = WindowsFileLock
    except ImportError:
        FileLock = GeneralFileLock
LOG_CRITICAL = logging.CRITICAL
LOG_ERROR = logging.ERROR
LOG_WARNING = logging.WARNING
LOG_INFO = logging.INFO
LOG_DEBUG = logging.DEBUG
class LogFormatter(logging.Formatter):
    __slots__ = ('other',)
    def __init__(self, *args, **kw):
        logging.Formatter.__init__(self, *args, **kw)
        self.other = logging.Formatter("%(levelname)s: %(message)s")
    def format(self, record):
        if record.levelno == logging.INFO:
            return logging.Formatter.format(self, record)
        else:
            return self.other.format(record)
def _make_aql_logger():
    logger = logging.getLogger("AQL")
    handler = logging.StreamHandler()
    formatter = LogFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
_logger = _make_aql_logger()
set_log_level = _logger.setLevel
log_critical = _logger.critical
log_error = _logger.error
log_warning = _logger.warning
log_info = _logger.info
log_debug = _logger.debug
add_log_handler = _logger.addHandler
class Tempfile (str):
    def __new__(cls, prefix='tmp', suffix='', root_dir=None, mode='w+b'):
        handle = tempfile.NamedTemporaryFile(mode=mode, suffix=suffix,
                                             prefix=prefix, dir=root_dir,
                                             delete=False)
        self = super(Tempfile, cls).__new__(cls, handle.name)
        self.__handle = handle
        return self
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.remove()
    def write(self, data):
        self.__handle.write(data)
    def read(self, data):
        self.__handle.read(data)
    def seek(self, offset):
        self.__handle.seek(offset)
    def tell(self):
        return self.__handle.tell()
    def flush(self):
        if self.__handle is not None:
            self.__handle.flush()
    def close(self):
        if self.__handle is not None:
            self.__handle.close()
            self.__handle = None
        return self
    def remove(self):
        self.close()
        try:
            os.remove(self)
        except OSError as ex:
            if ex.errno != errno.ENOENT:
                raise
        return self
class Tempdir(str):
    def __new__(cls, prefix='tmp', suffix='', root_dir=None, name=None):
        if root_dir is not None:
            if not os.path.isdir(root_dir):
                os.makedirs(root_dir)
        if name is None:
            path = tempfile.mkdtemp(prefix=prefix, suffix=suffix, dir=root_dir)
        else:
            if root_dir is not None:
                name = os.path.join(root_dir, name)
            path = os.path.abspath(name)
            if not os.path.isdir(path):
                os.makedirs(path)
        return super(Tempdir, cls).__new__(cls, path)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.remove()
    def remove(self):
        shutil.rmtree(self, ignore_errors=False)
def to_sequence(value, _seq_types=(u_str, bytes, bytearray)):
    if not isinstance(value, _seq_types):
        try:
            iter(value)
            return value
        except TypeError:
            pass
        if value is None:
            return tuple()
    return value,
def is_sequence(value, _seq_types=(u_str, bytes, bytearray)):
    if not isinstance(value, _seq_types):
        try:
            iter(value)
            return True
        except TypeError:
            pass
    return False
class UniqueList (object):
    __slots__ = (
        '__values_list',
        '__values_set',
    )
    def __init__(self, values=None):
        self.__values_list = []
        self.__values_set = set()
        self.__add_values(values)
    def __add_value_front(self, value):
        values_set = self.__values_set
        values_list = self.__values_list
        if value in values_set:
            values_list.remove(value)
        else:
            values_set.add(value)
        values_list.insert(0, value)
    def __add_value(self, value):
        values_set = self.__values_set
        values_list = self.__values_list
        if value not in values_set:
            values_set.add(value)
            values_list.append(value)
    def __add_values(self, values):
        values_set_add = self.__values_set.add
        values_list_append = self.__values_list.append
        values_set_size = self.__values_set.__len__
        values_list_size = self.__values_list.__len__
        for value in to_sequence(values):
            values_set_add(value)
            if values_set_size() > values_list_size():
                values_list_append(value)
    def __add_values_front(self, values):
        values_set = self.__values_set
        values_list = self.__values_list
        values_set_add = values_set.add
        values_list_insert = values_list.insert
        values_set_size = values_set.__len__
        values_list_size = values_list.__len__
        values_list_index = values_list.index
        pos = 0
        for value in to_sequence(values):
            values_set_add(value)
            if values_set_size() == values_list_size():
                i = values_list_index(value)
                if i < pos:
                    continue
                del values_list[i]
            values_list_insert(pos, value)
            pos += 1
    def __remove_value(self, value):
        try:
            self.__values_set.remove(value)
            self.__values_list.remove(value)
        except (KeyError, ValueError):
            pass
    def __remove_values(self, values):
        values_set_remove = self.__values_set.remove
        values_list_remove = self.__values_list.remove
        for value in to_sequence(values):
            try:
                values_set_remove(value)
                values_list_remove(value)
            except (KeyError, ValueError):
                pass
    def __contains__(self, other):
        return other in self.__values_set
    def __len__(self):
        return len(self.__values_list)
    def __iter__(self):
        return iter(self.__values_list)
    def __reversed__(self):
        return reversed(self.__values_list)
    def __str__(self):
        return str(self.__values_list)
    def __eq__(self, other):
        if isinstance(other, UniqueList):
            return self.__values_set == other.__values_set
        return self.__values_set == set(to_sequence(other))
    def __ne__(self, other):
        if isinstance(other, UniqueList):
            return self.__values_set != other.__values_set
        return self.__values_set != set(to_sequence(other))
    def __lt__(self, other):
        if not isinstance(other, UniqueList):
            other = UniqueList(other)
        return self.__values_list < other.__values_list
    def __le__(self, other):
        if isinstance(other, UniqueList):
            other = UniqueList(other)
        return self.__values_list <= other.__values_list
    def __gt__(self, other):
        if isinstance(other, UniqueList):
            other = UniqueList(other)
        return self.__values_list > other.__values_list
    def __ge__(self, other):
        if isinstance(other, UniqueList):
            other = UniqueList(other)
        return self.__values_list >= other.__values_list
    def __getitem__(self, index):
        return self.__values_list[index]
    def __iadd__(self, values):
        self.__add_values(values)
        return self
    def __add__(self, values):
        other = UniqueList(self)
        other.__add_values(values)
        return other
    def __radd__(self, values):
        other = UniqueList(values)
        other.__add_values(self)
        return other
    def __isub__(self, values):
        self.__remove_values(values)
        return self
    def append(self, value):
        self.__add_value(value)
    def extend(self, values):
        self.__add_values(values)
    def reverse(self):
        self.__values_list.reverse()
    def append_front(self, value):
        self.__add_value_front(value)
    def extend_front(self, values):
        self.__add_values_front(values)
    def remove(self, value):
        self.__remove_value(value)
    def pop(self):
        value = self.__values_list.pop()
        self.__values_set.remove(value)
        return value
    def pop_front(self):
        value = self.__values_list.pop(0)
        self.__values_set.remove(value)
        return value
    def self_test(self):
        size = len(self)
        if size != len(self.__values_list):
            raise AssertionError(
                "size(%s) != len(self.__values_list)(%s)" %
                (size, len(self.__values_list)))
        if size != len(self.__values_set):
            raise AssertionError(
                "size(%s) != len(self.__values_set)(%s)" %
                (size, len(self.__values_set)))
        if self.__values_set != set(self.__values_list):
            raise AssertionError("self.__values_set != self.__values_list")
class List (list):
    def __init__(self, values=None):
        super(List, self).__init__(to_sequence(values))
    def __iadd__(self, values):
        super(List, self).__iadd__(to_sequence(values))
        return self
    def __add__(self, values):
        other = List(self)
        other += List(self)
        return other
    def __radd__(self, values):
        other = List(values)
        other += self
        return other
    def __isub__(self, values):
        for value in to_sequence(values):
            while True:
                try:
                    self.remove(value)
                except ValueError:
                    break
        return self
    @staticmethod
    def __to_list(values):
        if isinstance(values, List):
            return values
        return List(values)
    def __eq__(self, other):
        return super(List, self).__eq__(self.__to_list(other))
    def __ne__(self, other):
        return super(List, self).__ne__(self.__to_list(other))
    def __lt__(self, other):
        return super(List, self).__lt__(self.__to_list(other))
    def __le__(self, other):
        return super(List, self).__le__(self.__to_list(other))
    def __gt__(self, other):
        return super(List, self).__gt__(self.__to_list(other))
    def __ge__(self, other):
        return super(List, self).__ge__(self.__to_list(other))
    def append_front(self, value):
        self.insert(0, value)
    def extend(self, values):
        super(List, self).extend(to_sequence(values))
    def extend_front(self, values):
        self[:0] = to_sequence(values)
    def pop_front(self):
        return self.pop(0)
class _SplitListBase(object):
    @classmethod
    def __to_sequence(cls, values):
        if not is_string(values):
            return values
        sep = cls._separator
        for s in cls._other_separators:
            values = values.replace(s, sep)
        return filter(None, values.split(sep))
    @classmethod
    def __to_split_list(cls, values):
        if isinstance(values, cls):
            return values
        return cls(values)
    def __init__(self, values=None):
        super(_SplitListBase, self).__init__(self.__to_sequence(values))
    def __iadd__(self, values):
        return super(_SplitListBase, self).__iadd__(self.__to_sequence(values))
    def __isub__(self, values):
        return super(_SplitListBase, self).__isub__(self.__to_sequence(values))
    def extend(self, values):
        super(_SplitListBase, self).extend(self.__to_sequence(values))
    def extend_front(self, values):
        super(_SplitListBase, self).extend_front(self.__to_sequence(values))
    def __eq__(self, other):
        return super(_SplitListBase, self).__eq__(self.__to_split_list(other))
    def __ne__(self, other):
        return super(_SplitListBase, self).__ne__(self.__to_split_list(other))
    def __lt__(self, other):
        return super(_SplitListBase, self).__lt__(self.__to_split_list(other))
    def __le__(self, other):
        return super(_SplitListBase, self).__le__(self.__to_split_list(other))
    def __gt__(self, other):
        return super(_SplitListBase, self).__gt__(self.__to_split_list(other))
    def __ge__(self, other):
        return super(_SplitListBase, self).__ge__(self.__to_split_list(other))
    def __str__(self):
        return self._separator.join(map(cast_str, iter(self)))
def split_list_type(list_type, separators):
    attrs = dict(_separator=separators[0],
                 _other_separators=separators[1:])
    return type('SplitList', (_SplitListBase, list_type), attrs)
class _ValueListBase(object):
    @classmethod
    def __to_sequence(cls, values):
        if isinstance(values, cls):
            return values
        return map(cls._value_type, to_sequence(values))
    @classmethod
    def __to_value_list(cls, values):
        if isinstance(values, cls):
            return values
        return cls(values)
    def __init__(self, values=None):
        super(_ValueListBase, self).__init__(self.__to_sequence(values))
    def __iadd__(self, values):
        return super(_ValueListBase, self).__iadd__(
            self.__to_value_list(values))
    def __isub__(self, values):
        return super(_ValueListBase, self).__isub__(
            self.__to_value_list(values))
    def extend(self, values):
        super(_ValueListBase, self).extend(self.__to_value_list(values))
    def extend_front(self, values):
        super(_ValueListBase, self).extend_front(self.__to_value_list(values))
    def append(self, value):
        super(_ValueListBase, self).append(self._value_type(value))
    def count(self, value):
        return super(_ValueListBase, self).count(self._value_type(value))
    def index(self, value, i=0, j=-1):
        return super(_ValueListBase, self).index(self._value_type(value), i, j)
    def insert(self, i, value):
        return super(_ValueListBase, self).insert(i, self._value_type(value))
    def remove(self, value):
        return super(_ValueListBase, self).remove(self._value_type(value))
    def __setitem__(self, index, value):
        if type(index) is slice:
            value = self.__to_value_list(value)
        else:
            value = self._value_type(value)
        return super(_ValueListBase, self).__setitem__(index, value)
    def __eq__(self, other):
        return super(_ValueListBase, self).__eq__(self.__to_value_list(other))
    def __ne__(self, other):
        return super(_ValueListBase, self).__ne__(self.__to_value_list(other))
    def __lt__(self, other):
        return super(_ValueListBase, self).__lt__(self.__to_value_list(other))
    def __le__(self, other):
        return super(_ValueListBase, self).__le__(self.__to_value_list(other))
    def __gt__(self, other):
        return super(_ValueListBase, self).__gt__(self.__to_value_list(other))
    def __ge__(self, other):
        return super(_ValueListBase, self).__ge__(self.__to_value_list(other))
    def __contains__(self, other):
        value = self._value_type(other)
        return super(_ValueListBase, self).__contains__(value)
def value_list_type(list_type, value_type):
    attrs = dict(_value_type=value_type)
    return type('ValueList', (_ValueListBase, list_type), attrs)
if os.path.normcase('ABC') == os.path.normcase('abc'):
    FilePathBase = IgnoreCaseString
else:
    FilePathBase = String
try:
    _splitunc = os.path.splitunc
except AttributeError:
    def _splitunc(path):
        return str(), path
class FilePath (FilePathBase):
    def __getnewargs__(self):
        return str(self),
    def __getstate__(self):
        return {}
    def __setstate__(self, state):
        pass
    def __add__(self, other):
        return FilePath(super(FilePath, self).__add__(other))
    def __iadd__(self, other):
        return FilePath(super(FilePath, self).__add__(other))
    def __hash__(self):
        return super(FilePath, self).__hash__()
    def abspath(self):
        return FilePath(os.path.abspath(self))
    def normpath(self):
        return FilePath(os.path.normpath(self))
    def filename(self):
        return FilePath(os.path.basename(self))
    def dirname(self):
        return FilePath(os.path.dirname(self))
    def ext(self):
        return FilePathBase(os.path.splitext(self)[1])
    def name(self):
        return FilePathBase(os.path.splitext(self.filename())[0])
    def drive(self):
        drive, path = os.path.splitdrive(self)
        if not drive:
            drive, path = _splitunc(path)
        return FilePathBase(drive)
    def change(self, dirname=None, name=None, ext=None, prefix=None):
        self_dirname, self_filename = os.path.split(self)
        self_name, self_ext = os.path.splitext(self_filename)
        if dirname is None:
            dirname = self_dirname
        if name is None:
            name = self_name
        if ext is None:
            ext = self_ext
        if prefix:
            name = prefix + name
        return FilePath(os.path.join(dirname, name + ext))
    def join_path(self, *paths):
        return FilePath(os.path.join(self, *paths))
class AbsFilePath (FilePath):
    def __new__(cls, value=None):
        if type(value) is cls:
            return value
        if value is None:
            value = ''
        value = os.path.normcase(os.path.abspath(value))
        return super(AbsFilePath, cls).__new__(cls, value)
try:
    import queue
except ImportError:
    import Queue as queue  # python 2
class _NoLock(object):
    def acquire_shared(self):
        return self
    def acquire_exclusive(self):
        return self
    def release(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
class _SharedLock(object):
    def __init__(self):
        self.cond = threading.Condition(threading.Lock())
        self.count = 0
    def acquire_shared(self):
        cond = self.cond
        with cond:
            while self.count < 0:
                cond.wait()
            self.count += 1
        return self
    def acquire_exclusive(self):
        cond = self.cond
        with cond:
            while self.count != 0:
                cond.wait()
            self.count -= 1
        return self
    def release(self):
        cond = self.cond
        with cond:
            if self.count > 0:
                self.count -= 1
            elif self.count < 0:
                self.count += 1
            cond.notify_all()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
class _Task(object):
    __slots__ = (
        'priority',
        'task_id',
        'func',
        'args',
        'kw'
    )
    def __init__(self, priority, task_id, func, args, kw):
        self.priority = priority
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kw = kw
    def __lt__(self, other):
        if isinstance(other, _NullTask):
            return False
        if isinstance(other, _ExpensiveTask):
            return True
        return self.priority < other.priority
    def __call__(self, lock):
        with lock.acquire_shared():
            return self.func(*self.args, **self.kw)
class _NullTask(_Task):
    __slots__ = (
        'task_id',
    )
    def __init__(self):
        self.task_id = None
    def __lt__(self, other):
        return True
    def __call__(self, lock):
        pass
_null_task = _NullTask()
class _ExpensiveTask(_Task):
    def __init__(self, task_id, func, args, kw):
        super(_ExpensiveTask, self).__init__(None, task_id, func, args, kw)
    def __lt__(self, other):
        return False
    def __call__(self, lock):
        with lock.acquire_exclusive():
            return self.func(*self.args, **self.kw)
class TaskResult (object):
    __slots__ = ('task_id', 'error', 'result')
    def __init__(self, task_id=None, result=None, error=None):
        self.task_id = task_id
        self.result = result
        self.error = error
    def is_failed(self):
        return self.error is not None
    def __lt__(self, other):
        return (self.task_id, self.result, self.error) <                (other.task_id, other.result, other.error)
    def __eq__(self, other):
        return (self.task_id, self.result, self.error) ==                (other.task_id, other.result, other.error)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return "task_id: %s, result: %s, error: %s" %               (self.task_id, self.result, self.error)
class _WorkerThread(threading.Thread):
    def __init__(self, tasks, finished_tasks, task_lock,
                 stop_event, fail_handler):
        super(_WorkerThread, self).__init__()
        self.tasks = tasks
        self.finished_tasks = finished_tasks
        self.task_lock = task_lock
        self.fail_handler = fail_handler
        self.stop_event = stop_event
        self.daemon = True
    def run(self):
        tasks = self.tasks
        finished_tasks = self.finished_tasks
        is_stopped = self.stop_event.is_set
        task_lock = self.task_lock
        while not is_stopped():
            task = tasks.get()
            task_id = task.task_id
            if task_id is not None:
                task_result = TaskResult(task_id=task_id)
            else:
                task_result = None
            try:
                result = task(task_lock)
                if task_result is not None:
                    task_result.result = result
            except BaseException as ex:
                self.fail_handler(task_result, ex)
            finally:
                if task_result is not None:
                    finished_tasks.put(task_result)
                tasks.task_done()
class TaskManager (object):
    __slots__ = (
        'task_lock',
        'num_threads',
        'threads',
        'tasks',
        'finished_tasks',
        'unfinished_tasks',
        'keep_going',
        'stop_event',
        'fail_event',
        'with_backtrace',
    )
    def __init__(self):
        self.tasks = queue.PriorityQueue()
        self.finished_tasks = queue.Queue()
        self.task_lock = _NoLock()
        self.unfinished_tasks = 0
        self.threads = []
        self.keep_going = True
        self.stop_event = threading.Event()
        self.fail_event = threading.Event()
        self.with_backtrace = True
    def start(self, num_threads):
        threads = self.threads
        num_threads -= len(threads)
        args = (self.tasks, self.finished_tasks, self.task_lock,
                self.stop_event, self.fail_handler)
        for i in range(num_threads):
            thread = _WorkerThread(*args)
            threads.append(thread)
            thread.start()
    def stop(self):
        stop_event = self.stop_event
        if not stop_event.is_set():
            stop_event.set()
        put_task = self.tasks.put
        for thread in self.threads:
            put_task(_null_task)
        for thread in self.threads:
            thread.join()
        self.threads[:] = []
        stop_event.clear()
    def __add_task(self, task):
        self.tasks.put(task)
        if task.task_id is not None:
            self.unfinished_tasks += 1
    def add_task(self, priority, task_id, function, *args, **kw):
        task = _Task(priority, task_id, function, args, kw)
        self.__add_task(task)
    def disable_keep_going(self):
        self.keep_going = False
    def disable_backtrace(self):
        self.with_backtrace = False
    def enable_expensive(self):
        if isinstance(self.task_lock, _SharedLock):
            return
        num_threads = len(self.threads)
        self.stop()
        if self.fail_event.is_set():
            return
        self.task_lock = _SharedLock()
        self.start(num_threads)
    def add_expensive_task(self, task_id, function, *args, **kw):
        task = _ExpensiveTask(task_id, function, args, kw)
        self.enable_expensive()
        self.__add_task(task)
    def fail_handler(self, task_result, ex):
        if self.with_backtrace:
            err = traceback.format_exc()
        else:
            err = str(ex)
        if task_result is not None:
            task_result.error = err
        else:
            log_warning("Internal task failed with error: %s", err)
        if not self.keep_going:
            self.fail_event.set()
            self.stop_event.set()
    def get_finished_tasks(self, block=True):
        result = []
        is_stopped = self.stop_event.is_set
        finished_tasks = self.finished_tasks
        if is_stopped():
            self.stop()
        if block:
            block = (self.unfinished_tasks > 0) and self.threads
        while True:
            try:
                task_result = finished_tasks.get(block=block)
                block = False
                result.append(task_result)
                finished_tasks.task_done()
            except queue.Empty:
                if self.tasks.empty() and not self.threads:
                    self.unfinished_tasks = 0
                    return result
                break
        self.unfinished_tasks -= len(result)
        assert self.unfinished_tasks >= 0
        return result
class Dict (dict):
    @staticmethod
    def to_items(items):
        if not items or (items is NotImplemented):
            return tuple()
        try:
            items = items.items
        except AttributeError:
            return items
        return items()
    def __init__(self, items=None):
        super(Dict, self).__init__(self.to_items(items))
    def __iadd__(self, items):
        for key, value in self.to_items(items):
            try:
                self[key] += value
            except KeyError:
                self[key] = value
        return self
    def copy(self, key_type=None, value_type=None):
        other = Dict()
        for key, value in self.items():
            if key_type:
                key = key_type(key)
            if value_type:
                value = value_type(value)
            other[key] = value
        return other
class _SplitDictBase(object):
    @classmethod
    def __to_items(cls, items_str):
        if not is_string(items_str):
            return items_str
        sep = cls._separator
        for s in cls._other_separators:
            items_str = items_str.replace(s, sep)
        items = []
        for v in filter(None, items_str.split(sep)):
            key, _, value = v.partition('=')
            items.append((key, value))
        return items
    @classmethod
    def __to_split_dict(cls, items):
        if isinstance(items, cls):
            return items
        return cls(cls.__to_items(items))
    def __init__(self, items=None):
        super(_SplitDictBase, self).__init__(self.__to_items(items))
    def __iadd__(self, items):
        return super(_SplitDictBase, self).__iadd__(self.__to_items(items))
    def update(self, other=None, **kwargs):
        other = self.__to_items(other)
        super(_SplitDictBase, self).update(other)
        items = self.__to_items(kwargs)
        super(_SplitDictBase, self).update(items)
    def __eq__(self, other):
        return super(_SplitDictBase, self).__eq__(self.__to_split_dict(other))
    def __ne__(self, other):
        return super(_SplitDictBase, self).__ne__(self.__to_split_dict(other))
    def __lt__(self, other):
        return super(_SplitDictBase, self).__lt__(self.__to_split_dict(other))
    def __le__(self, other):
        return super(_SplitDictBase, self).__le__(self.__to_split_dict(other))
    def __gt__(self, other):
        return super(_SplitDictBase, self).__gt__(self.__to_split_dict(other))
    def __ge__(self, other):
        return super(_SplitDictBase, self).__ge__(self.__to_split_dict(other))
    def __str__(self):
        return self._separator.join(sorted("%s=%s" % (key, value)
                                           for key, value in self.items()))
def split_dict_type(dict_type, separators):
    attrs = dict(_separator=separators[0],
                 _other_separators=separators[1:])
    return type('SplitDict', (_SplitDictBase, dict_type), attrs)
class _ValueDictBase(object):
    __VALUE_TYPES = {}
    @classmethod
    def get_key_type(cls):
        return cls._key_type
    @classmethod
    def get_value_type(cls):
        return cls._default_value_type
    @classmethod
    def _to_value(cls, key, value, val_types=__VALUE_TYPES):
        val_type = cls._default_value_type
        try:
            if val_type is None:
                val_type = val_types[key]
            if isinstance(value, val_type):
                return value
            value = val_type(value)
        except KeyError:
            pass
        cls.set_value_type(key, type(value))
        return value
    @classmethod
    def set_value_type(cls, key, value_type, value_types=__VALUE_TYPES):
        default_type = cls._default_value_type
        if default_type is None:
            if value_type is list:
                value_type = List
            if value_type is dict:
                value_type = Dict
            value_types[key] = value_type
    @classmethod
    def __to_items(cls, items):
        if isinstance(items, _ValueDictBase):
            return items
        key_type = cls._key_type
        to_value = cls._to_value
        items_tmp = []
        for key, value in Dict.to_items(items):
            key = key_type(key)
            value = to_value(key, value)
            items_tmp.append((key, value))
        return items_tmp
    @classmethod
    def __to_value_dict(cls, items):
        if isinstance(items, _ValueDictBase):
            return items
        return cls(items)
    def __init__(self, values=None):
        super(_ValueDictBase, self).__init__(self.__to_items(values))
    def __iadd__(self, values):
        return super(_ValueDictBase, self).__iadd__(self.__to_items(values))
    def get(self, key, default=None):
        return super(_ValueDictBase, self).get(self._key_type(key), default)
    def __getitem__(self, key):
        return super(_ValueDictBase, self).__getitem__(self._key_type(key))
    def __setitem__(self, key, value):
        key = self._key_type(key)
        value = self._to_value(key, value)
        return super(_ValueDictBase, self).__setitem__(key, value)
    def __delitem__(self, key):
        return super(_ValueDictBase, self).__delitem__(self._key_type(key))
    def pop(self, key, *args):
        return super(_ValueDictBase, self).pop(self._key_type(key), *args)
    def setdefault(self, key, default):
        key = self._key_type(key)
        default = self._to_value(key, default)
        return super(_ValueDictBase, self).setdefault(key, default)
    def update(self, other=None, **kwargs):
        other = self.__to_items(other)
        super(_ValueDictBase, self).update(other)
        items = self.__to_items(kwargs)
        super(_ValueDictBase, self).update(items)
    def __eq__(self, other):
        return super(_ValueDictBase, self).__eq__(self.__to_value_dict(other))
    def __ne__(self, other):
        return super(_ValueDictBase, self).__ne__(self.__to_value_dict(other))
    def __lt__(self, other):
        return super(_ValueDictBase, self).__lt__(self.__to_value_dict(other))
    def __le__(self, other):
        return super(_ValueDictBase, self).__le__(self.__to_value_dict(other))
    def __gt__(self, other):
        return super(_ValueDictBase, self).__gt__(self.__to_value_dict(other))
    def __ge__(self, other):
        return super(_ValueDictBase, self).__ge__(self.__to_value_dict(other))
    def __contains__(self, key):
        return super(_ValueDictBase, self).__contains__(self._key_type(key))
def value_dict_type(dict_type, key_type, default_value_type=None):
    attrs = dict(_key_type=key_type,
                 _default_value_type=default_value_type)
    return type('ValueDict', (_ValueDictBase, dict_type), attrs)
try:
    zip_longest = itertools.zip_longest
except AttributeError:
    zip_longest = itertools.izip_longest
class ErrorOptionTypeEnumAliasIsAlreadySet(Exception):
    def __init__(self, option, value, current_value, new_value):
        msg = "Alias '%s' of Enum Option '%s' can't be changed to "               "'%s' from '%s'" %              (value, option, new_value, current_value)
        super(ErrorOptionTypeEnumAliasIsAlreadySet, self).__init__(msg)
class ErrorOptionTypeEnumValueIsAlreadySet(Exception):
    def __init__(self, option, value, new_value):
        msg = "Value '%s' of Enum Option '%s' can't be changed to alias "               "to '%s'" % (value, option, new_value)
        super(ErrorOptionTypeEnumValueIsAlreadySet, self).__init__(msg)
class ErrorOptionTypeUnableConvertValue(TypeError):
    def __init__(self, option_help, invalid_value):
        if isinstance(option_help, OptionType):
            option_help = option_help.help()
        self.option_help = option_help
        self.invalid_value = invalid_value
        msg = "Unable to convert value '%s (%s)' to option %s" % (
            invalid_value, type(invalid_value), option_help.error_text())
        super(ErrorOptionTypeUnableConvertValue, self).__init__(msg)
class ErrorOptionTypeNoEnumValues(TypeError):
    def __init__(self, option_type):
        msg = "Enum option type '%s' doesn't have any values." % (option_type,)
        super(ErrorOptionTypeNoEnumValues, self).__init__(msg)
class ErrorOptionTypeCantDeduce(Exception):
    def __init__(self, value):
        msg = "Unable to deduce option type from value type: '%s." % (
            type(value),)
        super(ErrorOptionTypeCantDeduce, self).__init__(msg)
def auto_option_type(value):
    if is_sequence(value):
        unique = isinstance(value, (UniqueList, set, frozenset))
        value_type = type(next(iter(value), ''))
        opt_type = ListOptionType(value_type=value_type, unique=unique)
    elif isinstance(value, dict):
        opt_type = DictOptionType()
    elif isinstance(value, bool):
        opt_type = BoolOptionType()
    elif isinstance(value, IgnoreCaseString):
        opt_type = StrOptionType(ignore_case=True)
    elif is_string(value):
        opt_type = StrOptionType()
    elif isinstance(value, Version):
        opt_type = VersionOptionType()
    elif isinstance(value, FilePath):
        opt_type = PathOptionType()
    elif is_simple_value(value):
        opt_type = OptionType(value_type=type(value))
    else:
        raise ErrorOptionTypeCantDeduce(value)
    opt_type.is_auto = True
    return opt_type
def _get_type_name(value_type):
    if issubclass(value_type, bool):
        name = "boolean"
    elif issubclass(value_type, int):
        name = "integer"
    elif issubclass(value_type, IgnoreCaseString):
        name = "case insensitive string"
    elif issubclass(value_type, (str, u_str)):
        name = "string"
    else:
        name = value_type.__name__
    return name.title()
def _join_to_length(values, max_length=0, separator="", prefix="", suffix=""):
    result = []
    current_value = ""
    for value in values:
        value = prefix + value + suffix
        if len(current_value) + len(value) > max_length:
            if current_value:
                current_value += separator
                result.append(current_value)
                current_value = ""
        if current_value:
            current_value += separator
        current_value += value
    if current_value:
        result.append(current_value)
    return result
def _indent_items(indent_value, values):
    result = []
    indent_spaces = ' ' * len(indent_value)
    for value in values:
        if value:
            if result:
                value = indent_spaces + value
            else:
                value = indent_value + value
        result.append(value)
    return result
def _merge_lists(values1, values2, indent_size):
    result = []
    max_name = max(values1, key=len)
    indent_size = max(indent_size, len(max_name)) + 1
    for left, right in zip_longest(values1, values2, fillvalue=""):
        if not right:
            right_indent = ""
        else:
            right_indent = ' ' * (indent_size - len(left))
        value = left + right_indent + right
        result.append(value)
    return result
class OptionHelp(object):
    __slots__ = (
        'option_type',
        '_names',
        'type_name',
        'allowed_values',
        'current_value',
    )
    def __init__(self, option_type):
        self.option_type = option_type
        help_type = option_type.help_type()
        self.type_name = help_type if help_type else None
        help_range = option_type.help_range()
        self.allowed_values = help_range if help_range else None
        self._names = []
        self.current_value = None
    @property
    def is_key(self):
        return self.option_type.is_tool_key
    @property
    def group(self):
        return self.option_type.group
    @property
    def description(self):
        return self.option_type.description
    @property
    def names(self):
        return self._names
    @names.setter
    def names(self, names):
        self._names = sorted(names, key=str.lower)
    def is_hidden(self):
        return not bool(self.description) or self.option_type.is_hidden
    def _current_value(self, details):
        if self.current_value is not None:
            if isinstance(self.current_value, (list, tuple, UniqueList)):
                current_value = [to_string(v) for v in self.current_value]
                if current_value:
                    current_value = _join_to_length(
                        current_value,
                        64,
                        separator=",",
                        prefix="'",
                        suffix="'")
                    current_value = _indent_items("[ ", current_value)
                    current_value[-1] += " ]"
                    details.extend(current_value)
                else:
                    details.append("[]")
            else:
                current_value = self.option_type.to_str(self.current_value)
                if not current_value:
                    current_value = "''"
                details.append(current_value)
        else:
            details.append("N/A")
    def text(self, brief=False, names_indent=0):
        details = []
        self._current_value(details)
        if not brief:
            if self.description:
                details.append(self.description)
            if self.type_name:
                details.append("Type: " + self.type_name)
            if self.allowed_values:
                details += _indent_items("Allowed values: ",
                                         self.allowed_values)
        details = _indent_items(": ", details)
        result = []
        if self.names:
            names = self.names
            key_marker = '* ' if self.is_key else '  '
            names = [key_marker + name for name in names]
            details = _merge_lists(names, details, names_indent + 2)
        result += details
        return result
    def error_text(self):
        result = []
        if self.names:
            result.append(', '.join(self.names))
        if self.type_name:
            result.append("Type: " + self.type_name)
        if self.allowed_values:
            result.append("Allowed values: %s" %
                          ', '.join(self.allowed_values))
        return '. '.join(result)
class OptionHelpGroup(object):
    __slots__ = (
        'name',
        'max_option_name_length',
        'help_list',
    )
    def __init__(self, group_name):
        self.name = group_name
        self.max_option_name_length = 0
        self.help_list = []
    def append(self, option_help):
        self.max_option_name_length = max(
            self.max_option_name_length, len(max(option_help.names, key=len)))
        self.help_list.append(option_help)
    def __iter__(self):
        return iter(self.help_list)
    def text(self, brief=False, indent=0):
        result = []
        group_name = self.name
        if group_name:
            group_name = "%s:" % (group_name,)
            group_border_bottom = "-" * len(group_name)
            result.extend([group_name, group_border_bottom])
        names_indent = self.max_option_name_length
        self.help_list.sort(key=operator.attrgetter('names'))
        for option_help in self.help_list:
            opt_text = option_help.text(brief, names_indent)
            if (len(opt_text) > 1) and result and result[-1]:
                result.append("")
            result.extend(opt_text)
            if len(opt_text) > 1:
                result.append("")
        if indent:
            result = _indent_items(' ' * indent, result)
        return result
class OptionType (object):
    __slots__ = (
        'value_type',
        'default',
        'description',
        'group',
        'range_help',
        'is_auto',
        'is_tool_key',
        'is_hidden',
    )
    def __init__(self,
                 value_type=str,
                 description=None,
                 group=None,
                 range_help=None,
                 default=NotImplemented,
                 is_tool_key=False,
                 is_hidden=False
                 ):
        if type(value_type) is type and issubclass(value_type, OptionType):
            value_type = value_type()
        self.value_type = value_type
        self.is_auto = False
        self.is_tool_key = is_tool_key
        self.is_hidden = is_hidden
        self.description = description
        self.group = group
        self.range_help = range_help
        if default is NotImplemented:
            self.default = NotImplemented
        else:
            self.default = value_type(default)
    def __call__(self, value=NotImplemented):
        """
        Converts a value to options' value
        """
        try:
            if value is NotImplemented:
                if self.default is NotImplemented:
                    return self.value_type()
                return self.default
            return self.value_type(value)
        except (TypeError, ValueError):
            raise ErrorOptionTypeUnableConvertValue(self, value)
    def to_str(self, value):
        """
        Converts a value to options' value string
        """
        return to_string(value)
    def help(self):
        return OptionHelp(self)
    def help_type(self):
        return _get_type_name(self.value_type)
    def help_range(self):
        """
        Returns a description (list of strings) about range of allowed values
        """
        if self.range_help:
            return list(to_sequence(self.range_help))
        return []
class StrOptionType (OptionType):
    def __init__(self,
                 ignore_case=False,
                 description=None,
                 group=None,
                 range_help=None,
                 is_tool_key=False,
                 is_hidden=False
                 ):
        value_type = IgnoreCaseString if ignore_case else String
        super(StrOptionType, self).__init__(value_type,
                                            description,
                                            group,
                                            range_help,
                                            is_tool_key=is_tool_key,
                                            is_hidden=is_hidden)
class VersionOptionType (OptionType):
    def __init__(self,
                 description=None,
                 group=None,
                 range_help=None,
                 is_tool_key=False,
                 is_hidden=False):
        super(VersionOptionType, self).__init__(Version,
                                                description,
                                                group,
                                                range_help,
                                                is_tool_key=is_tool_key,
                                                is_hidden=is_hidden)
    def help_type(self):
        return "Version String"
class PathOptionType (OptionType):
    def __init__(self,
                 description=None,
                 group=None,
                 range_help=None,
                 is_tool_key=False,
                 is_hidden=False,
                 default=NotImplemented
                 ):
        super(PathOptionType, self).__init__(FilePath,
                                             description,
                                             group,
                                             range_help,
                                             is_tool_key=is_tool_key,
                                             is_hidden=is_hidden,
                                             default=default)
    def help_type(self):
        return "File System Path"
class AbsPathOptionType (OptionType):
    def __init__(self,
                 description=None,
                 group=None,
                 range_help=None,
                 is_tool_key=False,
                 is_hidden=False,
                 default=NotImplemented
                 ):
        super(AbsPathOptionType, self).__init__(AbsFilePath,
                                                description,
                                                group,
                                                range_help,
                                                is_tool_key=is_tool_key,
                                                is_hidden=is_hidden,
                                                default=default)
    def help_type(self):
        return "File System Path"
class BoolOptionType (OptionType):
    __slots__ = (
        'true_value',
        'false_value',
        'true_values',
        'false_values',
        'aliases',
    )
    __true_values = ('yes', 'true', 'on', 'enabled', 'y', '1', 't')
    __false_values = ('no', 'false', 'off', 'disabled', 'n', '0', 'f')
    def __init__(self,
                 description=None,
                 group=None,
                 style=None,
                 true_values=None,
                 false_values=None,
                 default=False,
                 is_tool_key=False,
                 is_hidden=False
                 ):
        super(BoolOptionType, self).__init__(bool, description, group,
                                             default=default,
                                             is_tool_key=is_tool_key,
                                             is_hidden=is_hidden)
        if style is None:
            style = ('true', 'false')
        else:
            style = map(IgnoreCaseString, style)
        if true_values is None:
            true_values = self.__true_values
        else:
            true_values = to_sequence(true_values)
        if false_values is None:
            false_values = self.__false_values
        else:
            false_values = to_sequence(false_values)
        self.true_value, self.false_value = style
        self.true_values = set()
        self.false_values = set()
        self.add_values(true_values, false_values)
        self.add_values(self.true_value, self.false_value)
    def __call__(self, value=NotImplemented):
        if type(value) is bool:
            return value
        if value is NotImplemented:
            value = self.default
        value_str = IgnoreCaseString(value)
        if value_str in self.true_values:
            return True
        if value_str in self.false_values:
            return False
        return True if value else False
    def to_str(self, value):
        return self.true_value if value else self.false_value
    def add_values(self, true_values, false_values):
        true_values = to_sequence(true_values)
        false_values = to_sequence(false_values)
        self.true_values.update(map(IgnoreCaseString, true_values))
        self.false_values.update(map(IgnoreCaseString, false_values))
    def help_range(self):
        def _make_help(value, values):
            values = list(values)
            values.remove(value)
            if values:
                values = ', '.join(sorted(values))
                return "%s (or %s)" % (value, values)
            return "%s" % (value,)
        return [_make_help(self.true_value, self.true_values),
                _make_help(self.false_value, self.false_values), ]
class EnumOptionType (OptionType):
    __slots__ = (
        '__values',
        'strict',
    )
    def __init__(self,
                 values,
                 description=None,
                 group=None,
                 value_type=IgnoreCaseString,
                 default=NotImplemented,
                 strict=True,
                 is_tool_key=False,
                 is_hidden=False
                 ):
        super(EnumOptionType, self).__init__(value_type, description, group,
                                             default=default,
                                             is_tool_key=is_tool_key,
                                             is_hidden=is_hidden)
        self.__values = {}
        if default is not NotImplemented:
            self.add_values(default)
        self.add_values(values)
        self.strict = strict
    def add_values(self, values):
        try:
            values = tuple(values.items())  # convert dictionary to a sequence
        except AttributeError:
            pass
        set_default_value = self.__values.setdefault
        value_type = self.value_type
        for value in to_sequence(values):
            it = iter(to_sequence(value))
            value = value_type(next(it))
            value = set_default_value(value, value)
            for alias in it:
                alias = value_type(alias)
                v = set_default_value(alias, value)
                if v != value:
                    if alias == v:
                        raise ErrorOptionTypeEnumValueIsAlreadySet(
                            self, alias, value)
                    else:
                        raise ErrorOptionTypeEnumAliasIsAlreadySet(
                            self, alias, v, value)
    def _get_default(self):
        value = self.default
        if value is not NotImplemented:
            return value
        try:
            return next(iter(self.__values.values()))
        except StopIteration:
            if self.strict:
                raise ErrorOptionTypeNoEnumValues(self)
        return self.value_type()
    def _convert_value(self, value):
        try:
            value = self.value_type(value)
        except (TypeError, ValueError):
            raise ErrorOptionTypeUnableConvertValue(self, value)
        try:
            return self.__values[value]
        except KeyError:
            if self.strict:
                raise ErrorOptionTypeUnableConvertValue(self, value)
        return value
    def __call__(self, value=NotImplemented):
        if value is NotImplemented:
            return self._get_default()
        return self._convert_value(value)
    def help_range(self):
        values = {}
        for alias, value in self.__values.items():
            if alias is value:
                values.setdefault(alias, [])
            else:
                values.setdefault(value, []).append(alias)
        help_str = []
        for value, aliases in values.items():
            s = to_string(value)
            if aliases:
                s += ' (or ' + ', '.join(map(to_string, aliases)) + ')'
            help_str.append(s)
        return help_str
    def range(self):
        values = []
        for alias, value in self.__values.items():
            if alias is value:
                values.append(alias)
        return values
class RangeOptionType (OptionType):
    __slots__ = (
        'min_value',
        'max_value',
        'restrain',
    )
    def __init__(self,
                 min_value,
                 max_value,
                 description=None,
                 group=None,
                 value_type=int,
                 restrain=True,
                 default=NotImplemented,
                 is_tool_key=False,
                 is_hidden=False
                 ):
        super(RangeOptionType, self).__init__(value_type, description, group,
                                              default=default,
                                              is_tool_key=is_tool_key,
                                              is_hidden=is_hidden)
        self.set_range(min_value, max_value, restrain)
        if default is not NotImplemented:
            self.default = self(default)
    def set_range(self, min_value, max_value, restrain=True):
        if min_value is not None:
            try:
                min_value = self.value_type(min_value)
            except (TypeError, ValueError):
                raise ErrorOptionTypeUnableConvertValue(self, min_value)
        else:
            min_value = self.value_type()
        if max_value is not None:
            try:
                max_value = self.value_type(max_value)
            except (TypeError, ValueError):
                raise ErrorOptionTypeUnableConvertValue(self, max_value)
        else:
            max_value = self.value_type()
        self.min_value = min_value
        self.max_value = max_value
        if restrain is not None:
            self.restrain = restrain
    def __call__(self, value=NotImplemented):
        try:
            min_value = self.min_value
            if value is NotImplemented:
                if self.default is NotImplemented:
                    return min_value
                value = self.default
            value = self.value_type(value)
            if value < min_value:
                if self.restrain:
                    value = min_value
                else:
                    raise TypeError()
            max_value = self.max_value
            if value > max_value:
                if self.restrain:
                    value = max_value
                else:
                    raise TypeError()
            return value
        except TypeError:
            raise ErrorOptionTypeUnableConvertValue(self, value)
    def help_range(self):
        return ["%s ... %s" % (self.min_value, self.max_value)]
    def range(self):
        return [self.min_value, self.max_value]
class ListOptionType (OptionType):
    __slots__ = ('item_type',)
    def __init__(self,
                 value_type=str,
                 unique=False,
                 separators=', ',
                 description=None,
                 group=None,
                 range_help=None,
                 is_tool_key=False,
                 is_hidden=False
                 ):
        if type(value_type) is type and issubclass(value_type, OptionType):
            value_type = value_type()
        if isinstance(value_type, OptionType):
            if description is None:
                description = value_type.description
                if description:
                    description = "List of: " + description
            if group is None:
                group = value_type.group
            if range_help is None:
                range_help = value_type.range_help
        if unique:
            list_type = UniqueList
        else:
            list_type = List
        list_type = value_list_type(list_type, value_type)
        if separators:
            list_type = split_list_type(list_type, separators)
        super(ListOptionType, self).__init__(list_type, description,
                                             group, range_help,
                                             is_tool_key=is_tool_key,
                                             is_hidden=is_hidden)
        self.item_type = value_type
    def __call__(self, values=None):
        try:
            if values is NotImplemented:
                values = []
            return self.value_type(values)
        except (TypeError, ValueError):
            raise ErrorOptionTypeUnableConvertValue(self, values)
    def help_type(self):
        if isinstance(self.item_type, OptionType):
            item_type = self.item_type.help_type()
        else:
            item_type = _get_type_name(self.item_type)
        return "List of %s" % item_type
    def help_range(self):
        if self.range_help:
            return list(to_sequence(self.range_help))
        if isinstance(self.item_type, OptionType):
            return self.item_type.help_range()
        return []
class DictOptionType (OptionType):
    def __init__(self,
                 key_type=str,
                 value_type=None,
                 separators=', ',
                 description=None,
                 group=None,
                 range_help=None,
                 is_tool_key=False,
                 is_hidden=False
                 ):
        if type(value_type) is type and issubclass(value_type, OptionType):
            value_type = value_type()
        if isinstance(value_type, OptionType):
            if description is None:
                description = value_type.description
                if description:
                    description = "List of: " + description
            if group is None:
                group = value_type.group
            if range_help is None:
                range_help = value_type.range_help
        dict_type = value_dict_type(Dict, key_type, value_type)
        if separators:
            dict_type = split_dict_type(dict_type, separators)
        super(DictOptionType, self).__init__(dict_type, description, group,
                                             range_help,
                                             is_tool_key=is_tool_key,
                                             is_hidden=is_hidden)
    def set_value_type(self, key, value_type):
        if isinstance(value_type, OptionType):
            value_type = value_type.value_type
        self.value_type.set_value_type(key, value_type)
    def __call__(self, values=None):
        try:
            if values is NotImplemented:
                values = None
            return self.value_type(values)
        except (TypeError, ValueError):
            raise ErrorOptionTypeUnableConvertValue(self, values)
    def help_type(self):
        value_type = self.value_type.get_value_type()
        if value_type is not None:
            if isinstance(value_type, OptionType):
                value_type = value_type.help_type()
            else:
                value_type = _get_type_name(value_type)
            return "Dictionary of %s" % (value_type,)
        return "Dictionary"
    def help_range(self):
        if self.range_help:
            return list(to_sequence(self.range_help))
        value_type = self.value_type.get_value_type()
        if isinstance(value_type, OptionType):
            return value_type.help_range()
        return []
class ErrorInvalidExecCommand(Exception):
    def __init__(self, arg):
        msg = "Invalid type of command argument: %s(%s)" % (arg, type(arg))
        super(ErrorInvalidExecCommand, self).__init__(msg)
class ErrorFileName(Exception):
    def __init__(self, filename):
        msg = "Invalid file name: %s(%s)" % (filename, type(filename))
        super(ErrorFileName, self).__init__(msg)
class ErrorUnmarshallableObject(Exception):
    def __init__(self, obj):
        msg = "Unmarshallable object: '%s'" % (obj, )
        super(ErrorUnmarshallableObject, self).__init__(msg)
if hasattr(os, 'O_NOINHERIT'):
    _O_NOINHERIT = os.O_NOINHERIT
else:
    _O_NOINHERIT = 0
if hasattr(os, 'O_SYNC'):
    _O_SYNC = os.O_SYNC
else:
    _O_SYNC = 0
if hasattr(os, 'O_BINARY'):
    _O_BINARY = os.O_BINARY
else:
    _O_BINARY = 0
def _open_file_handle(filename, read=True, write=False,
                      sync=False, truncate=False):
    flags = _O_NOINHERIT | _O_BINARY
    if not write:
        flags |= os.O_RDONLY
    else:
        flags |= os.O_CREAT
        if truncate:
            flags |= os.O_TRUNC
        if read:
            flags |= os.O_RDWR
        else:
            flags |= os.O_WRONLY
        if sync:
            flags |= _O_SYNC
    return os.open(filename, flags)
def open_file(filename, read=True, write=False, binary=False,
              sync=False, truncate=False, encoding=None):
    if not is_string(filename):
        raise ErrorFileName(filename)
    if write:
        mode = 'r+'
    else:
        mode = 'r'
    if binary:
        mode += 'b'
    fd = _open_file_handle(filename, read=read, write=write,
                           sync=sync, truncate=truncate)
    try:
        if sync and binary:
            return io.open(fd, mode, 0, encoding=encoding)
        else:
            return io.open(fd, mode, encoding=encoding)
    except:
        os.close(fd)
        raise
def read_text_file(filename, encoding='utf-8'):
    with open_file(filename, encoding=encoding) as f:
        return f.read()
def read_bin_file(filename):
    with open_file(filename, binary=True) as f:
        return f.read()
def write_text_file(filename, data, encoding='utf-8'):
    with open_file(filename, write=True,
                   truncate=True, encoding=encoding) as f:
        if isinstance(data, (bytearray, bytes)):
            data = decode_bytes(data, encoding)
        f.write(data)
def write_bin_file(filename, data, encoding=None):
    with open_file(filename, write=True, binary=True,
                   truncate=True, encoding=encoding) as f:
        if is_unicode(data):
            data = encode_str(data, encoding)
        f.write(data)
def exec_file(filename, file_locals):
    if not file_locals:
        file_locals = {}
    source = read_text_file(filename)
    code = compile(source, filename, 'exec')
    file_locals_orig = file_locals.copy()
    exec(code, file_locals)
    result = {}
    for key, value in file_locals.items():
        if key.startswith('_') or isinstance(value, types.ModuleType):
            continue
        if key not in file_locals_orig:
            result[key] = value
    return result
def dump_simple_object(obj):
    if isinstance(obj, (bytes, bytearray)):
        data = obj
    elif isinstance(obj, u_str):
        data = obj.encode('utf-8')
    else:
        try:
            data = marshal.dumps(obj, 0)  # use version 0, for a raw dump
        except ValueError:
            raise ErrorUnmarshallableObject(obj)
    return data
def simple_object_signature(obj, common_hash=None):
    data = dump_simple_object(obj)
    return data_signature(data, common_hash)
def new_hash(data=b''):
    return hashlib.md5(data)
def data_signature(data, common_hash=None):
    if common_hash is None:
        obj_hash = hashlib.md5(data)
    else:
        obj_hash = common_hash.copy()
        obj_hash.update(data)
    return obj_hash.digest()
def file_signature(filename, offset=0):
    checksum = hashlib.md5()
    chunk_size = checksum.block_size * 4096
    with open_file(filename, binary=True) as f:
        f.seek(offset)
        read = f.read
        checksum_update = checksum.update
        chunk = True
        while chunk:
            chunk = read(chunk_size)
            checksum_update(chunk)
    return checksum.digest()
def file_time_signature(filename):
    stat = os.stat(filename)
    return simple_object_signature((stat.st_size, stat.st_mtime))
def file_checksum(filename, offset=0, size=-1, alg='md5', chunk_size=262144):
    checksum = hashlib.__dict__[alg]()
    with open_file(filename, binary=True) as f:
        read = f.read
        f.seek(offset)
        checksum_update = checksum.update
        chunk = True
        while chunk:
            chunk = read(chunk_size)
            checksum_update(chunk)
            if size > 0:
                size -= len(chunk)
                if size <= 0:
                    break
            checksum_update(chunk)
    return checksum
def get_function_name(currentframe=inspect.currentframe):
    frame = currentframe()
    if frame:
        return frame.f_back.f_code.co_name
    return "__not_available__"
def print_stacks():
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    for thread_id, stack in sys._current_frames().items():
        print("\n" + ("=" * 64))
        print("Thread: %s (%s)" % (id2name.get(thread_id, ""), thread_id))
        traceback.print_stack(stack)
try:
    _getargspec = inspect.getfullargspec
except AttributeError:
    _getargspec = inspect.getargspec
def get_function_args(function, getargspec=_getargspec):
    args = getargspec(function)[:4]
    if isinstance(function, types.MethodType):
        if function.__self__:
            args = tuple([args[0][1:]] + list(args[1:]))
    return args
def equal_function_args(function1, function2):
    if function1 is function2:
        return True
    args1 = get_function_args(function1)
    args2 = get_function_args(function2)
    return args1[0:3] == args2[0:3]
def check_function_args(function, args, kw, getargspec=_getargspec):
    f_args, f_varargs, f_varkw, f_defaults = getargspec(function)[:4]
    current_args_num = len(args) + len(kw)
    args_num = len(f_args)
    if not f_varargs and not f_varkw:
        if current_args_num > args_num:
            return False
    if f_defaults:
        def_args_num = len(f_defaults)
    else:
        def_args_num = 0
    min_args_num = args_num - def_args_num
    if current_args_num < min_args_num:
        return False
    kw = set(kw)
    unknown_args = kw - set(f_args)
    if unknown_args and not f_varkw:
        return False
    def_args = f_args[args_num - def_args_num:]
    non_def_kw = kw - set(def_args)
    non_def_args_num = len(args) + len(non_def_kw)
    if non_def_args_num < min_args_num:
        return False
    twice_args = set(f_args[:len(args)]) & kw
    if twice_args:
        return False
    return True
def remove_files(files):
    for f in to_sequence(files):
        try:
            os.remove(f)
        except OSError as ex:
            if ex.errno != errno.ENOENT:
                raise
def _decode_data(data):
    if not data:
        return str()
    data = to_unicode(data)
    data = data.replace('\r\n', '\n')
    data = data.replace('\r', '\n')
    return data
class ExecCommandException(Exception):
    __slots__ = ('exception',)
    def __init__(self, cmd, exception):
        msg = ' '.join(to_sequence(cmd))
        msg += '\n%s' % (exception,)
        self.exception = exception
        super(ExecCommandException, self).__init__(msg)
    @staticmethod
    def failed():
        return True
    def __bool__(self):
        return self.failed()
    def __nonzero__(self):
        return self.failed()
class ExecCommandResult(Exception):
    __slots__ = ('cmd', 'status', 'stdout', 'stderr')
    def __init__(self, cmd, status=None, stdout=None, stderr=None):
        self.cmd = tuple(to_sequence(cmd))
        self.status = status
        self.stdout = stdout if stdout else ''
        self.stderr = stderr if stderr else ''
        super(ExecCommandResult, self).__init__()
    def __str__(self):
        msg = ' '.join(self.cmd)
        out = self.output()
        if out:
            msg += '\n' + out
        if self.status:
            msg += "\nExit status: %s" % (self.status,)
        return msg
    def failed(self):
        return self.status != 0
    def output(self):
        out = self.stdout
        if self.stderr:
            if out:
                out += '\n'
                out += self.stderr
            else:
                out = self.stderr
        return out
    def __bool__(self):
        return self.failed()
    def __nonzero__(self):
        return self.failed()
try:
    _MAX_CMD_LENGTH = os.sysconf('SC_ARG_MAX')
except AttributeError:
    _MAX_CMD_LENGTH = 32000  # 32768 default for Windows
def _gen_exec_cmd_file(cmd, file_flag, max_cmd_length=_MAX_CMD_LENGTH):
    if not file_flag:
        return cmd, None
    cmd_length = sum(map(len, cmd)) + len(cmd) - 1
    if cmd_length <= max_cmd_length:
        return cmd, None
    cmd_str = subprocess.list2cmdline(cmd[1:]).replace('\\', '\\\\')
    cmd_file = tempfile.NamedTemporaryFile(mode='w+',
                                           suffix='.args',
                                           delete=False)
    with cmd_file:
        cmd_file.write(cmd_str)
    cmd_file = cmd_file.name
    cmd = [cmd[0], file_flag + cmd_file]
    return cmd, cmd_file
def _exec_command_result(cmd, cwd, env, shell, stdin):
    try:
        if env:
            env = dict((cast_str(key), cast_str(value))
                       for key, value in env.items())
        p = subprocess.Popen(cmd, cwd=cwd, env=env,
                             shell=shell,
                             stdin=stdin, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=False)
        stdout, stderr = p.communicate()
        returncode = p.poll()
    except Exception as ex:
        raise ExecCommandException(cmd, exception=ex)
    stdout = _decode_data(stdout)
    stderr = _decode_data(stderr)
    return ExecCommandResult(cmd, status=returncode,
                             stdout=stdout, stderr=stderr)
def execute_command(cmd, cwd=None, env=None, stdin=None, file_flag=None):
    if is_string(cmd):
        shell = True
        cmd_file = None
    else:
        shell = False
        cmd, cmd_file = _gen_exec_cmd_file(cmd, file_flag)
    try:
        return _exec_command_result(cmd, cwd, env, shell, stdin)
    finally:
        if cmd_file:
            remove_files(cmd_file)
def get_shell_script_env(script, args=None, _var_re=re.compile(r'^\w+=')):
    args = to_sequence(args)
    script_path = os.path.abspath(
        os.path.expanduser(os.path.expandvars(script)))
    os_env = os.environ
    cwd, script = os.path.split(script_path)
    if os.name == "nt":
        cmd = ['call', script]
        cmd += args
        cmd += ['&&', 'set']
    else:
        cmd = ['.', './' + script]
        cmd += args
        cmd += ['&&', 'printenv']
        cmd = ' '.join(cmd)
    try:
        p = subprocess.Popen(cmd, cwd=cwd, shell=True, env=os_env,
                             stdin=None, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=False)
        stdout, stderr = p.communicate()
        status = p.poll()
    except Exception as ex:
        raise ExecCommandException(cmd, exception=ex)
    stdout = _decode_data(stdout)
    stderr = _decode_data(stderr)
    if status != 0:
        raise ExecCommandResult(cmd, status, stdout, stderr)
    script_env = {}
    for line in stdout.split('\n'):
        match = _var_re.match(line)
        if match:
            name, sep, value = line.partition('=')
            value = value.strip()
            current = os_env.get(name, None)
            if (current is None) or (value != current.strip()):
                script_env[name] = value
    return script_env
def cpu_count():
    try:
        return multiprocessing.cpu_count()
    except NotImplementedError:
        pass
    count = int(os.environ.get('NUMBER_OF_PROCESSORS', 0))
    if count > 0:
        return count
    try:
        if 'SC_NPROCESSORS_ONLN' in os.sysconf_names:
            count = os.sysconf('SC_NPROCESSORS_ONLN')
        elif 'SC_NPROCESSORS_CONF' in os.sysconf_names:
            count = os.sysconf('SC_NPROCESSORS_CONF')
        if count > 0:
            return cpu_count
    except AttributeError:
        pass
    count = 1  # unable to detect number of CPUs
    return count
def _memory_usage_smaps():
    private = 0
    with open("/proc/self/smaps") as smaps:
        for line in smaps:
            if line.startswith("Private"):
                private += int(line.split()[1])
    return private
def _memory_usage_statm():
    page_size = os.sysconf("SC_PAGE_SIZE")
    with open('/proc/self/statm') as f:
        mem_stat = f.readline().split()
        rss = int(mem_stat[1]) * page_size
        shared = int(mem_stat[2]) * page_size
        private = rss - shared
    return private // 1024
def memory_usage_linux():
    try:
        return _memory_usage_smaps()
    except IOError:
        try:
            return _memory_usage_statm()
        except IOError:
            return memory_usage_unix()
def memory_usage_unix():
    res = resource.getrusage(resource.RUSAGE_SELF)
    return res.ru_maxrss
def memory_usage_windows():
    process_handle = win32api.GetCurrentProcess()
    memory_info = win32process.GetProcessMemoryInfo(process_handle)
    return memory_info['PeakWorkingSetSize']
try:
    import resource
    if sys.platform[:5] == "linux":
        memory_usage = memory_usage_linux
    else:
        memory_usage = memory_usage_unix
except ImportError:
    try:
        import win32process
        import win32api
        memory_usage = memory_usage_windows
    except ImportError:
        def memory_usage():
            return 0
def load_module(module_file, package_name=None):
    module_dir, module_file = os.path.split(module_file)
    module_name = os.path.splitext(module_file)[0]
    if package_name:
        full_module_name = package_name + '.' + module_name
    else:
        full_module_name = module_name
    module = sys.modules.get(full_module_name)
    if module is not None:
        return module
    fp, pathname, description = imp.find_module(module_name, [module_dir])
    module = imp.load_module(full_module_name, fp, pathname, description)
    return module
def load_package(path, name=None, generate_name=False):
    find_path, find_name = os.path.split(path)
    if not name:
        if generate_name:
            name = new_hash(dump_simple_object(path)).hexdigest()
        else:
            name = find_name
    package = sys.modules.get(name)
    if package is not None:
        return package
    fp, pathname, description = imp.find_module(find_name, [find_path])
    package = imp.load_module(name, fp, pathname, description)
    return package
def flatten_list(seq):
    out_list = list(to_sequence(seq))
    i = 0
    while i < len(out_list):
        value = out_list[i]
        if is_sequence(value):
            if value:
                out_list[i: i + 1] = value
            else:
                del out_list[i]
            continue
        i += 1
    return out_list
_SIMPLE_SEQUENCES = (list, tuple, UniqueList, set, frozenset)
def simplify_value(value,                           # noqa  compexity > 9
                   simple_types=SIMPLE_TYPES_SET,
                   simple_lists=_SIMPLE_SEQUENCES):
    if value is None:
        return None
    value_type = type(value)
    if value_type in simple_types:
        return value
    for simple_type in simple_types:
        if isinstance(value, simple_type):
            return simple_type(value)
    if isinstance(value, simple_lists):
        return [simplify_value(v) for v in value]
    if isinstance(value, dict):
        return dict((key, simplify_value(v)) for key, v in value.items())
    try:
        return simplify_value(value.get())
    except Exception:
        trace_back = sys.exc_info()[2]
        if trace_back.tb_next is not None:
            raise
    return value
class Chrono (object):
    __slots__ = ('elapsed', )
    def __init__(self):
        self.elapsed = 0
    def __enter__(self):
        self.elapsed = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.elapsed
        return False
    def get(self):
        return self.elapsed
    def __str__(self):
        elapsed = self.elapsed
        minutes = int(elapsed / 60)
        seconds = int(elapsed - minutes * 60)
        milisecs = int((elapsed - int(elapsed)) * 1000)
        result = []
        if minutes:
            result.append("%s min" % minutes)
            milisecs = 0
        if seconds:
            result.append("%s sec" % seconds)
        if milisecs:
            result.append("%s ms" % milisecs)
        if not minutes and not seconds and not milisecs:
            result.append("0 ms")
        return ' '.join(result)
class ItemsGroups(object):
    __slots__ = (
        'wish_groups',
        'max_group_size',
        'group_size',
        'tail_size',
        'groups',
    )
    def __init__(self, size, wish_groups, max_group_size):
        wish_groups = max(1, wish_groups)
        group_size = size // wish_groups
        if max_group_size < 0:
            max_group_size = size
        elif max_group_size == 0:
            max_group_size = group_size + 1
        group_size = max(1, group_size)
        self.wish_groups = wish_groups
        self.group_size = min(max_group_size, group_size)
        self.max_group_size = max_group_size
        self.tail_size = size
        self.groups = [[]]
    def add_group(self):
        groups = self.groups
        if not groups[0]:
            return
        group_size = max(
            1, self.tail_size // max(1, self.wish_groups - len(self.groups)))
        self.group_size = min(self.max_group_size, group_size)
        group_files = []
        self.groups.append(group_files)
        return group_files
    def add(self, item):
        group_files = self.groups[-1]
        if len(group_files) >= self.group_size:
            group_files = self.add_group()
        group_files.append(item)
        self.tail_size -= 1
    def get(self):
        groups = self.groups
        if not groups[-1]:
            del groups[-1]
        return groups
def group_items(items, wish_groups=1, max_group_size=-1):
    groups = ItemsGroups(len(items), wish_groups, max_group_size)
    for item in items:
        groups.add(item)
    return groups.get()
class ErrorOptionValueMergeNonOptionValue(TypeError):
    def __init__(self, value):
        msg = "Unable to merge option value with non option value: '%s'" % (
            type(value),)
        super(ErrorOptionValueMergeNonOptionValue, self).__init__(msg)
class ErrorOptionValueOperationFailed(TypeError):
    def __init__(self, op, args, kw, err):
        args_str = ""
        if args:
            args_str += ', '.join(map(str, args))
        if kw:
            if args_str:
                args_str += ","
            args_str += str(kw)
        msg = "Operation %s( %s ) failed with error: %s" % (op, args_str, err)
        super(ErrorOptionValueOperationFailed, self).__init__(msg)
def _set_operator(dest_value, value):
    return value
def _op_iadd_key_operator(dest_value, key, value):
    dest_value[key] += value
    return dest_value
def _op_isub_key_operator(dest_value, key, value):
    dest_value[key] -= value
    return dest_value
def _update_operator(dest_value, value):
    if isinstance(dest_value, (UniqueList, list)):
        dest_value += value
        return dest_value
    elif isinstance(dest_value, Dict):
        dest_value.update(value)
        return dest_value
    else:
        return value
def op_set(value):
    return SimpleInplaceOperation(_set_operator, value)
def op_set_key(key, value):
    return SimpleInplaceOperation(operator.setitem, key, value)
def op_get_key(value, key):
    return SimpleOperation(operator.getitem, value, key)
def op_iadd(value):
    return SimpleInplaceOperation(operator.iadd, value)
def op_iadd_key(key, value):
    return SimpleInplaceOperation(_op_iadd_key_operator, key, value)
def op_isub_key(key, value):
    return SimpleInplaceOperation(_op_isub_key_operator, key, value)
def op_isub(value):
    return SimpleInplaceOperation(operator.isub, value)
def op_iupdate(value):
    return SimpleInplaceOperation(_update_operator, value)
def _convert_args(args, kw, options, converter):
    tmp_args = []
    for arg in args:
        if isinstance(arg, Operation):
            arg.convert(options, converter)
        else:
            arg = converter(options, arg)
        tmp_args.append(arg)
    tmp_kw = {}
    for key, arg in kw.items():
        if isinstance(arg, Operation):
            arg.convert(options, converter)
        elif converter is not None:
            arg = converter(options, arg)
        tmp_kw[key] = arg
    return tmp_args, tmp_kw
def _unconvert_args(args, kw, options, context, unconverter):
    tmp_args = []
    for arg in args:
        if isinstance(arg, Operation):
            arg = arg(options, context, unconverter)
        elif unconverter is not None:
            arg = unconverter(options, context, arg)
        tmp_args.append(arg)
    tmp_kw = {}
    for key, arg in kw.items():
        if isinstance(arg, Operation):
            arg = arg(options, context, unconverter)
        elif unconverter is not None:
            arg = unconverter(options, context, arg)
        tmp_kw[key] = arg
    return tmp_args, tmp_kw
class Condition(object):
    __slots__ = (
        'condition',
        'predicate',
        'args',
        'kw',
    )
    def __init__(self, condition, predicate, *args, **kw):
        self.condition = condition
        self.predicate = predicate
        self.args = args
        self.kw = kw
    def convert(self, options, converter):
        self.args, self.kw = _convert_args(
            self.args, self.kw, options, converter)
        cond = self.condition
        if cond is not None:
            cond.convert(options, converter)
    def __call__(self, options, context, unconverter):
        if self.condition is not None:
            if not self.condition(options, context, unconverter):
                return False
        args, kw = _unconvert_args(
            self.args, self.kw, options, context, unconverter)
        return self.predicate(options, context, *args, **kw)
class Operation(object):
    __slots__ = (
        'action',
        'kw',
        'args',
    )
    def __init__(self, action, *args, **kw):
        self.action = action
        self.args = args
        self.kw = kw
    def convert(self, options, converter):
        self.args, self.kw = _convert_args(
            self.args, self.kw, options, converter)
    def _call_action(self, options, context, args, kw):
        return self.action(options, context, *args, **kw)
    def __call__(self, options, context, unconverter):
        args, kw = _unconvert_args(
            self.args, self.kw, options, context, unconverter)
        try:
            result = self._call_action(options, context, args, kw)
        except Exception as ex:
            raise ErrorOptionValueOperationFailed(self.action, args, kw, ex)
        return result
    def __add__(self, other):
        return SimpleOperation(operator.add, self, other)
    def __radd__(self, other):
        return SimpleOperation(operator.add, other, self)
    def __sub__(self, other):
        return SimpleOperation(operator.sub, self, other)
    def __rsub__(self, other):
        return SimpleOperation(operator.sub, other, self)
class SimpleOperation(Operation):
    def _call_action(self, options, context, args, kw):
        return self.action(*args, **kw)
class InplaceOperation(object):
    __slots__ = (
        'action',
        'kw',
        'args',
    )
    def __init__(self, action, *args, **kw):
        self.action = action
        self.args = args
        self.kw = kw
    def convert(self, options, converter):
        self.args, self.kw = _convert_args(
            self.args, self.kw, options, converter)
    def _call_action(self, options, context, dest_value, args, kw):
        return self.action(options, context, dest_value, *args, **kw)
    def __call__(self, options, context, dest_value, value_type, unconverter):
        if self.action is None:
            return dest_value
        args, kw = _unconvert_args(
            self.args, self.kw, options, context, unconverter)
        try:
            result = self._call_action(options, context, dest_value, args, kw)
        except Exception as ex:
            raise ErrorOptionValueOperationFailed(self.action, args, kw, ex)
        if result is None:
            result = dest_value
        dest_value = value_type(result)
        return dest_value
class SimpleInplaceOperation(InplaceOperation):
    def _call_action(self, options, context, dest_value, args, kw):
        return self.action(dest_value, *args, **kw)
class ConditionalValue (object):
    __slots__ = (
        'ioperation',
        'condition',
    )
    def __init__(self, ioperation, condition=None):
        self.ioperation = ioperation
        self.condition = condition
    def convert(self, options, converter):
        condition = self.condition
        if isinstance(condition, Condition):
            condition.convert(options, converter)
        ioperation = self.ioperation
        if isinstance(ioperation, InplaceOperation):
            ioperation.convert(options, converter)
    def evaluate(self, value, value_type, options, context, unconverter):
        condition = self.condition
        if (condition is None) or condition(options, context, unconverter):
            if self.ioperation is not None:
                value = self.ioperation(
                    options, context, value, value_type, unconverter)
        return value
class OptionValue (object):
    __slots__ = (
        'option_type',
        'conditional_values',
    )
    def __init__(self, option_type, conditional_values=None):
        self.option_type = option_type
        self.conditional_values = list(to_sequence(conditional_values))
    def is_set(self):
        return bool(self.conditional_values)
    def is_tool_key(self):
        return self.option_type.is_tool_key
    def append_value(self, conditional_value):
        self.conditional_values.append(conditional_value)
    def prepend_value(self, conditional_value):
        self.conditional_values[:0] = [conditional_value]
    def merge(self, other):
        if self is other:
            return
        if not isinstance(other, OptionValue):
            raise ErrorOptionValueMergeNonOptionValue(other)
        values = self.conditional_values
        other_values = other.conditional_values
        diff_index = 0
        for value1, value2 in zip(values, other_values):
            if value1 is not value2:
                break
            diff_index += 1
        if self.option_type.is_auto and not other.option_type.is_auto:
            self.option_type = other.option_type
        self.conditional_values += other_values[diff_index:]
    def reset(self):
        self.conditional_values = []
    def copy(self):
        return OptionValue(self.option_type, self.conditional_values)
    def __copy__(self):
        return self.copy()
    def get(self, options, context, evaluator=None):
        if context is None:
            context = {}
        else:
            try:
                return context[self]
            except KeyError:
                pass
        value_type = self.option_type
        value = value_type()
        context[self] = value
        for conditional_value in self.conditional_values:
            value = conditional_value.evaluate(
                value, value_type, options, context, evaluator)
            context[self] = value
        return value
class ErrorDataFileFormatInvalid(Exception):
    def __init__(self):
        msg = "Data file format is not valid."
        super(ErrorDataFileFormatInvalid, self).__init__(msg)
class ErrorDataFileChunkInvalid(Exception):
    def __init__(self):
        msg = "Data file chunk format is not valid."
        super(ErrorDataFileChunkInvalid, self).__init__(msg)
class ErrorDataFileVersionInvalid(Exception):
    def __init__(self):
        msg = "Data file version is changed."
        super(ErrorDataFileVersionInvalid, self).__init__(msg)
class ErrorDataFileCorrupted(Exception):
    def __init__(self):
        msg = "Data file is corrupted"
        super(ErrorDataFileCorrupted, self).__init__(msg)
class _MmapFile(object):
    def __init__(self, filename):
        stream = open_file(filename, write=True, binary=True, sync=False)
        try:
            memmap = mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_WRITE)
        except Exception:
            stream.seek(0)
            stream.write(b'\0')
            stream.flush()
            memmap = mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_WRITE)
        self._check_resize_available(memmap)
        self.stream = stream
        self.memmap = memmap
        self.size = memmap.size
        self.resize = memmap.resize
        self.flush = memmap.flush
    @staticmethod
    def _check_resize_available(mem):
        size = mem.size()
        mem.resize(size + mmap.ALLOCATIONGRANULARITY)
        mem.resize(size)
    def close(self):
        self.memmap.flush()
        self.memmap.close()
        self.stream.close()
    def read(self, offset, size):
        return self.memmap[offset: offset + size]
    def write(self, offset, data):
        memmap = self.memmap
        end_offset = offset + len(data)
        if end_offset > memmap.size():
            page_size = mmap.ALLOCATIONGRANULARITY
            size = ((end_offset + (page_size - 1)) // page_size) * page_size
            if size == 0:
                size = page_size
            self.resize(size)
        memmap[offset: end_offset] = data
    def move(self, dest, src, size):
        memmap = self.memmap
        end_offset = dest + size
        if end_offset > memmap.size():
            self.resize(end_offset)
        memmap.move(dest, src, size)
class _IOFile(object):
    def __init__(self, filename):
        stream = open_file(filename, write=True, binary=True, sync=False)
        self.stream = stream
        self.resize = stream.truncate
        self.flush = stream.flush
    def close(self):
        self.stream.close()
    def read(self, offset, size):
        stream = self.stream
        stream.seek(offset)
        return stream.read(size)
    def write(self, offset, data):
        stream = self.stream
        stream.seek(offset)
        stream.write(data)
    def move(self, dest, src, size):
        stream = self.stream
        stream.seek(src)
        data = stream.read(size)
        stream.seek(dest)
        stream.write(data)
    def size(self, _end=os.SEEK_END):
        return self.stream.seek(0, _end)
class MetaData (object):
    __slots__ = (
        'offset',
        'key',
        'id',
        'data_offset',
        'data_size',
        'data_capacity',
    )
    _META_STRUCT = struct.Struct(">Q16sLL")
    size = _META_STRUCT.size
    def __init__(self, meta_offset, key, data_id, data_offset, data_size):
        self.offset = meta_offset
        self.key = key
        self.id = data_id
        self.data_offset = data_offset
        self.data_size = data_size
        self.data_capacity = data_size + 4
    def dump(self, meta_struct=_META_STRUCT):
        return meta_struct.pack(self.key, self.id,
                                self.data_size, self.data_capacity)
    @classmethod
    def load(cls, dump, meta_struct=_META_STRUCT):
        self = cls.__new__(cls)
        try:
            self.key, self.id, data_size, data_capacity = meta_struct.unpack(
                dump)
        except struct.error:
            raise ErrorDataFileChunkInvalid()
        if data_capacity < data_size:
            raise ErrorDataFileChunkInvalid()
        self.data_size = data_size
        self.data_capacity = data_capacity
        return self
    def resize(self, data_size):
        self.data_size = data_size
        capacity = self.data_capacity
        if capacity >= data_size:
            return 0
        self.data_capacity = data_size + min(data_size // 4, 128)
        return self.data_capacity - capacity
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        s = []
        for v in self.__slots__:
            s.append("%s: %s" % (v, getattr(self, v)))
        return ", ".join(s)
class DataFile (object):
    __slots__ = (
        'next_key',
        'id2data',
        'key2id',
        'meta_end',
        'data_begin',
        'data_end',
        'handle',
    )
    MAGIC_TAG = b".AQL.DB."
    VERSION = 1
    _HEADER_STRUCT = struct.Struct(">8sL")
    _HEADER_SIZE = _HEADER_STRUCT.size
    _KEY_STRUCT = struct.Struct(">Q")  # 8 bytes (next unique key)
    _KEY_OFFSET = _HEADER_SIZE
    _KEY_SIZE = _KEY_STRUCT.size
    _META_TABLE_HEADER_STRUCT = struct.Struct(">L")
    _META_TABLE_HEADER_SIZE = _META_TABLE_HEADER_STRUCT.size
    _META_TABLE_HEADER_OFFSET = _KEY_OFFSET + _KEY_SIZE
    _META_TABLE_OFFSET = _META_TABLE_HEADER_OFFSET + _META_TABLE_HEADER_SIZE
    def __init__(self, filename, force=False):
        self.id2data = {}
        self.key2id = {}
        self.meta_end = 0
        self.data_begin = 0
        self.data_end = 0
        self.handle = None
        self.next_key = None
        self.open(filename, force=force)
    def open(self, filename, force=False):
        self.close()
        try:
            self.handle = _MmapFile(filename)
        except Exception as ex:
            log_debug("mmap is not supported: %s", ex)
            self.handle = _IOFile(filename)
        self._init_header(force)
        self.next_key = self._key_generator()
        self._init_meta_table()
    def close(self):
        if self.handle is not None:
            self.handle.close()
            self.handle = None
            self.id2data.clear()
            self.key2id.clear()
            self.meta_end = 0
            self.data_begin = 0
            self.data_end = 0
            self.next_key = None
    def clear(self):
        self._reset_meta_table()
        self.next_key = self._key_generator()
        self.id2data.clear()
        self.key2id.clear()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    def _init_header(self, force, header_struct=_HEADER_STRUCT):
        header = self.handle.read(0, header_struct.size)
        try:
            tag, version = header_struct.unpack(header)
            if tag != self.MAGIC_TAG:
                if not force:
                    raise ErrorDataFileFormatInvalid()
            elif version == self.VERSION:
                return
        except struct.error:
            if (header and header != b'\0') and not force:
                raise ErrorDataFileFormatInvalid()
        header = header_struct.pack(self.MAGIC_TAG, self.VERSION)
        self.handle.resize(len(header))
        self.handle.write(0, header)
    def _key_generator(self,
                       key_offset=_KEY_OFFSET,
                       key_struct=_KEY_STRUCT,
                       max_key=(2 ** 64) - 1):
        key_dump = self.handle.read(key_offset, key_struct.size)
        try:
            next_key, = key_struct.unpack(key_dump)
        except struct.error:
            next_key = 0
        key_pack = key_struct.pack
        write_file = self.handle.write
        while True:
            if next_key < max_key:
                next_key += 1
            else:
                next_key = 1    # this should never happen
            write_file(key_offset, key_pack(next_key))
            yield next_key
    def _reset_meta_table(self,
                          meta_size=MetaData.size,
                          table_offset=_META_TABLE_OFFSET):
        self.meta_end = table_offset
        self.data_begin = table_offset + meta_size * 1024
        self.data_end = self.data_begin
        self._truncate_file()
    def _truncate_file(self,
                       table_header_struct=_META_TABLE_HEADER_STRUCT,
                       table_header_offset=_META_TABLE_HEADER_OFFSET):
        header_dump = table_header_struct.pack(self.data_begin)
        handle = self.handle
        handle.resize(self.data_end)
        handle.write(table_header_offset, header_dump)
        handle.write(self.meta_end, b'\0' * (self.data_begin - self.meta_end))
        handle.flush()
    def _init_meta_table(self,
                         table_header_struct=_META_TABLE_HEADER_STRUCT,
                         table_header_offset=_META_TABLE_HEADER_OFFSET,
                         table_header_size=_META_TABLE_HEADER_SIZE,
                         table_begin=_META_TABLE_OFFSET,
                         meta_size=MetaData.size):
        handle = self.handle
        header_dump = handle.read(table_header_offset, table_header_size)
        try:
            data_begin, = table_header_struct.unpack(header_dump)
        except struct.error:
            self._reset_meta_table()
            return
        if (data_begin <= table_begin) or (data_begin > handle.size()):
            self._reset_meta_table()
            return
        table_size = data_begin - table_begin
        if (table_size % meta_size) != 0:
            self._reset_meta_table()
            return
        dump = handle.read(table_begin, table_size)
        if len(dump) < table_size:
            self._reset_meta_table()
            return
        self._load_meta_table(data_begin, dump)
    def _load_meta_table(self, data_offset, metas_dump,
                         meta_size=MetaData.size,
                         table_begin=_META_TABLE_OFFSET):
        self.data_begin = data_offset
        file_size = self.handle.size()
        load_meta = MetaData.load
        pos = 0
        dump_size = len(metas_dump)
        while pos < dump_size:
            meta_dump = metas_dump[pos: pos + meta_size]
            try:
                meta = load_meta(meta_dump)
                data_capacity = meta.data_capacity
                if data_capacity == 0:
                    break
                meta.offset = pos + table_begin
                meta.data_offset = data_offset
                if (data_offset + meta.data_size) > file_size:
                    raise ErrorDataFileChunkInvalid()
                data_offset += data_capacity
            except Exception:
                self.data_end = data_offset
                self.meta_end = pos + table_begin
                self._truncate_file()
                return
            self.id2data[meta.id] = meta
            if meta.key:
                self.key2id[meta.key] = meta.id
            pos += meta_size
        self.meta_end = pos + table_begin
        self.data_end = data_offset
    def _extend_meta_table(self,
                           table_header_struct=_META_TABLE_HEADER_STRUCT,
                           table_header_offset=_META_TABLE_HEADER_OFFSET,
                           table_begin=_META_TABLE_OFFSET):
        data_begin = self.data_begin
        data_end = self.data_end
        table_capacity = data_begin - table_begin
        new_data_begin = data_begin + table_capacity
        handle = self.handle
        handle.move(new_data_begin, data_begin, data_end - data_begin)
        handle.write(data_begin, b'\0' * table_capacity)
        header_dump = table_header_struct.pack(new_data_begin)
        handle.write(table_header_offset, header_dump)
        self.data_begin = new_data_begin
        self.data_end += table_capacity
        for meta in self.id2data.values():
            meta.data_offset += table_capacity
    def _extend_data(self, meta, oversize):
        new_next_data = meta.data_offset + meta.data_capacity
        next_data = new_next_data - oversize
        rest_size = self.data_end - next_data
        if rest_size > 0:
            self.handle.move(new_next_data, next_data, rest_size)
            for meta in self.id2data.values():
                if meta.data_offset >= next_data:
                    meta.data_offset += oversize
        self.data_end += oversize
    def _append(self, key, data_id, data,
                meta_size=MetaData.size):
        meta_offset = self.meta_end
        if meta_offset == self.data_begin:
            self._extend_meta_table()
        data_offset = self.data_end
        meta = MetaData(meta_offset, key, data_id, data_offset, len(data))
        write = self.handle.write
        write(data_offset, data)
        write(meta_offset, meta.dump())
        self.data_end += meta.data_capacity
        self.meta_end += meta_size
        self.id2data[data_id] = meta
    def _update(self, meta, data, update_meta):
        data_size = len(data)
        if meta.data_size != data_size:
            update_meta = True
            oversize = meta.resize(data_size)
            if oversize > 0:
                self._extend_data(meta, oversize)
        write = self.handle.write
        if update_meta:
            write(meta.offset, meta.dump())
        write(meta.data_offset, data)
    def read(self, data_id):
        try:
            meta = self.id2data[data_id]
        except KeyError:
            return None
        return self.handle.read(meta.data_offset, meta.data_size)
    def write(self, data_id, data):
        try:
            meta = self.id2data[data_id]
            self._update(meta, data, update_meta=False)
        except KeyError:
            self._append(0, data_id, data)
    def write_with_key(self, data_id, data):
        meta = self.id2data.get(data_id)
        key = next(self.next_key)
        if meta is None:
            self._append(key, data_id, data)
        else:
            try:
                del self.key2id[meta.key]
            except KeyError:
                pass
            meta.key = key
            self._update(meta, data, update_meta=True)
        self.key2id[key] = data_id
        return key
    def get_ids(self, keys):
        try:
            return tuple(map(self.key2id.__getitem__, keys))
        except KeyError:
            return None
    def get_keys(self, data_ids):
        return map(operator.attrgetter('key'),
                   map(self.id2data.__getitem__, data_ids))
    def remove(self, data_ids):     # noqa  TODO: refactor to compexity < 10
        move = self.handle.move
        meta_size = MetaData.size
        remove_data_ids = frozenset(data_ids)
        metas = sorted(self.id2data.values(),
                       key=operator.attrgetter('data_offset'))
        meta_shift = 0
        data_shift = 0
        meta_offset = 0
        data_offset = 0
        last_meta_end = 0
        last_data_end = 0
        remove_data_begin = None
        remove_meta_begin = None
        move_meta_begin = None
        move_data_begin = None
        for meta in metas:
            meta_offset = meta.offset
            last_meta_end = meta_offset + meta_size
            data_offset = meta.data_offset
            last_data_end = data_offset + meta.data_size
            next_data_begin = data_offset + meta.data_capacity
            if meta.id in remove_data_ids:
                del self.id2data[meta.id]
                if meta.key:
                    del self.key2id[meta.key]
                if move_meta_begin is not None:
                    move(remove_meta_begin, move_meta_begin,
                         meta_offset - move_meta_begin)
                    move(remove_data_begin, move_data_begin,
                         data_offset - move_data_begin)
                    remove_meta_begin = None
                    move_meta_begin = None
                if remove_meta_begin is None:
                    remove_meta_begin = meta_offset - meta_shift
                    remove_data_begin = data_offset - data_shift
            else:
                if remove_meta_begin is not None:
                    if move_meta_begin is None:
                        move_meta_begin = meta_offset
                        move_data_begin = data_offset
                        meta_shift = move_meta_begin - remove_meta_begin
                        data_shift = move_data_begin - remove_data_begin
                if meta_shift:
                    meta.offset -= meta_shift
                    meta.data_offset -= data_shift
        if remove_data_begin is not None:
            if move_meta_begin is None:
                meta_shift = last_meta_end - remove_meta_begin
                data_shift = next_data_begin - remove_data_begin
            else:
                move(remove_meta_begin, move_meta_begin,
                     last_meta_end - move_meta_begin)
                move(remove_data_begin, move_data_begin,
                     last_data_end - move_data_begin)
        self.meta_end -= meta_shift
        self.data_end -= data_shift
        self.handle.write(self.meta_end, b'\0' * meta_shift)
        self.handle.resize(self.data_end)
    def self_test(self):    # noqa
        if self.handle is None:
            return
        file_size = self.handle.size()
        if self.data_begin > file_size:
            raise AssertionError("data_begin(%s) > file_size(%s)" %
                                 (self.data_begin, file_size))
        if self.data_begin > self.data_end:
            raise AssertionError("data_end(%s) > data_end(%s)" %
                                 (self.data_begin, self.data_end))
        if self.meta_end > self.data_begin:
            raise AssertionError("meta_end(%s) > data_begin(%s)" %
                                 (self.meta_end, self.data_begin))
        header_dump = self.handle.read(
            self._META_TABLE_HEADER_OFFSET, self._META_TABLE_HEADER_SIZE)
        try:
            data_begin, = self._META_TABLE_HEADER_STRUCT.unpack(header_dump)
        except struct.error:
            self._reset_meta_table()
            return
        if self.data_begin != data_begin:
            raise AssertionError("self.data_begin(%s) != data_begin(%s)" %
                                 (self.data_begin, data_begin))
        items = sorted(self.id2data.items(), key=lambda item: item[1].offset)
        last_meta_offset = self._META_TABLE_OFFSET
        last_data_offset = self.data_begin
        for data_id, meta in items:
            if meta.id != data_id:
                raise AssertionError(
                    "meta.id(%s) != data_id(%s)" % (meta.id, data_id))
            if meta.key != 0:
                if self.key2id[meta.key] != data_id:
                    raise AssertionError(
                        "self.key2id[ meta.key ](%s) != data_id(%s)" %
                        (self.key2id[meta.key], data_id))
            if meta.data_capacity < meta.data_size:
                raise AssertionError(
                    "meta.data_capacity(%s) < meta.data_size (%s)" %
                    (meta.data_capacity, meta.data_size))
            if meta.offset >= self.meta_end:
                raise AssertionError("meta.offset(%s) >= self.meta_end(%s)" %
                                     (meta.offset, self.meta_end))
            if meta.offset != last_meta_offset:
                raise AssertionError(
                    "meta.offset(%s) != last_meta_offset(%s)" %
                    (meta.offset, last_meta_offset))
            if meta.data_offset != last_data_offset:
                raise AssertionError(
                    "meta.data_offset(%s) != last_data_offset(%s)" %
                    (meta.data_offset, last_data_offset))
            if meta.data_offset >= self.data_end:
                raise AssertionError(
                    "meta.data_offset(%s) >= self.data_end(%s)" %
                    (meta.data_offset, self.data_end))
            if (meta.data_offset + meta.data_size) > file_size:
                raise AssertionError(
                    "(meta.data_offset + meta.data_size)(%s) > file_size(%s)" %
                    ((meta.data_offset + meta.data_size), file_size))
            last_data_offset += meta.data_capacity
            last_meta_offset += MetaData.size
        if last_meta_offset != self.meta_end:
            raise AssertionError("last_meta_offset(%s) != self.meta_end(%s)" %
                                 (last_meta_offset, self.meta_end))
        if last_data_offset != self.data_end:
            raise AssertionError("last_data_offset(%s) != self.data_end(%s)" %
                                 (last_data_offset, self.data_end))
        for key, data_id in self.key2id.items():
            if key != self.id2data[data_id].key:
                raise AssertionError(
                    "key(%s) != self.id2data[ data_id ].key(%s)" %
                    (key, self.id2data[data_id].key))
        for data_id, meta in self.id2data.items():
            meta_dump = self.handle.read(meta.offset, MetaData.size)
            stored_meta = MetaData.load(meta_dump)
            if meta.key != stored_meta.key:
                raise AssertionError("meta.key(%s) != stored_meta.key(%s)" %
                                     (meta.key, stored_meta.key))
            if meta.id != stored_meta.id:
                raise AssertionError("meta.id(%s) != stored_meta.id(%s)" %
                                     (meta.id, stored_meta.id))
            if meta.data_size != stored_meta.data_size:
                raise AssertionError(
                    "meta.data_size(%s) != stored_meta.data_size(%s)" %
                    (meta.data_size, stored_meta.data_size))
            if meta.data_capacity != stored_meta.data_capacity:
                raise AssertionError(
                    "meta.data_capacity(%s) != stored_meta.data_capacity(%s)" %
                    (meta.data_capacity, stored_meta.data_capacity))
class CLIOption(object):
    __slots__ = (
        'cli_name',
        'cli_long_name',
        'cli_only',
        'opt_name',
        'value_type',
        'default',
        'description',
        'metavar'
    )
    def __init__(self,
                 cli_name,
                 cli_long_name,
                 opt_name,
                 value_type,
                 default,
                 description,
                 metavar=None,
                 cli_only=False):
        self.cli_name = cli_name
        self.cli_long_name = cli_long_name
        self.cli_only = cli_only
        self.opt_name = opt_name
        self.value_type = value_type
        self.default = None if default is None else value_type(default)
        self.description = description
        self.metavar = metavar
    def add_to_parser(self, parser):
        args = []
        if self.cli_name is not None:
            args.append(self.cli_name)
        if self.cli_long_name is not None:
            args.append(self.cli_long_name)
        if self.value_type is bool:
            action = 'store_false' if self.default else 'store_true'
        elif issubclass(self.value_type, (list, UniqueList)):
            action = 'append'
        else:
            action = 'store'
        kw = {'dest': self.opt_name,
              'help': self.description, 'action': action}
        if self.metavar:
            kw['metavar'] = self.metavar
        parser.add_argument(*args, **kw)
class CLIConfig(object):
    def __init__(self, cli_options, args=None):
        super(CLIConfig, self).__setattr__('targets', tuple())
        super(CLIConfig, self).__setattr__('_set_options', set())
        super(CLIConfig, self).__setattr__('_defaults', {})
        self.__parse_arguments(cli_options, args)
    @staticmethod
    def __get_args_parser(cli_options):
        parser = argparse.ArgumentParser()
        for opt in cli_options:
            opt.add_to_parser(parser)
        return parser
    def __set_defaults(self, cli_options):
        defaults = self._defaults
        for opt in cli_options:
            defaults[opt.opt_name] = (opt.default, opt.value_type)
        targets_type = split_list_type(value_list_type(UniqueList, str), ', ')
        defaults['targets'] = (tuple(), targets_type)
        return defaults
    def __parse_values(self, args):
        targets = []
        for arg in args:
            name, sep, value = arg.partition('=')
            name = name.strip()
            if sep:
                setattr(self, name, value.strip())
            else:
                targets.append(name)
        if targets:
            self.targets = tuple(targets)
    def __parse_options(self, cli_options, args):
        defaults = self.__set_defaults(cli_options)
        for opt in cli_options:
            name = opt.opt_name
            value = getattr(args, name)
            default, value_type = defaults[name]
            if value is None:
                value = default
            else:
                self._set_options.add(name)
                value = value_type(value)
            super(CLIConfig, self).__setattr__(name, value)
    def __parse_arguments(self, cli_options, cli_args):
        parser = self.__get_args_parser(cli_options)
        parser.add_argument('targets_or_options',
                            metavar='TARGET | OPTION=VALUE',
                            nargs='*', help="Targets or option's values")
        args = parser.parse_args(cli_args)
        self.__parse_options(cli_options, args)
        self.__parse_values(args.targets_or_options)
    def read_file(self, config_file, config_locals=None):
        if config_locals is None:
            config_locals = {}
        exec_locals = exec_file(config_file, config_locals)
        for name, value in exec_locals.items():
            self.set_default(name, value)
    def __set(self, name, value):
        defaults = self._defaults
        try:
            default_value, value_type = defaults[name]
        except KeyError:
            if value is not None:
                defaults[name] = (value, type(value))
        else:
            if value is None:
                value = default_value
            elif type(value) is not value_type:
                value = value_type(value)
        super(CLIConfig, self).__setattr__(name, value)
    def set_default(self, name, value):
        if name.startswith("_"):
            super(CLIConfig, self).__setattr__(name, value)
        else:
            if name not in self._set_options:
                self.__set(name, value)
    def __setattr__(self, name, value):
        if name.startswith("_"):
            super(CLIConfig, self).__setattr__(name, value)
        else:
            self.__set(name, value)
            if value is None:
                self._set_options.discard(name)
            else:
                self._set_options.add(name)
    def items(self):
        for name, value in self.__dict__.items():
            if not name.startswith("_") and (name != "targets"):
                yield (name, value)
EVENT_ERROR,     EVENT_WARNING,     EVENT_STATUS,     EVENT_DEBUG,     = EVENT_ALL = tuple(range(4))
class ErrorEventUserHandlerWrongArgs (Exception):
    def __init__(self, event, handler):
        msg = "Invalid arguments of event '%s' handler method: '%s'" % (
            event, handler)
        super(ErrorEventUserHandlerWrongArgs, self).__init__(msg)
class ErrorEventHandlerAlreadyDefined (Exception):
    def __init__(self, event, handler, other_handler):
        msg = "Default event '%s' handler is defined twice: '%s', '%s'" %               (event, handler, other_handler)
        super(ErrorEventHandlerAlreadyDefined, self).__init__(msg)
class ErrorEventHandlerUnknownEvent (Exception):
    def __init__(self, event):
        msg = "Unknown event: '%s'" % (event,)
        super(ErrorEventHandlerUnknownEvent, self).__init__(msg)
class EventSettings(object):
    __slots__ = (
        'brief',
        'with_output',
        'trace_exec'
    )
    def __init__(self, brief=True, with_output=True, trace_exec=False):
        self.brief = brief
        self.with_output = with_output
        self.trace_exec = trace_exec
class EventManager(object):
    __slots__ = (
        'default_handlers',
        'user_handlers',
        'ignored_events',
        'disable_defaults',
        'settings',
    )
    def __init__(self):
        self.default_handlers = {}
        self.user_handlers = {}
        self.ignored_events = set()
        self.disable_defaults = False
        self.settings = EventSettings()
    def add_default_handler(self, handler, importance_level, event=None):
        if not event:
            event = handler.__name__
        pair = (handler, importance_level)
        other = self.default_handlers.setdefault(event, pair)
        if other != pair:
            raise ErrorEventHandlerAlreadyDefined(event, other[0], handler)
    def add_user_handler(self, user_handler, event=None):
        if not event:
            event = user_handler.__name__
        try:
            default_handler = self.default_handlers[event][0]
        except KeyError:
            raise ErrorEventHandlerUnknownEvent(event)
        if not equal_function_args(default_handler, user_handler):
            raise ErrorEventUserHandlerWrongArgs(event, user_handler)
        self.user_handlers.setdefault(event, []).append(user_handler)
    def remove_user_handler(self, user_handlers):
        user_handlers = to_sequence(user_handlers)
        for handlers in self.user_handlers.values():
            for user_handler in user_handlers:
                try:
                    handlers.remove(user_handler)
                except ValueError:
                    pass
    def send_event(self, event, *args, **kw):
        if event in self.ignored_events:
            return
        if self.disable_defaults:
            default_handlers = []
        else:
            default_handlers = [self.default_handlers[event][0]]
        user_handlers = self.user_handlers.get(event, [])
        args = (self.settings,) + args
        for handler in itertools.chain(user_handlers, default_handlers):
            handler(*args, **kw)
    def __get_events(self, event_filters):
        events = set()
        for event_filter in to_sequence(event_filters):
            if event_filter not in EVENT_ALL:
                events.add(event_filter)
            else:
                for event, pair in self.default_handlers.items():
                    level = pair[1]
                    if event_filter == level:
                        events.add(event)
        return events
    def enable_events(self, event_filters, enable):
        events = self.__get_events(event_filters)
        if enable:
            self.ignored_events.difference_update(events)
        else:
            self.ignored_events.update(events)
    def enable_default_handlers(self, enable):
        self.disable_defaults = not enable
    def set_settings(self, settings):
        self.settings = settings
_event_manager = EventManager()
def _event_impl(handler, importance_level, event=None):
    if not event:
        event = handler.__name__
    _event_manager.add_default_handler(handler, importance_level)
    def _send_event(*args, **kw):
        _event_manager.send_event(event, *args, **kw)
    return _send_event
def event_error(handler):
    return _event_impl(handler, EVENT_ERROR)
def event_warning(handler):
    return _event_impl(handler, EVENT_WARNING)
def event_status(handler):
    return _event_impl(handler, EVENT_STATUS)
def event_debug(handler):
    return _event_impl(handler, EVENT_DEBUG)
def event_handler(event=None):
    if isinstance(event, (types.FunctionType, types.MethodType)):
        _event_manager.add_user_handler(event)
        return event
    def _event_handler_impl(handler):
        _event_manager.add_user_handler(handler, event)
        return handler
    return _event_handler_impl
def set_event_settings(settings):
    _event_manager.set_settings(settings)
def enable_events(event_filters):
    _event_manager.enable_events(event_filters, True)
def disable_events(event_filters):
    _event_manager.enable_events(event_filters, False)
def disable_default_handlers():
    _event_manager.enable_default_handlers(False)
def enable_default_handlers():
    _event_manager.enable_default_handlers(True)
def add_user_handler(handler, event=None):
    _event_manager.add_user_handler(handler, event)
def remove_user_handler(handler):
    _event_manager.remove_user_handler(handler)
try:
    filterfalse = itertools.filterfalse
except AttributeError:
    filterfalse = itertools.ifilterfalse
class ErrorNoPrograms(Exception):
    def __init__(self, prog):
        msg = "No programs were specified: %s(%s)" % (prog, type(prog))
        super(ErrorNoPrograms, self).__init__(msg)
def abs_file_path(file_path, path_sep=os.path.sep,
                  seps=(os.path.sep, os.path.altsep),
                  _abspath=os.path.abspath,
                  _normcase=os.path.normcase):
    if not file_path:
        file_path = '.'
    if file_path[-1] in seps:
        last_sep = path_sep
    else:
        last_sep = ''
    return _normcase(_abspath(file_path)) + last_sep
def expand_file_path(path,
                     _normpath=os.path.normpath,
                     _expanduser=os.path.expanduser,
                     _expandvars=os.path.expandvars):
    return _normpath(_expanduser(_expandvars(path)))
def exclude_files_from_dirs(files, dirs):
    result = []
    folders = tuple(os.path.normcase(
        os.path.abspath(folder)) + os.path.sep for folder in to_sequence(dirs))
    for filename in to_sequence(files):
        filename = os.path.normcase(os.path.abspath(filename))
        if not filename.startswith(folders):
            result.append(filename)
    return result
def _masks_to_match(masks, _null_match=lambda name: False):
    if not masks:
        return _null_match
    if is_string(masks):
        masks = masks.split('|')
    re_list = []
    for mask in to_sequence(masks):
        mask = os.path.normcase(mask).strip()
        re_list.append("(%s)" % fnmatch.translate(mask))
    re_str = '|'.join(re_list)
    return re.compile(re_str).match
def find_files(paths=".",
               mask=("*",),
               exclude_mask=('.*',),
               exclude_subdir_mask=('__*', '.*'),
               found_dirs=None):
    found_files = []
    paths = to_sequence(paths)
    match_mask = _masks_to_match(mask)
    match_exclude_mask = _masks_to_match(exclude_mask)
    match_exclude_subdir_mask = _masks_to_match(exclude_subdir_mask)
    path_join = os.path.join
    for path in paths:
        for root, folders, files in os.walk(os.path.abspath(path)):
            for file_name in files:
                file_name_nocase = os.path.normcase(file_name)
                if (not match_exclude_mask(file_name_nocase)) and                   match_mask(file_name_nocase):
                    found_files.append(path_join(root, file_name))
            folders[:] = filterfalse(match_exclude_subdir_mask, folders)
            if found_dirs is not None:
                found_dirs.update(path_join(root, folder)
                                  for folder in folders)
    found_files.sort()
    return found_files
def find_file_in_paths(paths, filename):
    for path in paths:
        file_path = os.path.join(path, filename)
        if os.access(file_path, os.R_OK):
            return os.path.normpath(file_path)
    return None
def _get_env_path(env, hint_prog=None):
    paths = env.get('PATH', tuple())
    if is_string(paths):
        paths = paths.split(os.pathsep)
    paths = [os.path.expanduser(path) for path in paths]
    if hint_prog:
        hint_dir = os.path.dirname(hint_prog)
        paths.insert(0, hint_dir)
    return paths
def _get_env_path_ext(env, hint_prog=None,
                      is_windows=(os.name == 'nt'),
                      is_cygwin=(sys.platform == 'cygwin')):
    if not is_windows and not is_cygwin:
        return tuple()
    if hint_prog:
        hint_ext = os.path.splitext(hint_prog)[1]
        return hint_ext,
    path_exts = env.get('PATHEXT')
    if path_exts is None:
        path_exts = os.environ.get('PATHEXT')
    if is_string(path_exts):
        path_sep = ';' if is_cygwin else os.pathsep
        path_exts = path_exts.split(path_sep)
    if not path_exts:
        path_exts = ['.exe', '.cmd', '.bat', '.com']
    if is_cygwin:
        if '' not in path_exts:
            path_exts = [''] + path_exts
    return path_exts
def _add_program_exts(progs, exts):
    progs = to_sequence(progs)
    if not exts:
        return tuple(progs)
    result = []
    for prog in progs:
        prog_ext = os.path.splitext(prog)[1]
        if prog_ext or (prog_ext in exts):
            result.append(prog)
        else:
            result += (prog + ext for ext in exts)
    return result
def _find_program(progs, paths):
    for path in paths:
        for prog in progs:
            prog_path = os.path.join(path, prog)
            if os.access(prog_path, os.X_OK):
                return os.path.normcase(prog_path)
    return None
def find_program(prog, env, hint_prog=None):
    paths = _get_env_path(env, hint_prog)
    path_ext = _get_env_path_ext(env, hint_prog)
    progs = _add_program_exts(prog, path_ext)
    return _find_program(progs, paths)
def find_programs(progs, env, hint_prog=None):
    paths = _get_env_path(env, hint_prog)
    path_ext = _get_env_path_ext(env, hint_prog)
    result = []
    for prog in progs:
        progs = _add_program_exts(prog, path_ext)
        prog = _find_program(progs, paths)
        result.append(prog)
    return result
def find_optional_program(prog, env, hint_prog=None):
    paths = _get_env_path(env, hint_prog)
    path_ext = _get_env_path_ext(env, hint_prog)
    progs = _add_program_exts(prog, path_ext)
    return _OptionalProgramFinder(progs, paths)
def find_optional_programs(progs, env, hint_prog=None):
    paths = _get_env_path(env, hint_prog)
    path_ext = _get_env_path_ext(env, hint_prog)
    result = []
    for prog in progs:
        progs = _add_program_exts(prog, path_ext)
        prog = _OptionalProgramFinder(progs, paths)
        result.append(prog)
    return result
class _OptionalProgramFinder(object):
    __slots__ = (
        'progs',
        'paths',
        'result',
    )
    def __init__(self, progs, paths):
        if not progs:
            raise ErrorNoPrograms(progs)
        self.progs = progs
        self.paths = paths
        self.result = None
    def __nonzero__(self):
        return bool(self.get())
    def __bool__(self):
        return bool(self.get())
    def __call__(self):
        return self.get()
    def __str__(self):
        return self.get()
    def get(self):
        progpath = self.result
        if progpath:
            return progpath
        prog_full_path = _find_program(self.progs, self.paths)
        if prog_full_path is not None:
            self.result = prog_full_path
            return prog_full_path
        self.result = self.progs[0]
        return self.result
def _norm_local_path(path):
    if not path:
        return '.'
    path_sep = os.path.sep
    if path[-1] in (path_sep, os.path.altsep):
        last_sep = path_sep
    else:
        last_sep = ''
    path = os.path.normcase(os.path.normpath(path))
    return path + last_sep
try:
    _splitunc = os.path.splitunc
except AttributeError:
    def _splitunc(path):
        return str(), path
def split_drive(path):
    drive, path = os.path.splitdrive(path)
    if not drive:
        drive, path = _splitunc(path)
    return drive, path
def _split_path(path):
    drive, path = split_drive(path)
    path = path.split(os.path.sep)
    path.insert(0, drive)
    return path
def split_path(path):
    path = os.path.normcase(os.path.normpath(path))
    path = _split_path(path)
    path = [p for p in path if p]
    return path
def _common_prefix_size(*paths):
    min_path = min(paths)
    max_path = max(paths)
    i = 0
    for i, path in enumerate(min_path[:-1]):
        if path != max_path[i]:
            return i
    return i + 1
def _relative_join(base_path, base_path_seq, path, sep=os.path.sep):
    path = _split_path(_norm_local_path(path))
    prefix_index = _common_prefix_size(base_path_seq, path)
    if prefix_index == 0:
        drive = path[0]
        if drive:
            drive = drive.replace(':', '').split(sep)
            del path[0]
            path[0:0] = drive
    else:
        path = path[prefix_index:]
    path.insert(0, base_path)
    path = filter(None, path)
    return sep.join(path)
def relative_join_list(base_path, paths):
    base_path = _norm_local_path(base_path)
    base_path_seq = _split_path(base_path)
    return [_relative_join(base_path, base_path_seq, path)
            for path in to_sequence(paths)]
def relative_join(base_path, path):
    base_path = _norm_local_path(base_path)
    base_path_seq = _split_path(base_path)
    return _relative_join(base_path, base_path_seq, path)
def change_path(path, dirname=None, name=None, ext=None, prefix=None):
    path_dirname, path_filename = os.path.split(path)
    path_name, path_ext = os.path.splitext(path_filename)
    if dirname is None:
        dirname = path_dirname
    if name is None:
        name = path_name
    if ext is None:
        ext = path_ext
    if prefix:
        name = prefix + name
    path = dirname
    if path:
        path += os.path.sep
    return path + name + ext
def _simple_path_getter(path):
    return path
def group_paths_by_dir(file_paths,
                       wish_groups=1,
                       max_group_size=-1,
                       path_getter=None):
    groups = ItemsGroups(len(file_paths), wish_groups, max_group_size)
    if path_getter is None:
        path_getter = _simple_path_getter
    files = []
    for file_path in file_paths:
        path = path_getter(file_path)
        dir_path, file_name = os.path.split(path)
        dir_path = os.path.normcase(dir_path)
        files.append((dir_path, file_path))
    files.sort(key=operator.itemgetter(0))
    last_dir = None
    for dir_path, file_path in files:
        if last_dir != dir_path:
            last_dir = dir_path
            groups.add_group()
        groups.add(file_path)
    return groups.get()
class Chdir (object):
    __slots__ = ('previous_path', )
    def __init__(self, path):
        self.previous_path = os.getcwd()
        os.chdir(path)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.previous_path)
        return False
class ErrorDataFileFormatInvalid(Exception):
    def __init__(self, filename):
        msg = "Invalid format of data file: %s" % (filename,)
        super(ErrorDataFileFormatInvalid, self).__init__(msg)
class ErrorDataFileCorrupted(Exception):
    def __init__(self, filename):
        msg = "Corrupted format of data file: %s" % (filename,)
        super(ErrorDataFileCorrupted, self).__init__(msg)
def _bytes_to_blob_stub(value):
    return value
def _many_bytes_to_blob_stub(values):
    return values
def _blob_to_bytes_stub(value):
    return value
def _bytes_to_blob_buf(value):
    return buffer(value)        # noqa
def _many_bytes_to_blob_buf(values):
    return map(buffer, values)  # noqa
def _blob_to_bytes_buf(value):
    return bytes(value)
try:
    buffer
except NameError:
    _bytes_to_blob = _bytes_to_blob_stub
    _many_bytes_to_blob = _many_bytes_to_blob_stub
    _blob_to_bytes = _blob_to_bytes_stub
else:
    _bytes_to_blob = _bytes_to_blob_buf
    _many_bytes_to_blob = _many_bytes_to_blob_buf
    _blob_to_bytes = _blob_to_bytes_buf
class SqlDataFile (object):
    __slots__ = (
        'id2key',
        'key2id',
        'connection',
    )
    def __init__(self, filename, force=False):
        self.id2key = {}
        self.key2id = {}
        self.connection = None
        self.open(filename, force=force)
    def clear(self):
        with self.connection as conn:
            conn.execute("DELETE FROM items")
        self.id2key.clear()
        self.key2id.clear()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    def _load_ids(self, conn, blob_to_bytes=_blob_to_bytes):
        set_key = self.key2id.__setitem__
        set_id = self.id2key.__setitem__
        for key, data_id in conn.execute("SELECT key,id FROM items"):
            data_id = blob_to_bytes(data_id)
            set_key(key, data_id)
            set_id(data_id, key)
    def open(self, filename, force=False):
        self.close()
        try:
            conn = self._open_connection(filename)
        except ErrorDataFileCorrupted:
            os.remove(filename)
            conn = self._open_connection(filename)
        except ErrorDataFileFormatInvalid:
            if not force and not self._is_aql_db(filename):
                raise
            os.remove(filename)
            conn = self._open_connection(filename)
        self._load_ids(conn)
        self.connection = conn
    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        self.id2key.clear()
        self.key2id.clear()
    @staticmethod
    def _is_aql_db(filename):
        magic_tag = b".AQL.DB."
        with open_file(filename, read=True, binary=True) as f:
            tag = f.read(len(magic_tag))
            return tag == magic_tag
    @staticmethod
    def _open_connection(filename):
        conn = None
        try:
            conn = sqlite3.connect(filename,
                                   detect_types=sqlite3.PARSE_DECLTYPES)
            with conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS items("
                    "key INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "id BLOB UNIQUE,"
                    "data BLOB NOT NULL"
                    ")")
        except (sqlite3.DataError, sqlite3.IntegrityError):
            if conn is not None:
                conn.close()
            raise ErrorDataFileCorrupted(filename)
        except sqlite3.DatabaseError:
            if conn is not None:
                conn.close()
            raise ErrorDataFileFormatInvalid(filename)
        conn.execute("PRAGMA synchronous=OFF")
        return conn
    def read(self, data_id,
             bytes_to_blob=_bytes_to_blob,
             blob_to_bytes=_blob_to_bytes):
        result = self.connection.execute("SELECT data FROM items where id=?",
                                         (bytes_to_blob(data_id),))
        data = result.fetchone()
        if not data:
            return None
        return blob_to_bytes(data[0])
    def write_with_key(self, data_id, data,
                       bytes_to_blob=_bytes_to_blob):
        key = self.id2key.pop(data_id, None)
        if key is not None:
            del self.key2id[key]
        with self.connection as conn:
            cur = conn.execute(
                "INSERT OR REPLACE INTO items(id, data) VALUES (?,?)",
                (bytes_to_blob(data_id), bytes_to_blob(data)))
        key = cur.lastrowid
        self.key2id[key] = data_id
        self.id2key[data_id] = key
        return key
    write = write_with_key
    def get_ids(self, keys):
        try:
            return tuple(map(self.key2id.__getitem__, keys))
        except KeyError:
            return None
    def get_keys(self, data_ids):
        return map(self.id2key.__getitem__, data_ids)
    def remove(self, data_ids, many_bytes_to_blob=_many_bytes_to_blob):
        with self.connection as conn:
            conn.executemany("DELETE FROM items WHERE id=?",
                             zip(many_bytes_to_blob(data_ids)))
        get_key = self.id2key.__getitem__
        del_key = self.key2id.__delitem__
        del_id = self.id2key.__delitem__
        for data_id in data_ids:
            key = get_key(data_id)
            del_key(key)
            del_id(data_id)
    def self_test(self, blob_to_bytes=_blob_to_bytes):  # noqa
        if self.connection is None:
            if self.id2key:
                raise AssertionError("id2key is not empty")
            if self.key2id:
                raise AssertionError("key2id is not empty")
            return
        key2id = self.key2id.copy()
        id2key = self.id2key.copy()
        items = self.connection.execute("SELECT key,id FROM items")
        for key, data_id in items:
            data_id = blob_to_bytes(data_id)
            d = key2id.pop(key, None)
            if d is None:
                raise AssertionError("key(%s) not in key2id" % (key,))
            if d != data_id:
                raise AssertionError("data_id(%s) != d(%s)" %
                                     (binascii.hexlify(data_id),
                                      binascii.hexlify(d)))
            k = id2key.pop(data_id, None)
            if k is None:
                raise AssertionError("data_id(%s) not in id2key" %
                                     (binascii.hexlify(data_id),))
            if k != key:
                raise AssertionError("key(%s) != k(%s)" % (key, k))
        if key2id:
            raise AssertionError("unknown keys: %s" % (key2id,))
        if id2key:
            raise AssertionError("unknown data_ids: %s" % (id2key,))
class Tool(object):
    def __init__(self, options):
        pass
    @classmethod
    def setup(cls, options):
        pass
    @classmethod
    def options(cls):
        return None
    @classmethod
    def find_program(cls, options, prog, hint_prog=None):
        env = options.env.get()
        prog = find_program(prog, env, hint_prog)
        if prog is None:
            raise NotImplementedError()
        return prog
    @classmethod
    def find_programs(cls, options, progs, hint_prog=None):
        env = options.env.get()
        progs = find_programs(progs, env, hint_prog)
        for prog in progs:
            if prog is None:
                raise NotImplementedError()
        return progs
    @classmethod
    def find_optional_program(cls, options, prog, hint_prog=None):
        env = options.env.get()
        return find_optional_program(prog, env, hint_prog)
    @classmethod
    def find_optional_programs(cls, options, progs, hint_prog=None):
        env = options.env.get()
        return find_optional_programs(progs, env, hint_prog)
class ErrorOptionsCyclicallyDependent(TypeError):
    def __init__(self):
        msg = "Options cyclically depend from each other."
        super(ErrorOptionsCyclicallyDependent, self).__init__(msg)
class ErrorOptionsMergeNonOptions(TypeError):
    def __init__(self, value):
        msg = "Type '%s' can't be merged with Options." % (type(value),)
        super(ErrorOptionsMergeNonOptions, self).__init__(msg)
class ErrorOptionsMergeDifferentOptions(TypeError):
    def __init__(self, name1, name2):
        msg = "Can't merge one an optional value into two different options "               "'%s' and '%s' " % (name1, name2)
        super(ErrorOptionsMergeDifferentOptions, self).__init__(msg)
class ErrorOptionsMergeChild(TypeError):
    def __init__(self):
        msg = "Can't merge child options into the parent options. "               "Use join() to move child options into its parent."
        super(ErrorOptionsMergeChild, self).__init__(msg)
class ErrorOptionsJoinNoParent(TypeError):
    def __init__(self, options):
        msg = "Can't join options without parent: %s" % (options, )
        super(ErrorOptionsJoinNoParent, self).__init__(msg)
class ErrorOptionsJoinParent(TypeError):
    def __init__(self, options):
        msg = "Can't join options with children: %s" % (options, )
        super(ErrorOptionsJoinParent, self).__init__(msg)
class ErrorOptionsNoIteration(TypeError):
    def __init__(self):
        msg = "Options doesn't support iteration"
        super(ErrorOptionsNoIteration, self).__init__(msg)
class ErrorOptionsUnableEvaluate(TypeError):
    def __init__(self, name, err):
        msg = "Unable to evaluate option '%s', error: %s" % (name, err)
        super(ErrorOptionsUnableEvaluate, self).__init__(msg)
class _OpValueRef(tuple):
    def __new__(cls, value):
        return super(_OpValueRef, cls).__new__(cls, (value.name, value.key))
    def get(self, options, context):
        name, key = self
        value = getattr(options, name).get(context)
        if key is not NotImplemented:
            value = value[key]
        return value
class _OpValueExRef(tuple):
    def __new__(cls, value):
        return super(_OpValueExRef, cls).__new__(cls, (value.name,
                                                       value.key,
                                                       value.options))
    def get(self):
        name, key, options = self
        value = getattr(options, name).get()
        if key is not NotImplemented:
            value = value[key]
        return value
def _store_op_value(options, value):
    if isinstance(value, OptionValueProxy):
        value_options = value.options
        if (options is value_options) or options._is_parent(value_options):
            value = _OpValueRef(value)
        else:
            value_options._add_dependency(options)
            value = _OpValueExRef(value)
    elif isinstance(value, dict):
        value = dict((k, _store_op_value(options, v))
                     for k, v in value.items())
    elif isinstance(value, (list, tuple, UniqueList, set, frozenset)):
        value = [_store_op_value(options, v) for v in value]
    return value
def _load_op_value(options, context, value):
    if isinstance(value, _OpValueRef):
        value = value.get(options, context)
        value = simplify_value(value)
    elif isinstance(value, _OpValueExRef):
        value = value.get()
        value = simplify_value(value)
    elif isinstance(value, dict):
        value = dict((k, _load_op_value(options, context, v))
                     for k, v in value.items())
    elif isinstance(value, (list, tuple, UniqueList, set, frozenset)):
        value = [_load_op_value(options, context, v) for v in value]
    else:
        value = simplify_value(value)
    return value
def _eval_cmp_value(value):
    if isinstance(value, OptionValueProxy):
        value = value.get()
    value = simplify_value(value)
    return value
class OptionValueProxy (object):
    def __init__(self,
                 option_value,
                 from_parent,
                 name,
                 options,
                 key=NotImplemented):
        self.option_value = option_value
        self.from_parent = from_parent
        self.name = name
        self.options = options
        self.key = key
        self.child_ref = None
    def is_set(self):
        return self.option_value.is_set()
    def is_set_not_to(self, value):
        return self.option_value.is_set() and (self != value)
    def get(self, context=None):
        self.child_ref = None
        v = self.options.evaluate(self.option_value, context, self.name)
        return v if self.key is NotImplemented else v[self.key]
    def __iadd__(self, other):
        self.child_ref = None
        if self.key is not NotImplemented:
            other = op_iadd_key(self.key, other)
        self.options._append_value(
            self.option_value, self.from_parent, other, op_iadd)
        return self
    def __add__(self, other):
        return SimpleOperation(operator.add, self, other)
    def __radd__(self, other):
        return SimpleOperation(operator.add, other, self)
    def __sub__(self, other):
        return SimpleOperation(operator.sub, self, other)
    def __rsub__(self, other):
        return SimpleOperation(operator.sub, other, self)
    def __isub__(self, other):
        self.child_ref = None
        if self.key is not NotImplemented:
            other = op_isub_key(self.key, other)
        self.options._append_value(
            self.option_value, self.from_parent, other, op_isub)
        return self
    def set(self, value):
        self.child_ref = None
        if self.key is not NotImplemented:
            value = op_set_key(self.key, value)
        self.options._append_value(
            self.option_value, self.from_parent, value, op_set)
    def __setitem__(self, key, value):
        child_ref = self.child_ref
        if (child_ref is not None) and (child_ref() is value):
            return
        if self.key is not NotImplemented:
            raise KeyError(key)
        option_type = self.option_value.option_type
        if isinstance(option_type, DictOptionType):
            if isinstance(value, OptionType) or (type(value) is type):
                option_type.set_value_type(key, value)
                return
        value = op_set_key(key, value)
        self.child_ref = None
        self.options._append_value(
            self.option_value, self.from_parent, value, op_set)
    def __getitem__(self, key):
        if self.key is not NotImplemented:
            raise KeyError(key)
        child = OptionValueProxy(
            self.option_value, self.from_parent, self.name, self.options, key)
        self.child_ref = weakref.ref(child)
        return child
    def update(self, value):
        self.child_ref = None
        self.options._append_value(
            self.option_value, self.from_parent, value, op_iupdate)
    def __iter__(self):
        raise TypeError()
    def __bool__(self):
        return bool(self.get(context=None))
    def __nonzero__(self):
        return bool(self.get(context=None))
    def __str__(self):
        return str(self.get(context=None))
    def is_true(self, context):
        return bool(self.get(context))
    def is_false(self, context):
        return not bool(self.get(context))
    def eq(self, context, other):
        return self.cmp(context, operator.eq, other)
    def ne(self, context, other):
        return self.cmp(context, operator.ne, other)
    def lt(self, context, other):
        return self.cmp(context, operator.lt, other)
    def le(self, context, other):
        return self.cmp(context, operator.le, other)
    def gt(self, context, other):
        return self.cmp(context, operator.gt, other)
    def ge(self, context, other):
        return self.cmp(context, operator.ge, other)
    def __eq__(self, other):
        return self.eq(None, _eval_cmp_value(other))
    def __ne__(self, other):
        return self.ne(None, _eval_cmp_value(other))
    def __lt__(self, other):
        return self.lt(None, _eval_cmp_value(other))
    def __le__(self, other):
        return self.le(None, _eval_cmp_value(other))
    def __gt__(self, other):
        return self.gt(None, _eval_cmp_value(other))
    def __ge__(self, other):
        return self.ge(None, _eval_cmp_value(other))
    def __contains__(self, other):
        return self.has(None, _eval_cmp_value(other))
    def cmp(self, context, cmp_operator, other):
        self.child_ref = None
        value = self.get(context)
        if not isinstance(value, (Dict, List)) and           (self.key is NotImplemented):
            other = self.option_value.option_type(other)
        return cmp_operator(value, other)
    def has(self, context, other):
        value = self.get(context)
        return other in value
    def has_any(self, context, others):
        value = self.get(context)
        for other in to_sequence(others):
            if other in value:
                return True
        return False
    def has_all(self, context, others):
        value = self.get(context)
        for other in to_sequence(others):
            if other not in value:
                return False
        return True
    def one_of(self, context, others):
        value = self.get(context)
        for other in others:
            other = self.option_value.option_type(other)
            if value == other:
                return True
        return False
    def not_in(self, context, others):
        return not self.one_of(context, others)
    def option_type(self):
        self.child_ref = None
        return self.option_value.option_type
class ConditionGeneratorHelper(object):
    __slots__ = ('name', 'options', 'condition', 'key')
    def __init__(self, name, options, condition, key=NotImplemented):
        self.name = name
        self.options = options
        self.condition = condition
        self.key = key
    @staticmethod
    def __cmp_value(options, context, cmp_method, name, key, *args):
        opt = getattr(options, name)
        if key is not NotImplemented:
            opt = opt[key]
        return getattr(opt, cmp_method)(context, *args)
    @staticmethod
    def __make_cmp_condition(condition, cmp_method, name, key, *args):
        return Condition(condition,
                         ConditionGeneratorHelper.__cmp_value,
                         cmp_method,
                         name,
                         key,
                         *args)
    def cmp(self, cmp_method, *args):
        condition = self.__make_cmp_condition(
            self.condition, cmp_method, self.name, self.key, *args)
        return ConditionGenerator(self.options, condition)
    def __iter__(self):
        raise TypeError()
    def __getitem__(self, key):
        if self.key is not NotImplemented:
            raise KeyError(key)
        return ConditionGeneratorHelper(self.name,
                                        self.options,
                                        self.condition,
                                        key)
    def __setitem__(self, key, value):
        if not isinstance(value, ConditionGeneratorHelper):
            value = op_set_key(key, value)
            self.options.append_value(
                self.name, value, op_set, self.condition)
    def eq(self, other):
        return self.cmp('eq', other)
    def ne(self, other):
        return self.cmp('ne', other)
    def gt(self, other):
        return self.cmp('gt', other)
    def ge(self, other):
        return self.cmp('ge', other)
    def lt(self, other):
        return self.cmp('lt', other)
    def le(self, other):
        return self.cmp('le', other)
    def has(self, value):
        return self.cmp('has', value)
    def has_any(self, values):
        return self.cmp('has_any', values)
    def has_all(self, values):
        return self.cmp('has_all', values)
    def one_of(self, values):
        return self.cmp('one_of', values)
    def not_in(self, values):
        return self.cmp('not_in', values)
    def is_true(self):
        return self.cmp('is_true')
    def is_false(self):
        return self.cmp('is_false')
    def __iadd__(self, value):
        if self.key is not NotImplemented:
            value = op_iadd_key(self.key, value)
        self.options.append_value(self.name, value, op_iadd, self.condition)
        return self
    def __isub__(self, value):
        if self.key is not NotImplemented:
            value = op_isub_key(self.key, value)
        self.options.append_value(self.name, value, op_isub, self.condition)
        return self
class ConditionGenerator(object):
    def __init__(self, options, condition=None):
        self.__dict__['__options'] = options
        self.__dict__['__condition'] = condition
    def __getattr__(self, name):
        return ConditionGeneratorHelper(name,
                                        self.__dict__['__options'],
                                        self.__dict__['__condition'])
    def __setattr__(self, name, value):
        if not isinstance(value, ConditionGeneratorHelper):
            condition = self.__dict__['__condition']
            self.__dict__['__options'].append_value(name,
                                                    value,
                                                    op_set,
                                                    condition)
def _items_by_value(items):
    values = {}
    for name, value in items:
        try:
            values[value].add(name)
        except KeyError:
            values[value] = {name}
    return values
class Options (object):
    def __init__(self, parent=None):
        self.__dict__['__parent'] = parent
        self.__dict__['__cache'] = {}
        self.__dict__['__opt_values'] = {}
        self.__dict__['__children'] = []
        if parent is not None:
            parent.__dict__['__children'].append(weakref.ref(self))
    def _add_dependency(self, child):
        children = self.__dict__['__children']
        for child_ref in children:
            if child_ref() is child:
                return
        if child._is_dependency(self):
            raise ErrorOptionsCyclicallyDependent()
        children.append(weakref.ref(child))
    def _is_dependency(self, other):
        children = list(self.__dict__['__children'])
        while children:
            child_ref = children.pop()
            child = child_ref()
            if child is None:
                continue
            if child is other:
                return True
            children += child.__dict__['__children']
        return False
    def _is_parent(self, other):
        if other is None:
            return False
        parent = self.__dict__['__parent']
        while parent is not None:
            if parent is other:
                return True
            parent = parent.__dict__['__parent']
        return False
    def __copy_parent_option(self, opt_value):
        parent = self.__dict__['__parent']
        items = parent._values_map_by_name().items()
        names = [name for name, value in items if value is opt_value]
        opt_value = opt_value.copy()
        self.__set_opt_value(opt_value, names)
        return opt_value
    def get_hash_ref(self):
        if self.__dict__['__opt_values']:
            return weakref.ref(self)
        parent = self.__dict__['__parent']
        if parent is None:
            return weakref.ref(self)
        return parent.get_hash_ref()
    def has_changed_key_options(self):
        parent = self.__dict__['__parent']
        for name, opt_value in self.__dict__['__opt_values'].items():
            if not opt_value.is_tool_key() or not opt_value.is_set():
                continue
            parent_opt_value, from_parent = parent._get_value(
                name, raise_ex=False)
            if parent_opt_value is None:
                continue
            if parent_opt_value.is_set():
                value = self.evaluate(opt_value, None, name)
                parent_value = parent.evaluate(parent_opt_value, None, name)
                if value != parent_value:
                    return True
        return False
    def __add_new_option(self, name, value):
        self.clear_cache()
        if isinstance(value, OptionType):
            opt_value = OptionValue(value)
        elif isinstance(value, OptionValueProxy):
            if value.options is self:
                if not value.from_parent:
                    opt_value = value.option_value
                else:
                    opt_value = self.__copy_parent_option(value.option_value)
            elif self._is_parent(value.options):
                opt_value = self.__copy_parent_option(value.option_value)
            else:
                opt_value = value.option_value.copy()
                opt_value.reset()
                value = self._make_cond_value(value, op_set)
                opt_value.append_value(value)
        elif isinstance(value, OptionValue):
            opt_value = value
        else:
            opt_value = OptionValue(auto_option_type(value))
            value = self._make_cond_value(value, op_set)
            opt_value.append_value(value)
        self.__dict__['__opt_values'][name] = opt_value
    def __set_value(self, name, value, operation_type=op_set):
        opt_value, from_parent = self._get_value(name, raise_ex=False)
        if opt_value is None:
            self.__add_new_option(name, value)
            return
        if isinstance(value, OptionType):
            opt_value.option_type = value
            return
        elif isinstance(value, OptionValueProxy):
            if value.option_value is opt_value:
                return
        elif value is opt_value:
            return
        self._append_value(opt_value, from_parent, value, operation_type)
    def __set_opt_value(self, opt_value, names):
        opt_values = self.__dict__['__opt_values']
        for name in names:
            opt_values[name] = opt_value
    def __setattr__(self, name, value):
        self.__set_value(name, value)
    def __setitem__(self, name, value):
        self.__set_value(name, value)
    def _get_value(self, name, raise_ex):
        try:
            return self.__dict__['__opt_values'][name], False
        except KeyError:
            parent = self.__dict__['__parent']
            if parent is not None:
                value, from_parent = parent._get_value(name, False)
                if value is not None:
                    return value, True
            if raise_ex:
                raise AttributeError(
                    "Options '%s' instance has no option '%s'" %
                    (type(self), name))
            return None, False
    def __getitem__(self, name):
        return self.__getattr__(name)
    def __getattr__(self, name):
        opt_value, from_parent = self._get_value(name, raise_ex=True)
        return OptionValueProxy(opt_value, from_parent, name, self)
    def __contains__(self, name):
        return self._get_value(name, raise_ex=False)[0] is not None
    def __iter__(self):
        raise ErrorOptionsNoIteration()
    def _values_map_by_name(self, result=None):
        if result is None:
            result = {}
        parent = self.__dict__['__parent']
        if parent is not None:
            parent._values_map_by_name(result=result)
        result.update(self.__dict__['__opt_values'])
        return result
    def _values_map_by_value(self):
        items = self._values_map_by_name().items()
        return _items_by_value(items)
    def help(self, with_parent=False, hidden=False):
        if with_parent:
            options_map = self._values_map_by_name()
        else:
            options_map = self.__dict__['__opt_values']
        options2names = _items_by_value(options_map.items())
        result = {}
        for option, names in options2names.items():
            option_help = option.option_type.help()
            if option_help.is_hidden() and not hidden:
                continue
            option_help.names = names
            try:
                option_help.current_value = self.evaluate(option, {}, names)
            except Exception:
                pass
            group_name = option_help.group if option_help.group else ""
            try:
                group = result[group_name]
            except KeyError:
                group = result[group_name] = OptionHelpGroup(group_name)
            group.append(option_help)
        return sorted(result.values(), key=operator.attrgetter('name'))
    def help_text(self, title, with_parent=False, hidden=False, brief=False):
        border = "=" * len(title)
        result = ["", title, border, ""]
        for group in self.help(with_parent=with_parent, hidden=hidden):
            text = group.text(brief=brief, indent=2)
            if result[-1]:
                result.append("")
            result.extend(text)
        return result
    def set_group(self, group):
        opt_values = self._values_map_by_name().values()
        for opt_value in opt_values:
            if isinstance(opt_value, OptionValueProxy):
                opt_value = opt_value.option_value
            opt_value.option_type.group = group
    def __nonzero__(self):
        return bool(self.__dict__['__opt_values']) or             bool(self.__dict__['__parent'])
    def __bool__(self):
        return bool(self.__dict__['__opt_values']) or             bool(self.__dict__['__parent'])
    def update(self, other):
        if not other:
            return
        if self is other:
            return
        if isinstance(other, Options):
            self.merge(other)
        else:
            ignore_types = (ConditionGeneratorHelper,
                            ConditionGenerator,
                            Options)
            for name, value in other.items():
                if isinstance(value, ignore_types):
                    continue
                try:
                    self.__set_value(name, value, op_iupdate)
                except ErrorOptionTypeCantDeduce:
                    pass
    def __merge(self, self_names, other_names, move_values=False):
        self.clear_cache()
        other_values = _items_by_value(other_names.items())
        self_names_set = set(self_names)
        self_values = _items_by_value(self_names.items())
        for value, names in other_values.items():
            same_names = names & self_names_set
            if same_names:
                self_value_name = next(iter(same_names))
                self_value = self_names[self_value_name]
                self_values_names = self_values[self_value]
                self_other_names = same_names - self_values_names
                if self_other_names:
                    raise ErrorOptionsMergeDifferentOptions(
                        self_value_name, self_other_names.pop())
                else:
                    new_names = names - self_values_names
                    self_value.merge(value)
            else:
                if move_values:
                    self_value = value
                else:
                    self_value = value.copy()
                new_names = names
            self.__set_opt_value(self_value, new_names)
    def merge(self, other):
        if not other:
            return
        if self is other:
            return
        if not isinstance(other, Options):
            raise ErrorOptionsMergeNonOptions(other)
        if other._is_parent(self):
            raise ErrorOptionsMergeChild()
        self.__merge(self._values_map_by_name(), other._values_map_by_name())
    def join(self):
        parent = self.__dict__['__parent']
        if parent is None:
            raise ErrorOptionsJoinNoParent(self)
        if self.__dict__['__children']:
            raise ErrorOptionsJoinParent(self)
        parent.__merge(parent.__dict__['__opt_values'],
                       self.__dict__['__opt_values'],
                       move_values=True)
        self.clear()
    def unjoin(self):
        parent = self.__dict__['__parent']
        if parent is None:
            return
        self.__merge(
            self.__dict__['__opt_values'], parent._values_map_by_name())
        self.__dict__['__parent'] = None
    def __unjoin_children(self):
        children = self.__dict__['__children']
        for child_ref in children:
            child = child_ref()
            if child is not None:
                child.unjoin()
        del children[:]
    def __clear_children_cache(self):
        def _clear_child_cache(ref):
            child = ref()
            if child is not None:
                child.clear_cache()
                return True
            return False
        self.__dict__['__children'] = list(
            filter(_clear_child_cache, self.__dict__['__children']))
    def __remove_child(self, child):
        def _filter_child(child_ref, removed_child=child):
            filter_child = child_ref()
            return (filter_child is not None) and                    (filter_child is not removed_child)
        self.__dict__['__children'] = list(
            filter(_filter_child, self.__dict__['__children']))
    def clear(self):
        parent = self.__dict__['__parent']
        self.__unjoin_children()
        if parent is not None:
            parent.__remove_child(self)
        self.__dict__['__parent'] = None
        self.__dict__['__cache'].clear()
        self.__dict__['__opt_values'].clear()
    def override(self, **kw):
        other = Options(self)
        other.update(kw)
        return other
    def copy(self):
        other = Options()
        for opt_value, names in self._values_map_by_value().items():
            other.__set_opt_value(opt_value.copy(), names)
        return other
    def _evaluate(self, option_value, context):
        try:
            if context is not None:
                return context[option_value]
        except KeyError:
            pass
        attrs = self.__dict__
        if attrs['__opt_values']:
            cache = attrs['__cache']
        else:
            cache = attrs['__parent'].__dict__['__cache']
        try:
            return cache[option_value]
        except KeyError:
            pass
        value = option_value.get(self, context, _load_op_value)
        cache[option_value] = value
        return value
    def evaluate(self, option_value, context, name):
        try:
            return self._evaluate(option_value, context)
        except ErrorOptionTypeUnableConvertValue as ex:
            if not name:
                raise
            option_help = ex.option_help
            if option_help.names:
                raise
            option_help.names = tuple(to_sequence(name))
            raise ErrorOptionTypeUnableConvertValue(
                option_help, ex.invalid_value)
        except Exception as ex:
            raise ErrorOptionsUnableEvaluate(name, ex)
    def _store_value(self, value):
        if isinstance(value, Operation):
            value.convert(self, _store_op_value)
        else:
            value = _store_op_value(self, value)
        return value
    def _load_value(self, value):
        if isinstance(value, Operation):
            return value(self, {}, _load_op_value)
        else:
            value = _load_op_value(self, {}, value)
        return value
    def _make_cond_value(self, value, operation_type, condition=None):
        if isinstance(value, ConditionalValue):
            return value
        if not isinstance(value, InplaceOperation):
            value = operation_type(value)
        value = ConditionalValue(value, condition)
        value.convert(self, _store_op_value)
        return value
    def append_value(self, name, value, operation_type, condition=None):
        opt_value, from_parent = self._get_value(name, raise_ex=True)
        self._append_value(
            opt_value, from_parent, value, operation_type, condition)
    def _append_value(self,
                      opt_value,
                      from_parent,
                      value,
                      operation_type,
                      condition=None):
        value = self._make_cond_value(value, operation_type, condition)
        self.clear_cache()
        if from_parent:
            opt_value = self.__copy_parent_option(opt_value)
        opt_value.append_value(value)
    def clear_cache(self):
        self.__dict__['__cache'].clear()
        self.__clear_children_cache()
    def when(self, cond=None):
        if cond is not None:
            if isinstance(cond, ConditionGeneratorHelper):
                cond = cond.condition
            elif isinstance(cond, ConditionGenerator):
                cond = cond.__dict__['__condition']
            elif not isinstance(cond, Condition):
                cond = Condition(None,
                                 lambda options, context, arg: bool(arg),
                                 cond)
        return ConditionGenerator(self, cond)
    If = when
class ErrorEntitiesFileUnknownEntity(Exception):
    def __init__(self, entity):
        msg = "Unknown entity: %s" % (entity, )
        super(ErrorEntitiesFileUnknownEntity, self).__init__(msg)
class EntitiesFile (object):
    __slots__ = (
        'data_file',
        'file_lock',
        'cache',
        'pickler',
    )
    def __init__(self, filename, use_sqlite=False, force=False):
        self.cache = {}
        self.data_file = None
        self.pickler = EntityPickler()
        self.open(filename, use_sqlite=use_sqlite, force=force)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_entity, traceback):
        self.close()
    def open(self, filename, use_sqlite=False, force=False):
        self.file_lock = FileLock(filename)
        self.file_lock.write_lock(wait=False, force=force)
        if use_sqlite:
            self.data_file = SqlDataFile(filename, force=force)
        else:
            self.data_file = DataFile(filename, force=force)
    def close(self):
        self.cache.clear()
        if self.data_file is not None:
            self.data_file.close()
            self.data_file = None
        self.file_lock.release_lock()
    def clear(self):
        if self.data_file is not None:
            self.data_file.clear()
        self.cache.clear()
    def find_node_entity(self, entity):
        entity_id = entity.id
        dump = self.data_file.read(entity_id)
        if dump is None:
            return None
        try:
            entity = self.pickler.loads(dump)
            entity.id = entity_id
        except Exception:
            self.data_file.remove((entity_id,))
            return None
        return entity
    def add_node_entity(self, entity):
        dump = self.pickler.dumps(entity)
        self.data_file.write(entity.id, dump)
    def remove_node_entities(self, entities):
        entity_ids = map(operator.attrgetter('id'), entities)
        self.data_file.remove(entity_ids)
    def _find_entity_by_id(self, entity_id):
        try:
            return self.cache[entity_id]
        except KeyError:
            pass
        data = self.data_file.read(entity_id)
        if data is None:
            raise ValueError()
        try:
            entity = self.pickler.loads(data)
            entity.id = entity_id
        except Exception:
            self.data_file.remove((entity_id,))
            raise ValueError()
        self.cache[entity_id] = entity
        return entity
    def find_entities_by_key(self, keys):
        entity_ids = self.data_file.get_ids(keys)
        if entity_ids is None:
            return None
        try:
            return list(map(self._find_entity_by_id, entity_ids))
        except Exception:
            return None
    def find_entities(self, entities):
        try:
            return list(map(self._find_entity_by_id,
                            map(operator.attrgetter('id'), entities)))
        except Exception:
            return None
    def add_entities(self, entities):
        keys = []
        entity_ids = []
        key_append = keys.append
        entity_append = entity_ids.append
        for entity in entities:
            entity_id = entity.id
            try:
                stored_entity = self._find_entity_by_id(entity_id)
                if stored_entity == entity:
                    entity_append(entity_id)
                    continue
            except Exception:
                pass
            key = self.update_entity(entity)
            key_append(key)
        keys.extend(self.data_file.get_keys(entity_ids))
        return keys
    def update_entity(self, entity):
        entity_id = entity.id
        self.cache[entity_id] = entity
        data = self.pickler.dumps(entity)
        key = self.data_file.write_with_key(entity_id, data)
        return key
    def remove_entities(self, entities):
        remove_ids = tuple(map(operator.attrgetter('id'), entities))
        for entity_id in remove_ids:
            try:
                del self.cache[entity_id]
            except KeyError:
                pass
        self.data_file.remove(remove_ids)
    def self_test(self):
        if self.data_file is None:
            if self.cache:
                raise AssertionError("cache is not empty")
            return
        self.data_file.self_test()
        for entity_id, entity in self.cache.items():
            if entity_id != entity.id:
                raise AssertionError(
                    "entity_id(%s) != entity.id(%s)" % (entity_id, entity.id))
            dump = self.data_file.read(entity_id)
            stored_entity = self.pickler.loads(dump)
            if stored_entity != entity:
                raise AssertionError("stored_entity(%s) != entity(%s)" %
                                     (stored_entity.id, entity.id))
class ErrorEntityNameEmpty(Exception):
    def __init__(self):
        msg = "Entity name is empty"
        super(ErrorEntityNameEmpty, self).__init__(msg)
class ErrorSignatureEntityInvalidDataType(Exception):
    def __init__(self, data):
        msg = "Signature data type must be bytes or bytearray, "               "actual type: '%s'" % (type(data),)
        super(ErrorSignatureEntityInvalidDataType, self).__init__(msg)
class ErrorTextEntityInvalidDataType(Exception):
    def __init__(self, text):
        msg = "Text data type must be string, actual type: '%s'" % (
            type(text),)
        super(ErrorTextEntityInvalidDataType, self).__init__(msg)
class EntityBase (object):
    __slots__ = ('id', 'name', 'signature', 'tags')
    def __new__(cls, name, signature, tags=None):
        self = super(EntityBase, cls).__new__(cls)
        if name is not NotImplemented:
            if not name:
                raise ErrorEntityNameEmpty()
            self.name = name
        if signature is not NotImplemented:
            self.signature = signature
        self.tags = frozenset(to_sequence(tags))
        return self
    def __hash__(self):
        return hash(self.id)
    def get(self):
        """
        Returns value of the entity
        """
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def get_id(self):
        cls = self.__class__
        return simple_object_signature((self.name,
                                        cls.__name__,
                                        cls.__module__))
    def get_name(self):
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def get_signature(self):
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def __getattr__(self, attr):
        if attr == 'signature':
            self.signature = signature = self.get_signature()
            return signature
        elif attr == 'name':
            self.name = name = self.get_name()
            return name
        elif attr == 'id':
            self.id = entity_id = self.get_id()
            return entity_id
        raise AttributeError("Unknown attribute: '%s'" % (attr,))
    def __getnewargs__(self):
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def is_actual(self):
        """
        Checks whether the entity is actual or not
        """
        return bool(self.signature)
    def get_actual(self):
        """
        Returns an actual entity.
        If the current entity is actual then it will be simply returned.
        """
        return self
    def __getstate__(self):
        return {}
    def __setstate__(self, state):
        pass
    def __eq__(self, other):
        return (self.id == other.id) and                (self.signature == other.signature)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return cast_str(self.get())
    def remove(self):
        pass
@pickleable
class SimpleEntity (EntityBase):
    __slots__ = ('data', )
    def __new__(cls, data=None, name=None, signature=None, tags=None):
        if data is None:
            signature = None
        else:
            if signature is None:
                signature = simple_object_signature(data)
        if not name:
            name = signature
        self = super(SimpleEntity, cls).__new__(cls, name, signature, tags)
        self.data = data
        return self
    def get(self):
        return self.data
    def __getnewargs__(self):
        tags = self.tags
        if not tags:
            tags = None
        name = self.name
        if name == self.signature:
            name = None
        return self.data, name, self.signature, tags
@pickleable
class NullEntity (EntityBase):
    def __new__(cls):
        name = 'N'
        signature = None
        return super(NullEntity, cls).__new__(cls, name, signature)
    def get(self):
        return None
    def __getnewargs__(self):
        return tuple()
    def is_actual(self):
        return False
@pickleable
class SignatureEntity (EntityBase):
    def __new__(cls, data=None, name=None, tags=None):
        if data is not None:
            if not isinstance(data, (bytes, bytearray)):
                raise ErrorSignatureEntityInvalidDataType(data)
        if not name:
            name = data
        return super(SignatureEntity, cls).__new__(cls, name, data, tags)
    def get(self):
        return self.signature
    def __getnewargs__(self):
        tags = self.tags
        if not tags:
            tags = None
        name = self.name
        if name == self.signature:
            name = None
        return self.signature, name, tags
def _build_options():
    options = Options()
    options.build_path = PathOptionType(
        description="The building directory full path.")
    options.build_dir = PathOptionType(
        description="The building directory.", default='build_output')
    options.relative_build_paths = BoolOptionType(
        description="The building directory suffix.", default=True)
    options.build_dir_name = StrOptionType(
        description="The building directory name.")
    options.prefix = StrOptionType(description="Output files prefix.")
    options.suffix = StrOptionType(description="Output files suffix.")
    options.target = StrOptionType(description="Output file name.")
    build_variant = EnumOptionType(values=[
        ('debug', 'dbg', 'd'),
        ('release_speed', 'release',
         'rel', 'rs', 'speed'),
        ('release_size', 'rz',
         'rel_size', 'size'),
        ('final', 'f'),
    ],
        default='debug',
        description="Current build variant")
    options.build_variant = build_variant
    options.bv = options.build_variant
    options.build_variants = ListOptionType(
        value_type=build_variant,
        unique=True,
        description="Active build variants"
    )
    options.bvs = options.build_variants
    file_signature = EnumOptionType(
        values=[('checksum', 'md5', 'sign'), ('timestamp', 'time')],
        default='checksum',
        description="Type used to detect changes in dependency files"
    )
    options.file_signature = file_signature
    options.signature = options.file_signature
    options.batch_build = BoolOptionType(description="Prefer batch build.")
    options.batch_groups = OptionType(
        value_type=int,
        default=1,
        description="Preferred number of batching groups."
    )
    options.batch_size = OptionType(
        value_type=int,
        default=0,
        description="Preferred size of a batching group.")
    options.set_group("Build")
    return options
def _target_options():
    options = Options()
    options.target_os = EnumOptionType(
        values=['native', 'unknown',
                ('windows',
                 'win32', 'win64'),
                ('linux', 'linux-gnu'),
                'uclinux',
                'cygwin',
                'interix',
                'freebsd',
                'openbsd',
                'netbsd',
                ('OS-X', 'osx', 'darwin'),
                'java',
                'sunos',
                'hpux',
                'vxworks',
                'solaris',
                'elf'],
        default='native',
        strict=False,
        is_tool_key=True,
        description="The target system/OS name, e.g. 'Linux', 'Windows' etc.")
    options.os = options.target_os
    options.target_arch = EnumOptionType(
        values=['native', 'unknown',
                ('x86-32', 'x86_32', 'x86', '80x86', 'i386', 'i486', 'i586',
                 'i686'),
                ('x86-64', 'x86_64', 'amd64', 'x64'),
                'arm', 'arm64',
                'alpha',
                'mips',
                'ia64',
                'm68k',
                'sparc',
                'sparc64',
                'sparcv9',
                'powerpc',
                ],
        default='native',
        strict=False,
        is_tool_key=True,
        description="The target machine type, e.g. 'i386'")
    options.arch = options.target_arch
    options.target_subsystem = EnumOptionType(
        values=['console', 'windows'],
        default='console',
        description="The target subsystem."
    )
    options.target_platform = StrOptionType(
        ignore_case=True,
        description="The target system's distribution, e.g. 'win32', 'Linux'"
    )
    options.target_os_release = StrOptionType(
        ignore_case=True,
        description="The target system's release, e.g. '2.2.0' or 'XP'"
    )
    options.target_os_version = VersionOptionType(
        description="The target system's release version, "
                    "e.g. '2.2.0' or '5.1.2600'"
    )
    options.target_cpu = StrOptionType(
        ignore_case=True,
        description="The target real processor name, e.g. 'amdk6'.")
    options.target_cpu_flags = ListOptionType(
        value_type=IgnoreCaseString,
        description="The target CPU flags, e.g. 'mmx', 'sse2'.")
    options.set_group("Target system")
    return options
def _optimization_options():
    options = Options()
    options.optimization = EnumOptionType(
        values=[('off', 0), ('size', 1), ('speed', 2)],
        default='off',
        description='Optimization level'
    )
    options.optlevel = options.optimization
    options.opt = options.optimization
    options.inlining = EnumOptionType(values=['off', 'on', 'full'],
                                      default='off',
                                      description='Inline function expansion')
    options.whole_optimization = BoolOptionType(
        description='Whole program optimization')
    options.whole_opt = options.whole_optimization
    options.set_group("Optimization")
    return options
def _code_gen_options():
    options = Options()
    options.debug_symbols = BoolOptionType(
        description='Include debug symbols', style=('on', 'off'))
    options.profile = BoolOptionType(
        description='Enable compiler profiling', style=('on', 'off'))
    options.keep_asm = BoolOptionType(
        description='Keep generated assemblers files')
    options.runtime_link = EnumOptionType(
        values=['default', 'static', ('shared', 'dynamic')],
        default='default',
        description='Linkage type of runtime library')
    options.rt_link = options.runtime_link
    options.runtime_debug = BoolOptionType(
        style=('on', 'off'),
        description='Use debug version of runtime library'
    )
    options.rt_debug = options.runtime_debug
    options.rtti = BoolOptionType(
        description='Enable Run Time Type Information', default=True)
    options.exceptions = BoolOptionType(
        description='Allow to throw exceptions', default=True)
    options.runtime_thread = EnumOptionType(
        values=['default', 'single', 'multi'],
        default='default',
        description='Threading mode of runtime library'
    )
    options.rt_thread = options.runtime_thread
    options.set_group("Code generation")
    return options
def _diagnostic_options():
    options = Options()
    options.warning_level = RangeOptionType(
        0, 4, description='Warning level', default=4)
    options.warn_level = options.warning_level
    options.warning_as_error = BoolOptionType(
        description='Treat warnings as errors')
    options.werror = options.warning_as_error
    options.warnings_as_errors = options.warning_as_error
    options.lint = EnumOptionType(
        values=[('off', 0), ('on', 1), ('global', 2)],
        default='off',
        description='Lint source code.',
        is_hidden=True
    )
    options.lint_flags = ListOptionType(description="Lint tool options",
                                        is_hidden=True)
    options.set_group("Diagnostic")
    return options
def _env_options():
    if os.path.normcase('ABC') == os.path.normcase('abc'):
        env_key_type = UpperCaseString
    else:
        env_key_type = String
    options = Options()
    options.env = DictOptionType(key_type=env_key_type)
    options.env['PATH'] = ListOptionType(
        value_type=PathOptionType(),
        separators=os.pathsep
    )
    options.env['PATHEXT'] = ListOptionType(
        value_type=PathOptionType(),
        separators=os.pathsep
    )
    options.env['TEMP'] = PathOptionType()
    options.env['TMP'] = PathOptionType()
    options.env['HOME'] = PathOptionType()
    options.env['HOMEPATH'] = PathOptionType()
    options.env = os.environ.copy()
    return options
def _init_defaults(options):
    if_ = options.If()
    if_.target_os.ne('native').build_dir_name += options.target_os + '_'
    if_.target_arch.ne('native').build_dir_name += options.target_arch + '_'
    options.build_dir_name += options.build_variant
    options.build_path = SimpleOperation(
        os.path.join, options.build_dir, options.build_dir_name)
    bv = if_.build_variant
    debug_build_variant = bv.eq('debug')
    debug_build_variant.optimization = 'off'
    debug_build_variant.inlining = 'off'
    debug_build_variant.whole_optimization = 'off'
    debug_build_variant.debug_symbols = 'on'
    debug_build_variant.runtime_debug = 'on'
    speed_build_variant = bv.one_of(['release_speed', 'final'])
    speed_build_variant.optimization = 'speed'
    speed_build_variant.inlining = 'full'
    speed_build_variant.whole_optimization = 'on'
    speed_build_variant.debug_symbols = 'off'
    speed_build_variant.runtime_debug = 'off'
    size_build_variant = bv.eq('release_size')
    size_build_variant.optimization = 'size'
    size_build_variant.inlining = 'on'
    size_build_variant.whole_optimization = 'on'
    size_build_variant.debug_symbols = 'off'
    size_build_variant.runtime_debug = 'off'
def builtin_options():
    options = Options()
    options.merge(_build_options())
    options.merge(_target_options())
    options.merge(_optimization_options())
    options.merge(_code_gen_options())
    options.merge(_diagnostic_options())
    options.merge(_env_options())
    _init_defaults(options)
    return options
class ErrorFileEntityNoName(Exception):
    def __init__(self):
        msg = "Filename is not specified"
        super(ErrorFileEntityNoName, self).__init__(msg)
class FileEntityBase (EntityBase):
    def __new__(cls, name, signature=NotImplemented, tags=None):
        if isinstance(name, FileEntityBase):
            name = name.name
        else:
            if isinstance(name, EntityBase):
                name = name.get()
        if not name:
            raise ErrorFileEntityNoName()
        name = os.path.normcase(os.path.abspath(name))
        self = super(FileEntityBase, cls).__new__(cls, name,
                                                  signature, tags=tags)
        return self
    def get(self):
        return self.name
    def __getnewargs__(self):
        tags = self.tags
        if not tags:
            tags = None
        return self.name, self.signature, tags
    def remove(self):
        try:
            os.remove(self.name)
        except OSError:
            pass
    def get_actual(self):
        signature = self.get_signature()
        if self.signature == signature:
            return self
        other = super(FileEntityBase, self).__new__(self.__class__,
                                                    self.name,
                                                    signature,
                                                    self.tags)
        other.id = self.id
        return other
    def is_actual(self):
        if not self.signature:
            return False
        if self.signature == self.get_signature():
            return True
        return False
def _get_file_checksum(path, offset=0):
    try:
        signature = file_signature(path, offset)
    except (OSError, IOError):
        try:
            signature = file_time_signature(path)
        except (OSError, IOError):
            return None
    return signature
def _get_file_timestamp(path):
    try:
        signature = file_time_signature(path)
    except (OSError, IOError):
        return None
    return signature
@pickleable
class FileChecksumEntity(FileEntityBase):
    def get_signature(self):
        return _get_file_checksum(self.name)
@pickleable
class FileTimestampEntity(FileEntityBase):
    def get_signature(self):
        return _get_file_timestamp(self.name)
@pickleable
class DirEntity (FileTimestampEntity):
    def remove(self):
        try:
            os.rmdir(self.name)
        except OSError:
            pass
@pickleable
class FilePartChecksumEntity (FileEntityBase):
    __slots__ = ('offset',)
    def __new__(cls, name, signature=NotImplemented, tags=None, offset=0):
        self = super(FilePartChecksumEntity, cls).__new__(cls,
                                                          name,
                                                          signature,
                                                          tags=tags)
        self.offset = offset
        return self
    def __getnewargs__(self):
        tags = self.tags
        if not tags:
            tags = None
        return self.name, self.signature, tags, self.offset
    def get_signature(self):
        return _get_file_checksum(self.name, self.offset)
    def get_actual(self):
        signature = self.get_signature()
        if self.signature == signature:
            return self
        other = super(FileEntityBase, self).__new__(self.__class__,
                                                    self.name,
                                                    signature,
                                                    self.tags)
        other.id = self.id
        other.offset = self.offset
        return other
    def __eq__(self, other):
        return super(FilePartChecksumEntity, self).__eq__(other) and             (self.offset == other.offset)
@event_debug
def event_exec_cmd(settings, cmd, cwd, env):
    if settings.trace_exec:
        cmd = ' '.join(cmd)
        log_debug("CWD: '%s', CMD: '%s'", cwd, cmd)
def _get_trace_arg(entity, brief):
    if isinstance(entity, FileEntityBase):
        value = entity.get()
        if brief:
            value = os.path.basename(value)
    else:
        if isinstance(entity, FilePath):
            value = entity
            if brief:
                value = os.path.basename(value)
        else:
            if isinstance(entity, EntityBase):
                value = to_string(entity.get())
            else:
                value = to_string(entity)
            value = value.strip()
            max_len = 64 if brief else 256
            src_len = len(value)
            if src_len > max_len:
                value = "%s...%s" % (value[:max_len // 2],
                                     value[src_len - (max_len // 2):])
            value = value.replace('\r', '')
            value = value.replace('\n', ' ')
    return value
def _join_args(entities, brief):
    args = [_get_trace_arg(arg, brief) for arg in to_sequence(entities)]
    if not brief or (len(args) < 3):
        return ' '.join(args)
    wish_size = 128
    args_str = [args.pop(0)]
    last = args.pop()
    size = len(args_str[0]) + len(last)
    for arg in args:
        size += len(arg)
        if size > wish_size:
            args_str.append('...')
            break
        args_str.append(arg)
    args_str.append(last)
    return ' '.join(args_str)
def _get_trace_str(name, sources, targets, brief):
    name = _join_args(name, brief)
    sources = _join_args(sources, brief)
    targets = _join_args(targets, brief)
    build_str = name
    if sources:
        build_str += " << " + sources
    if targets:
        build_str += " >> " + targets
    return build_str
def _make_build_path(path_dir, _path_cache=set()):
    if path_dir not in _path_cache:
        if not os.path.isdir(path_dir):
            try:
                os.makedirs(path_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        _path_cache.add(path_dir)
def _make_build_paths(dirnames):
    for dirname in dirnames:
        _make_build_path(dirname)
def _split_filename_ext(filename, ext, replace_ext):
    if ext:
        if filename.endswith(ext):
            return filename[:-len(ext)], ext
        if not replace_ext:
            return filename, ext
    ext_pos = filename.rfind(os.path.extsep)
    if ext_pos > 0:
        if not ext:
            ext = filename[ext_pos:]
        filename = filename[:ext_pos]
    return filename, ext
def _split_file_name(file_path,
                     ext=None,
                     prefix=None,
                     suffix=None,
                     replace_ext=False
                     ):
    if isinstance(file_path, EntityBase):
        file_path = file_path.get()
    dirname, filename = os.path.split(file_path)
    filename, ext = _split_filename_ext(filename, ext, replace_ext)
    if prefix:
        filename = prefix + filename
    if suffix:
        filename += suffix
    if ext:
        filename += ext
    return dirname, filename
def _split_file_names(file_paths,
                      ext=None,
                      prefix=None,
                      suffix=None,
                      replace_ext=False):
    dirnames = []
    filenames = []
    for file_path in file_paths:
        dirname, filename = _split_file_name(file_path, ext, prefix, suffix,
                                             replace_ext)
        dirnames.append(dirname)
        filenames.append(filename)
    return dirnames, filenames
def _get_file_signature_type(file_signature_type):
    if file_signature_type == 'timestamp':
        return FileTimestampEntity
    return FileChecksumEntity
class BuilderInitiator(object):
    __slots__ = ('is_initiated', 'builder', 'options', 'args', 'kw')
    def __init__(self, builder, options, args, kw):
        self.is_initiated = False
        self.builder = builder
        self.options = options
        self.args = self.__store_args(args)
        self.kw = self.__store_kw(kw)
    def __store_args(self, args):
        return tuple(map(self.options._store_value, args))
    def __load_args(self):
        return tuple(map(self.options._load_value, self.args))
    def __store_kw(self, kw):
        store_value = self.options._store_value
        return dict((name, store_value(value)) for name, value in kw.items())
    def __load_kw(self):
        load_value = self.options._load_value
        return dict((name, load_value(value))
                    for name, value in self.kw.items())
    def initiate(self):
        if self.is_initiated:
            return self.builder
        builder = self.builder
        kw = self.__load_kw()
        args = self.__load_args()
        options = self.options
        builder._init_attrs(options)
        builder.__init__(options, *args, **kw)
        if not hasattr(builder, 'name'):
            builder.set_name()
        if not hasattr(builder, 'signature'):
            builder.set_signature()
        self.is_initiated = True
        return builder
    def can_build_batch(self):
        return self.builder.can_build_batch()
    def can_build(self):
        return self.builder.can_build()
    def is_batch(self):
        return self.builder.is_batch()
class Builder (object):
    """
    Base class for all builders
    'name' - uniquely identifies builder
    'signature' - uniquely identifies builder's parameters
    """
    NAME_ATTRS = None
    SIGNATURE_ATTRS = None
    def __new__(cls, options, *args, **kw):
        self = super(Builder, cls).__new__(cls)
        return BuilderInitiator(self, options, args, kw)
    def _init_attrs(self, options):
        self.build_dir = options.build_dir.get()
        self.build_path = options.build_path.get()
        self.relative_build_paths = options.relative_build_paths.get()
        if options.file_signature == 'timestamp':
            self.use_timestamp = True
            self.file_entity_type = FileTimestampEntity
        else:
            self.use_timestamp = False
            self.file_entity_type = FileChecksumEntity
        self.env = options.env.get()
        is_batch = (options.batch_build.get() or not self.can_build()) and             self.can_build_batch()
        self.__is_batch = is_batch
        if is_batch:
            self.batch_groups = options.batch_groups.get()
            self.batch_size = options.batch_size.get()
    def can_build_batch(self):
        return self.__class__.build_batch != Builder.build_batch
    def can_build(self):
        return self.__class__.build != Builder.build
    def is_batch(self):
        return self.__is_batch
    def initiate(self):
        return self
    def set_name(self):
        cls = self.__class__
        name = [cls.__module__,
                cls.__name__,
                simplify_value(self.build_path),
                bool(self.relative_build_paths)]
        if self.NAME_ATTRS:
            name.extend(simplify_value(getattr(self, attr_name))
                        for attr_name in self.NAME_ATTRS)
        self.name = simple_object_signature(name)
    def set_signature(self):
        sign = []
        if self.SIGNATURE_ATTRS:
            sign.extend(simplify_value(getattr(self, attr_name))
                        for attr_name in self.SIGNATURE_ATTRS)
        self.signature = simple_object_signature(sign)
    def check_actual(self, target_entities):
        """
        Checks that previous target entities are still up to date.
        It called only if all other checks were successful.
        Returns None if all targets are actual.
        Otherwise first not actual target.
        :param target_entities: Previous target entities
        """
        for entity in target_entities:
            if not entity.is_actual():
                return target_entities
        return None
    def clear(self, target_entities, side_effect_entities):
        for entity in target_entities:
            entity.remove()
        for entity in side_effect_entities:
            entity.remove()
    def depends(self, options, source_entities):
        """
        Could be used to dynamically generate dependency nodes
        Returns list of dependency nodes or None
        """
        return None
    def replace(self, options, source_entities):
        """
        Could be used to dynamically replace sources
        Returns list of nodes/entities or None (if sources are not changed)
        """
        return None
    def split(self, source_entities):
        """
        Could be used to dynamically split building sources to several nodes
        Returns list of groups of source entities or None
        """
        return None
    def split_single(self, source_entities):
        """
        Implementation of split for splitting one-by-one
        """
        return source_entities
    def split_batch(self, source_entities):
        """
        Implementation of split for splitting to batch groups of batch size
        """
        return group_items(source_entities, self.batch_groups, self.batch_size)
    def split_batch_by_build_dir(self, source_entities):
        """
        Implementation of split for grouping sources by output
        """
        num_groups = self.batch_groups
        group_size = self.batch_size
        if self.relative_build_paths:
            path_getter = operator.methodcaller('get')
            groups = group_paths_by_dir(source_entities,
                                        num_groups,
                                        group_size,
                                        path_getter=path_getter)
        else:
            groups = group_items(source_entities, num_groups, group_size)
        return groups
    def get_weight(self, source_entities):
        return len(source_entities)
    def build(self, source_entities, targets):
        """
        Builds a node
        Returns a build output string or None
        """
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def build_batch(self, source_entities, targets):
        """
        Builds a node
        Returns a build output string or None
        """
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def get_target_entities(self, source_entities):
        """
        If it's possible returns target entities of the node, otherwise None
        """
        return None
    def get_trace_name(self, source_entities, brief):
        return self.__class__.__name__
    def get_trace_sources(self, source_entities, brief):
        return source_entities
    def get_trace_targets(self, target_entities, brief):
        return target_entities
    def get_trace(self,
                  source_entities=None,
                  target_entities=None,
                  brief=False):
        try:
            name = self.get_trace_name(source_entities, brief)
        except Exception:
            name = ''
        try:
            sources = self.get_trace_sources(source_entities, brief)
        except Exception:
            sources = None
        try:
            if (target_entities is None) and source_entities:
                target_entities = self.get_target_entities(source_entities)
            targets = self.get_trace_targets(target_entities, brief)
        except Exception:
            targets = None
        return _get_trace_str(name, sources, targets, brief)
    def get_build_dir(self):
        _make_build_path(self.build_dir)
        return self.build_dir
    def get_build_path(self):
        _make_build_path(self.build_path)
        return self.build_path
    def get_target_path(self, target, ext=None, prefix=None):
        target_dir, name = _split_file_name(target,
                                            prefix=prefix,
                                            ext=ext,
                                            replace_ext=False)
        if target_dir.startswith((os.path.curdir, os.path.pardir)):
            target_dir = os.path.abspath(target_dir)
        elif not os.path.isabs(target_dir):
            target_dir = os.path.abspath(os.path.join(self.build_path,
                                                      target_dir))
        _make_build_path(target_dir)
        target = os.path.join(target_dir, name)
        return target
    @staticmethod
    def makedirs(path):
        _make_build_path(path)
    def get_target_dir(self, target_dir):
        target_dir, name = os.path.split(target_dir)
        if not name:
            target_dir, name = os.path.split(target_dir)
        elif not target_dir and name in (os.path.curdir, os.path.pardir):
            target_dir = name
            name = ''
        if target_dir.startswith((os.path.curdir, os.path.pardir)):
            target_dir = os.path.abspath(target_dir)
        elif not os.path.isabs(target_dir):
            target_dir = os.path.abspath(os.path.join(self.build_path,
                                                      target_dir))
        target_dir = os.path.join(target_dir, name)
        _make_build_path(target_dir)
        return target_dir
    def get_source_target_path(self,
                               file_path,
                               ext=None,
                               prefix=None,
                               suffix=None,
                               replace_ext=True):
        build_path = self.build_path
        dirname, filename = _split_file_name(file_path,
                                             ext=ext,
                                             prefix=prefix,
                                             suffix=suffix,
                                             replace_ext=replace_ext)
        if self.relative_build_paths:
            build_path = relative_join(build_path, dirname)
        _make_build_path(build_path)
        build_path = os.path.join(build_path, filename)
        return build_path
    def get_source_target_paths(self,
                                file_paths,
                                ext=None,
                                prefix=None,
                                suffix=None,
                                replace_ext=True):
        build_path = self.build_path
        dirnames, filenames = _split_file_names(file_paths,
                                                ext=ext,
                                                prefix=prefix,
                                                suffix=suffix,
                                                replace_ext=replace_ext)
        if self.relative_build_paths:
            dirnames = relative_join_list(build_path, dirnames)
            _make_build_paths(dirnames)
            build_paths = [os.path.join(dirname, filename)
                           for dirname, filename in zip(dirnames, filenames)]
        else:
            _make_build_path(build_path)
            build_paths = [
                os.path.join(build_path, filename) for filename in filenames]
        return build_paths
    def make_entity(self, value, tags=None):
        if isinstance(value, FilePath):
            return self.make_file_entity(name=value, tags=tags)
        return SimpleEntity(value, tags=tags)
    def make_simple_entity(self, value, tags=None):
        return SimpleEntity(value, tags=tags)
    def make_file_entity(self, value, tags=None):
        return self.file_entity_type(name=value, tags=tags)
    def make_file_entities(self, entities, tags=None):
        make_file_entity = self.make_file_entity
        for entity in to_sequence(entities):
            if isinstance(entity, EntityBase):
                yield entity
            else:
                yield make_file_entity(entity, tags)
    def make_entities(self, entities, tags=None):
        make_entity = self.make_entity
        for entity in to_sequence(entities):
            if isinstance(entity, EntityBase):
                yield entity
            else:
                yield make_entity(entity, tags)
    def exec_cmd(self, cmd, cwd=None, env=None, file_flag=None, stdin=None):
        result = self.exec_cmd_result(
            cmd, cwd=cwd, env=env, file_flag=file_flag, stdin=stdin)
        if result.failed():
            raise result
        return result.output()
    def exec_cmd_result(self,
                        cmd,
                        cwd=None,
                        env=None,
                        file_flag=None,
                        stdin=None):
        if env is None:
            env = self.env
        if cwd is None:
            cwd = self.get_build_path()
        result = execute_command(
            cmd, cwd=cwd, env=env, file_flag=file_flag, stdin=stdin)
        event_exec_cmd(cmd, cwd, env)
        return result
class FileBuilder (Builder):
    make_entity = Builder.make_file_entity
class ErrorNodeDependencyInvalid(Exception):
    def __init__(self, dep):
        msg = "Invalid node dependency: %s" % (dep,)
        super(ErrorNodeDependencyInvalid, self).__init__(msg)
class ErrorNodeSplitUnknownSource(Exception):
    def __init__(self, node, entity):
        msg = "Node '%s' can't be split to unknown source entity: %s" % (
            node.get_build_str(brief=False), entity)
        super(ErrorNodeSplitUnknownSource, self).__init__(msg)
class ErrorNoTargets(AttributeError):
    def __init__(self, node):
        msg = "Node targets are not built or set yet: %s" % (node,)
        super(ErrorNoTargets, self).__init__(msg)
class ErrorNoSrcTargets(Exception):
    def __init__(self, node, src_entity):
        msg = "Source '%s' targets are not built or set yet: %s" % (
            src_entity.get(), node)
        super(ErrorNoSrcTargets, self).__init__(msg)
class ErrorUnactualEntity(Exception):
    def __init__(self, node_entity, entity):
        msg = "Target entity is not actual: %s (%s), node: %s" %               (entity.name, type(entity), node_entity.get_build_str())
        super(ErrorUnactualEntity, self).__init__(msg)
class ErrorNodeUnknownSource(Exception):
    def __init__(self, src_entity):
        msg = "Unknown source entity: %s (%s)" % (src_entity, type(src_entity))
        super(ErrorNodeUnknownSource, self).__init__(msg)
@event_status
def event_node_rebuild_reason(settings, reason):
    if isinstance(reason, NodeRebuildReason):
        msg = reason.get_message(settings.brief)
    else:
        msg = str(reason)
    log_debug(msg)
class NodeRebuildReason (Exception):
    __slots__ = (
        'builder',
        'sources',
    )
    def __init__(self, node_entity):
        self.builder = node_entity.builder
        self.sources = node_entity.source_entities
    def get_node_name(self, brief):
        return self.builder.get_trace(self.sources, brief=brief)
    def __str__(self):
        return self.get_message(False)
    def get_message(self, brief):
        node_name = self.get_node_name(brief)
        description = self.get_description(brief)
        return "%s\nRebuilding the node: %s" % (description, node_name)
    def get_description(self, brief):
        return "Node's state is changed."
class NodeRebuildReasonAlways (NodeRebuildReason):
    def get_description(self, brief):
        return "Node is marked to rebuild always."
class NodeRebuildReasonNew (NodeRebuildReason):
    def get_description(self, brief):
        return "Node's previous state has not been found."
class NodeRebuildReasonSignature (NodeRebuildReason):
    def get_description(self, brief):
        return "Node`s signature has been changed "                "(sources, builder parameters or dependencies were changed)."
class NodeRebuildReasonNoTargets (NodeRebuildReason):
    def get_description(self, brief):
        return "Unknown Node's targets."
class NodeRebuildReasonImplicitDep (NodeRebuildReason):
    __slots__ = (
        'entity',
    )
    def __init__(self, node_entity, idep_entity=None):
        super(NodeRebuildReasonImplicitDep, self).__init__(node_entity)
        self.entity = idep_entity
    def get_description(self, brief):
        dep = (" '%s'" % self.entity) if self.entity is not None else ""
        return "Node's implicit dependency%s has changed, " % (dep,)
class NodeRebuildReasonTarget (NodeRebuildReason):
    __slots__ = (
        'entity',
    )
    def __init__(self, node_entity, target_entity):
        super(NodeRebuildReasonTarget, self).__init__(node_entity)
        self.entity = target_entity
    def get_description(self, brief):
        return "Node's target '%s' has changed." % (self.entity,)
@pickleable
class NodeEntity (EntityBase):
    __slots__ = (
        'name',
        'signature',
        'builder',
        'source_entities',
        'dep_entities',
        'target_entities',
        'itarget_entities',
        'idep_entities',
        'idep_keys',
    )
    def __new__(cls,
                name=NotImplemented,
                signature=NotImplemented,
                targets=None,
                itargets=None,
                idep_keys=None,
                builder=None,
                source_entities=None,
                dep_entities=None):
        self = super(NodeEntity, cls).__new__(cls, name, signature)
        if targets is not None:
            self.target_entities = targets
            self.itarget_entities = itargets
            self.idep_keys = idep_keys
        else:
            self.builder = builder
            self.source_entities = source_entities
            self.dep_entities = dep_entities
        return self
    def get(self):
        return self.name
    def __getnewargs__(self):
        return (self.name,
                self.signature,
                self.target_entities,
                self.itarget_entities,
                self.idep_keys)
    def get_targets(self):
        builder = self.builder
        targets = builder.get_target_entities(self.source_entities)
        if not targets:
            return ()
        return tuple(builder.make_entities(targets))
    def get_name(self):
        hash_sum = new_hash(self.builder.name)
        name_entities = self.target_entities
        if not name_entities:
            name_entities = self.source_entities
        names = sorted(entity.id for entity in name_entities)
        for name in names:
            hash_sum.update(name)
        return hash_sum.digest()
    def get_signature(self):
        builder_signature = self.builder.signature
        if builder_signature is None:
            return None
        hash_sum = new_hash(builder_signature)
        for entity in self.dep_entities:
            ent_sign = entity.signature
            if not ent_sign:
                return None
            hash_sum.update(entity.id)
            hash_sum.update(ent_sign)
        for entity in self.source_entities:
            entity_signature = entity.signature
            if entity_signature is None:
                return None
            hash_sum.update(entity_signature)
        return hash_sum.digest()
    def get_build_str(self):
        try:
            targets = getattr(self, 'target_entities', None)
            return self.builder.get_trace(self.source_entities, targets)
        except Exception as ex:
            log_error(ex)
        return str(self)  # Can't do much, show as a raw pointer
    def __getattr__(self, attr):
        if attr == 'target_entities':
            self.target_entities = targets = self.get_targets()
            return targets
        return super(NodeEntity, self).__getattr__(attr)
    _ACTUAL_IDEPS_CACHE = {}
    def _get_ideps(self, vfile, idep_keys,
                   ideps_cache_get=_ACTUAL_IDEPS_CACHE.__getitem__,
                   ideps_cache_set=_ACTUAL_IDEPS_CACHE.__setitem__):
        entities = vfile.find_entities_by_key(idep_keys)
        if entities is None:
            raise NodeRebuildReasonImplicitDep(self)
        for i, entity in enumerate(entities):
            entity_id = entity.id
            try:
                entities[i] = ideps_cache_get(entity_id)
            except KeyError:
                actual_entity = entity.get_actual()
                ideps_cache_set(entity_id, actual_entity)
                if entity is not actual_entity:
                    vfile.update_entity(actual_entity)
                    raise NodeRebuildReasonImplicitDep(self, entity)
        return entities
    def _save_ideps(self, vfile,
                    _actual_ideps_cache_set=_ACTUAL_IDEPS_CACHE.setdefault):
        entities = []
        for entity in self.idep_entities:
            entity_id = entity.id
            cached_entity = _actual_ideps_cache_set(entity_id, entity)
            if cached_entity is entity:
                if entity.signature is None:
                    raise ErrorUnactualEntity(self, entity)
            entities.append(cached_entity)
        keys = vfile.add_entities(entities)
        self.idep_entities = entities
        self.idep_keys = keys
    def check_actual(self, vfile, explain):
        try:
            previous = vfile.find_node_entity(self)
            if previous is None:
                raise NodeRebuildReasonNew(self)
            if not self.signature:
                raise NodeRebuildReasonAlways(self)
            if self.signature != previous.signature:
                raise NodeRebuildReasonSignature(self)
            ideps = self._get_ideps(vfile, previous.idep_keys)
            target_entities = previous.target_entities
            if target_entities is None:
                raise NodeRebuildReasonNoTargets(self)
            unactual_target = self.builder.check_actual(target_entities)
            if unactual_target is not None:
                raise NodeRebuildReasonTarget(self, unactual_target)
        except NodeRebuildReason as reason:
            if explain:
                event_node_rebuild_reason(reason)
            return False
        self.target_entities = target_entities
        self.itarget_entities = previous.itarget_entities
        self.idep_entities = ideps
        return True
    def save(self, vfile):
        for entity in self.target_entities:
            if entity.signature is None:
                raise ErrorUnactualEntity(self, entity)
        self._save_ideps(vfile)
        vfile.add_node_entity(self)
    def clear(self, vfile):
        """
        Clear produced target entities
        """
        self.idep_entities = tuple()
        node_entity = vfile.find_node_entity(self)
        if node_entity is None:
            self.itarget_entities = tuple()
        else:
            targets = node_entity.target_entities
            itargets = node_entity.itarget_entities
            if targets:
                self.target_entities = targets
            else:
                self.target_entities = tuple()
            if itargets:
                self.itarget_entities = itargets
            else:
                self.itarget_entities = tuple()
        try:
            self.builder.clear(self.target_entities, self.itarget_entities)
        except Exception:
            pass
    def add_targets(self, values, tags=None):
        self.target_entities.extend(
            self.builder.make_entities(values, tags))
    def add_target_files(self, values, tags=None):
        self.target_entities.extend(
            self.builder.make_file_entities(values, tags))
    def add_target_entity(self, entity):
        self.target_entities.append(entity)
    def add_target_entities(self, entities):
        self.target_entities.extend(entities)
    def add_side_effects(self, entities, tags=None):
        self.itarget_entities.extend(
            self.builder.make_entities(entities, tags))
    def add_side_effect_files(self, entities, tags=None):
        self.itarget_entities.extend(
            self.builder.make_file_entities(entities, tags))
    def add_side_effect_entity(self, entity):
        self.itarget_entities.append(entity)
    def add_side_effect_entities(self, entities):
        self.itarget_entities.extend(entities)
    def add_implicit_deps(self, entities, tags=None):
        self.idep_entities.extend(
            self.builder.make_entities(entities, tags))
    def add_implicit_dep_files(self, entities, tags=None):
        self.idep_entities.extend(
            self.builder.make_file_entities(entities, tags))
    def add_implicit_dep_entity(self, entity):
        self.idep_entities.append(entity)
    def add_implicit_dep_entities(self, entities):
        self.idep_entities.extend(entities)
class _NodeBatchTargets (object):
    def __init__(self, node_entities_map):
        self.node_entities_map = node_entities_map
    def __getitem__(self, source):
        try:
            return self.node_entities_map[source]
        except KeyError:
            raise ErrorNodeUnknownSource(source)
class NodeFilter (object):
    __slots__ = (
        'node',
        'node_attribute',
    )
    def __init__(self, node, node_attribute='target_entities'):
        self.node = node
        self.node_attribute = node_attribute
    def get_node(self):
        node = self.node
        while isinstance(node, NodeFilter):
            node = node.node
        return node
    def __iter__(self):
        raise TypeError()
    def __getitem__(self, item):
        return NodeIndexFilter(self, item)
    def get(self):
        entities = self.get_entities()
        if len(entities) == 1:
            return entities[0]
        return entities
    def get_entities(self):
        node = self.node
        if isinstance(node, NodeFilter):
            entities = node.get_entities()
        else:
            entities = getattr(node, self.node_attribute)
        return entities
class NodeTagsFilter(NodeFilter):
    __slots__ = (
        'tags',
    )
    def __init__(self, node, tags, node_attribute='target_entities'):
        super(NodeTagsFilter, self).__init__(node, node_attribute)
        self.tags = frozenset(to_sequence(tags))
    def get_entities(self):
        entities = super(NodeTagsFilter, self).get_entities()
        tags = self.tags
        return tuple(entity for entity in entities
                     if entity.tags and (entity.tags & tags))
class NodeIndexFilter(NodeFilter):
    __slots__ = (
        'index',
    )
    def __init__(self, node, index, node_attribute='target_entities'):
        super(NodeIndexFilter, self).__init__(node, node_attribute)
        self.index = index
    def get_entities(self):
        entities = super(NodeIndexFilter, self).get_entities()
        try:
            return to_sequence(entities[self.index])
        except IndexError:
            return tuple()
class NodeDirNameFilter(NodeFilter):
    def get_entities(self):
        entities = super(NodeDirNameFilter, self).get_entities()
        return tuple(SimpleEntity(os.path.dirname(entity.get()))
                     for entity in entities)
class NodeBaseNameFilter(NodeFilter):
    def get_entities(self):
        entities = super(NodeBaseNameFilter, self).get_entities()
        return tuple(SimpleEntity(os.path.basename(entity.get()))
                     for entity in entities)
class Node (object):
    __slots__ = (
        'builder',
        'options',
        'cwd',
        'initiated',
        'depends_called',
        'replace_called',
        'split_called',
        'check_actual',
        'node_entities',
        'node_entities_map',
        'sources',
        'source_entities',
        'dep_nodes',
        'dep_entities',
        'target_entities',
        'itarget_entities',
        'idep_entities',
    )
    def __init__(self, builder, sources, cwd=None):
        self.builder = builder
        self.options = getattr(builder, 'options', None)
        if cwd is None:
            self.cwd = os.path.abspath(os.getcwd())
        else:
            self.cwd = cwd
        self.initiated = False
        self.depends_called = False
        self.replace_called = False
        self.split_called = False
        self.check_actual = self._not_actual
        self.sources = tuple(to_sequence(sources))
        self.dep_nodes = set()
        self.dep_entities = []
    def shrink(self):
        self.cwd = None
        self.dep_nodes = None
        self.sources = None
        self.node_entities = None
        self.node_entities_map = None
        self.dep_entities = None
        self.check_actual = None
        self.builder = None
        self.options = None
    def skip(self):
        self.shrink()
        self.initiated = True
        self.depends_called = True
        self.replace_called = True
        self.split_called = True
        self.target_entities =             self.itarget_entities =             self.idep_entities = tuple()
    def depends(self, dependencies):
        dep_nodes = self.dep_nodes
        dep_entities = self.dep_entities
        for entity in to_sequence(dependencies):
            if isinstance(entity, Node):
                dep_nodes.add(entity)
            elif isinstance(entity, NodeFilter):
                dep_nodes.add(entity.get_node())
            elif isinstance(entity, EntityBase):
                dep_entities.append(entity)
            else:
                raise ErrorNodeDependencyInvalid(entity)
    def __getattr__(self, attr):
        if attr in ['target_entities', 'itarget_entities', 'idep_entities']:
            raise ErrorNoTargets(self)
        raise AttributeError("Node has not attribute '%s'" % (attr,))
    def _set_source_entities(self):
        entities = []
        make_entity = self.builder.make_entity
        for src in self.sources:
            if isinstance(src, Node):
                entities += src.target_entities
            elif isinstance(src, NodeFilter):
                entities += src.get_entities()
            elif isinstance(src, EntityBase):
                entities.append(src)
            else:
                entity = make_entity(src)
                entities.append(entity)
        self.sources = None
        self.source_entities = entities
    def _update_dep_entities(self):
        dep_nodes = self.dep_nodes
        if not dep_nodes:
            return
        dep_entities = self.dep_entities
        for node in dep_nodes:
            target_entities = node.target_entities
            if target_entities:
                dep_entities.extend(target_entities)
        dep_nodes.clear()
        dep_entities.sort(key=operator.attrgetter('id'))
    def initiate(self, chdir=os.chdir):
        if self.initiated:
            if self.sources:
                self._set_source_entities()
        else:
            chdir(self.cwd)
            self.builder = self.builder.initiate()
            self._set_source_entities()
            self._update_dep_entities()
            self.initiated = True
    def build_depends(self, chdir=os.chdir):
        if self.depends_called:
            return None
        self.depends_called = True
        chdir(self.cwd)
        nodes = self.builder.depends(self.options, self.source_entities)
        return nodes
    def build_replace(self, chdir=os.chdir):
        if self.replace_called:
            return None
        self.replace_called = True
        chdir(self.cwd)
        sources = self.builder.replace(self.options, self.source_entities)
        if sources is None:
            return None
        self.sources = tuple(to_sequence(sources))
        return self.get_source_nodes()
    def _split_batch(self, vfile, explain):
        builder = self.builder
        dep_entities = self.dep_entities
        node_entities = []
        not_actual_nodes = {}
        not_actual_sources = []
        for src in self.source_entities:
            node_entity = NodeEntity(builder=builder,
                                     source_entities=(src,),
                                     dep_entities=dep_entities)
            if not node_entity.check_actual(vfile, explain):
                not_actual_nodes[src] = node_entity
                not_actual_sources.append(src)
            node_entities.append(node_entity)
        self.node_entities = node_entities
        if not not_actual_nodes:
            return None
        groups = builder.split_batch(not_actual_sources)
        if not groups:
            groups = not_actual_sources
        split_nodes = []
        for group in groups:
            group = tuple(to_sequence(group))
            node_entities = tuple(not_actual_nodes[src] for src in group)
            node = self._split(group, node_entities)
            node.node_entities_map = not_actual_nodes
            split_nodes.append(node)
        return split_nodes
    def build_split(self, vfile, explain):
        if self.split_called:
            return None
        self.split_called = True
        self.check_actual = self._split_actual
        builder = self.builder
        dep_entities = self.dep_entities
        if builder.is_batch():
            return self._split_batch(vfile, explain)
        sources = self.source_entities
        groups = self.builder.split(sources)
        if (not groups) or (len(groups) < 2):
            node_entity = NodeEntity(builder=builder,
                                     source_entities=sources,
                                     dep_entities=dep_entities)
            if not node_entity.check_actual(vfile, explain):
                self.check_actual = self._not_actual
            self.node_entities = (node_entity,)
            return None
        node_entities = []
        split_nodes = []
        for group in groups:
            group = to_sequence(group)
            node_entity = NodeEntity(builder=builder,
                                     source_entities=group,
                                     dep_entities=dep_entities)
            if not node_entity.check_actual(vfile, explain):
                node = self._split(group, (node_entity,))
                split_nodes.append(node)
            node_entities.append(node_entity)
        self.node_entities = node_entities
        return split_nodes
    def _split(self, source_entities, node_entities):
        other = object.__new__(self.__class__)
        other.builder = self.builder
        other.dep_nodes = ()
        other.sources = ()
        other.source_entities = source_entities
        other.node_entities = node_entities
        other.initiated = True
        other.depends_called = True
        other.replace_called = True
        other.split_called = True
        other.check_actual = self._not_actual
        return other
    def prebuild(self):
        dep_nodes = self.build_depends()
        if dep_nodes:
            return dep_nodes
        source_nodes = self.build_replace()
        return source_nodes
    def _reset_targets(self):
        for node_entity in self.node_entities:
            node_entity.target_entities = []
            node_entity.itarget_entities = []
            node_entity.idep_entities = []
    def _populate_targets(self):
        node_entities = self.node_entities
        if len(node_entities) == 1:
            node_entity = node_entities[0]
            self.target_entities = node_entity.target_entities
            self.itarget_entities = node_entity.itarget_entities
            self.idep_entities = node_entity.idep_entities
        else:
            targets = []
            itargets = []
            ideps = []
            for node_entity in node_entities:
                targets += node_entity.target_entities
                itargets += node_entity.itarget_entities
                ideps += node_entity.idep_entities
            self.target_entities = targets
            self.itarget_entities = itargets
            self.idep_entities = ideps
    def _check_actual(self, vfile, explain):
        for node_entity in self.node_entities:
            if not node_entity.check_actual(vfile, explain):
                return False
        self._populate_targets()
        self.check_actual = self._actual
        return True
    def _split_actual(self,  vfile, explain):
        self._populate_targets()
        self.check_actual = self._actual
        return True
    @staticmethod
    def _actual(vfile, explain):
        return True
    @staticmethod
    def _not_actual(vfile, explain):
        return False
    def recheck_actual(self):
        self.check_actual = self._check_actual
    def build(self):
        builder = self.builder
        self._reset_targets()
        if builder.is_batch():
            targets = _NodeBatchTargets(self.node_entities_map)
            output = builder.build_batch(self.source_entities, targets)
        else:
            targets = self.node_entities
            output = builder.build(self.source_entities, targets[0])
        self._populate_targets()
        return output
    def save(self, vfile):
        for node_entity in self.node_entities:
            node_entity.save(vfile)
    def save_failed(self, vfile):
        node_entities = self.node_entities
        if len(node_entities) < 2:
            return
        for node_entity in node_entities:
            if node_entity.target_entities:
                node_entity.save(vfile)
    def _clear_split(self):
        builder = self.builder
        source_entities = self.source_entities
        if builder.is_batch():
            groups = source_entities
        else:
            groups = self.builder.split(source_entities)
            if not groups:
                groups = [source_entities]
        node_entities = []
        for group in groups:
            group = to_sequence(group)
            node_entity = NodeEntity(builder=builder,
                                     source_entities=group,
                                     dep_entities=())
            node_entities.append(node_entity)
        self.node_entities = node_entities
    def clear(self, vfile):
        self._clear_split()
        node_entities = []
        for node_entity in self.node_entities:
            node_entity.clear(vfile)
            node_entities.append(node_entity)
        self._populate_targets()
        return node_entities
    def get_weight(self):
        return self.builder.get_weight(self.source_entities)
    def get_names(self):
        return (entity.name for entity in self.node_entities)
    def get_names_and_signatures(self):
        return ((entity.name, entity.signature)
                for entity in self.node_entities)
    def get_dep_nodes(self):
        return self.dep_nodes
    def get_sources(self):
        return tuple(src.get() for src in self.get_source_entities())
    def get_source_entities(self):
        return self.source_entities
    def get_source_nodes(self):
        nodes = []
        for src in self.sources:
            if isinstance(src, Node):
                nodes.append(src)
            elif isinstance(src, NodeFilter):
                nodes.append(src.get_node())
        return nodes
    def is_built(self):
        return self.builder is None
    def at(self, tags):
        return NodeTagsFilter(self, tags)
    def __iter__(self):
        raise TypeError()
    def __getitem__(self, item):
        return NodeIndexFilter(self, item)
    def __filter(self, node_attribute, tags):
        if tags is None:
            return NodeFilter(self, node_attribute)
        return NodeTagsFilter(self, tags, node_attribute)
    def filter_sources(self, tags=None):
        return self.__filter('source_entities', tags)
    def filter_side_effects(self, tags=None):
        return self.__filter('itarget_entities', tags)
    def filter_implicit_dependencies(self, tags=None):
        return self.__filter('idep_entities', tags)
    def filter_dependencies(self, tags=None):
        return self.__filter('dep_entities', tags)
    def get(self):
        targets = self.get_target_entities()
        if len(targets) == 1:
            return targets[0].get()
        return tuple(target.get() for target in targets)
    def get_target_entities(self):
        return self.target_entities
    def get_side_effect_entities(self):
        return self.itarget_entities
    def get_build_str(self, brief=True):
        try:
            targets = getattr(self, 'target_entities', None)
            return self.builder.get_trace(self.source_entities, targets, brief)
        except Exception as ex:
            if 'BuilderInitiator' not in str(ex):
                raise
        return str(self)  # show as a raw pointer
    def print_sources(self):    # noqa
        result = []
        sources = self.sources
        if not sources:
            sources = self.source_entities
        for src in sources:
            if isinstance(src, EntityBase):
                result.append(src.get())
            elif isinstance(src, Node):
                targets = getattr(src, 'target_entities', None)
                if targets is not None:
                    result += (target.get() for target in targets)
                else:
                    result.append(src)
            elif isinstance(src, NodeFilter):
                try:
                    targets = src.get_entities()
                except AttributeError:
                    continue
                if targets is not None:
                    result += (target.get() for target in targets)
                else:
                    result.append(src)
            else:
                result.append(src)
        sources_str = ', '.join(map(str, result))
        log_info("node '%s' sources: %s", self, sources_str)
    def print_targets(self):
        targets = [t.get() for t in getattr(self, 'target_entities', [])]
        log_info("node '%s' targets: %s", self, targets)
@event_warning
def event_build_target_twice(settings, entity, node1):
    log_warning("Target '%s' is built twice. The last time built by: '%s' ",
                entity.name, node1.get_build_str(settings.brief))
@event_error
def event_failed_node(settings, node, error):
    msg = node.get_build_str(settings.brief)
    msg += '\n\n%s\n' % (error,)
    log_error(msg)
@event_status
def event_node_building(settings, node):
    pass
@event_status
def event_node_building_finished(settings, node, builder_output, progress):
    msg = node.get_build_str(settings.brief)
    if settings.with_output and builder_output:
        msg += '\n'
        if builder_output:
            msg += builder_output
            msg += '\n'
    msg = "(%s) %s" % (progress, msg)
    log_info(msg)
@event_status
def event_node_building_failed(settings, node, error):
    pass
@event_status
def event_node_removed(settings, node, progress):
    msg = node.get_build_str(settings.brief)
    if msg:
        log_info("(%s) Removed: %s", progress, msg)
class ErrorNodeDependencyCyclic(Exception):
    def __init__(self, node, deps):
        msg = "Node '%s' (%s) has a cyclic dependency: %s" % (
            node, node.get_build_str(True), deps)
        super(ErrorNodeDependencyCyclic, self).__init__(msg)
class ErrorNodeUnknown(Exception):
    def __init__(self, node):
        msg = "Unknown node '%s'" % (node, )
        super(ErrorNodeUnknown, self).__init__(msg)
class ErrorNodeSignatureDifferent(Exception):
    def __init__(self, node, other_node):
        msg = "Two similar nodes have different signatures"               "(sources, builder parameters or dependencies): [%s], [%s]" %               (node.get_build_str(brief=False),
               other_node.get_build_str(brief=False))
        super(ErrorNodeSignatureDifferent, self).__init__(msg)
class ErrorNodeDuplicateNames(Exception):
    def __init__(self, node):
        msg = "Batch node has duplicate targets: %s" %               (node.get_build_str(brief=False))
        super(ErrorNodeDuplicateNames, self).__init__(msg)
class ErrorNodeDependencyUnknown(Exception):
    def __init__(self, node, dep_node):
        msg = "Unable to add dependency to node '%s' from node '%s'" % (
            node, dep_node)
        super(ErrorNodeDependencyUnknown, self).__init__(msg)
class InternalErrorRemoveNonTailNode(Exception):
    def __init__(self, node):
        msg = "Removing non-tail node: %s" % (node,)
        super(InternalErrorRemoveNonTailNode, self).__init__(msg)
class InternalErrorRemoveUnknownTailNode(Exception):
    def __init__(self, node):
        msg = "Remove unknown tail node: : %s" % (node,)
        super(InternalErrorRemoveUnknownTailNode, self).__init__(msg)
class _NodesTree (object):
    __slots__ = (
        'node2deps',
        'dep2nodes',
        'tail_nodes',
    )
    def __init__(self):
        self.node2deps = {}
        self.dep2nodes = {}
        self.tail_nodes = set()
    def __len__(self):
        return len(self.node2deps)
    def get_nodes(self):
        return frozenset(self.node2deps)
    def __has_cycle(self, node, new_deps):
        if node in new_deps:
            return True
        deps = set(new_deps)
        node2deps = self.node2deps
        while deps:
            dep = deps.pop()
            dep_deps = node2deps[dep]
            if node in dep_deps:
                return True
            deps |= dep_deps
        return False
    def _depends(self, node, deps):
        node2deps = self.node2deps
        dep2nodes = self.dep2nodes
        try:
            current_node_deps = node2deps[node]
            deps = set(dep for dep in deps if not dep.is_built())
            new_deps = deps - current_node_deps
            if not new_deps:
                return
            if self.__has_cycle(node, new_deps):
                raise ErrorNodeDependencyCyclic(node, new_deps)
            self.tail_nodes.discard(node)
            current_node_deps.update(new_deps)
            for dep in new_deps:
                dep2nodes[dep].add(node)
        except KeyError as dep_node:
            raise ErrorNodeDependencyUnknown(node, dep_node.args[0])
    def add(self, nodes):
        for node in nodes:
            if node not in self.node2deps:
                self.node2deps[node] = set()
                self.dep2nodes[node] = set()
                self.tail_nodes.add(node)
                node_srcnodes = node.get_source_nodes()
                node_depnodes = node.get_dep_nodes()
                self.add(node_srcnodes)
                self.add(node_depnodes)
                self._depends(node, node_srcnodes)
                self._depends(node, node_depnodes)
    def depends(self, node, deps):
        self.add(deps)
        self._depends(node, deps)
    def remove_tail(self, node):
        node2deps = self.node2deps
        try:
            deps = node2deps.pop(node)
            if deps:
                raise InternalErrorRemoveNonTailNode(node)
        except KeyError as ex:
            raise InternalErrorRemoveUnknownTailNode(ex.args[0])
        tail_nodes = self.tail_nodes
        for dep in self.dep2nodes.pop(node):
            d = node2deps[dep]
            d.remove(node)
            if not d:
                tail_nodes.add(dep)
    def filter_unknown_deps(self, deps):
        return [dep for dep in deps if dep in self.node2deps]
    def pop_tails(self):
        tails = self.tail_nodes
        self.tail_nodes = set()
        return tails
    def __get_all_nodes(self, nodes):
        nodes = set(nodes)
        all_nodes = set(nodes)
        node2deps = self.node2deps
        while nodes:
            node = nodes.pop()
            try:
                deps = node2deps[node] - all_nodes
            except KeyError as node:
                raise ErrorNodeUnknown(node.args[0])
            all_nodes.update(deps)
            nodes.update(deps)
        return all_nodes
    def shrink_to(self, nodes):
        node2deps = self.node2deps
        dep2nodes = self.dep2nodes
        ignore_nodes = set(node2deps) - self.__get_all_nodes(nodes)
        self.tail_nodes -= ignore_nodes
        for node in ignore_nodes:
            del node2deps[node]
            del dep2nodes[node]
        for dep_nodes in dep2nodes.values():
            dep_nodes.difference_update(ignore_nodes)
    def self_test(self):
        if set(self.node2deps) != set(self.dep2nodes):
            raise AssertionError("Not all deps are added")
        all_dep_nodes = set()
        for node in self.dep2nodes:
            if node not in self.node2deps:
                raise AssertionError("Missed node: %s" % (node,))
            node_deps = self.node2deps[node]
            if node_deps:
                if node in self.tail_nodes:
                    raise AssertionError("Invalid tail node: %s" % (node,))
            all_dep_nodes |= node_deps
            for dep in node_deps:
                if node not in self.dep2nodes[dep]:
                    raise AssertionError(
                        "node not in self.dep2nodes[dep]: "
                        "dep: %s, node: %s" % (dep, node))
        if all_dep_nodes - set(self.dep2nodes):
            raise AssertionError("Not all deps are added")
class _VFiles(object):
    __slots__ = (
        'names',
        'handles',
        'use_sqlite',
        'force_lock',
    )
    def __init__(self, use_sqlite=False, force_lock=False):
        self.handles = {}
        self.names = {}
        self.use_sqlite = use_sqlite
        self.force_lock = force_lock
    def __iter__(self):
        raise TypeError()
    def __getitem__(self, builder):
        builder_name = builder.name
        try:
            vfilename = self.names[builder_name]
        except KeyError:
            vfilename = os.path.join(builder.get_build_dir(), '.aql.db')
            self.names[builder_name] = vfilename
        try:
            return self.handles[vfilename]
        except KeyError:
            vfile = EntitiesFile(
                vfilename, use_sqlite=self.use_sqlite, force=self.force_lock)
            self.handles[vfilename] = vfile
            return vfile
    def close(self):
        for vfile in self.handles.values():
            vfile.close()
        self.handles.clear()
        self.names.clear()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, backtrace):
        self.close()
def _build_node(node):
    event_node_building(node)
    out = node.build()
    if out:
        try:
            out = out.strip()
        except Exception:
            pass
    return out
def _get_module_nodes(node, module_cache, node_cache):
    try:
        return module_cache[node]
    except KeyError:
        pass
    result = set((node,))
    try:
        src_nodes = node_cache[node]
    except KeyError:
        node_cache[node] = src_nodes = frozenset(node.get_source_nodes())
    for src in src_nodes:
        result.update(_get_module_nodes(src, module_cache, node_cache))
    module_cache[node] = result
    return result
def _get_leaf_nodes(nodes, exclude_nodes, node_cache):
    leafs = set()
    for node in nodes:
        if node_cache[node].issubset(exclude_nodes):
            leafs.add(node)
    return leafs
class _NodeLocker(object):
    __slots__ = (
        'node2deps',
        'dep2nodes',
        'locked_nodes',
        'unlocked_nodes',
    )
    def __init__(self):
        self.node2deps = {}
        self.dep2nodes = {}
        self.locked_nodes = {}
        self.unlocked_nodes = []
    def sync_modules(self, nodes, module_cache=None, node_cache=None):
        if module_cache is None:
            module_cache = {}
        if node_cache is None:
            node_cache = {}
        for node1, node2 in itertools.product(nodes, nodes):
            if node1 is not node2:
                self.__add_modules(node1, node2, module_cache, node_cache)
    def __add_modules(self, node1, node2, module_cache, node_cache):
        node1_sources = _get_module_nodes(node1, module_cache, node_cache)
        node2_sources = _get_module_nodes(node2, module_cache, node_cache)
        common = node1_sources & node2_sources
        node1_sources -= common
        node2_sources -= common
        leafs1 = _get_leaf_nodes(node1_sources, common, node_cache)
        leafs2 = _get_leaf_nodes(node2_sources, common, node_cache)
        for leaf in leafs1:
            self.__add(leaf, node2_sources)
        for leaf in leafs2:
            self.__add(leaf, node1_sources)
    def sync(self, nodes):
        for node in nodes:
            node_deps = self.__add(node, nodes)
            node_deps.remove(node)
    def __add(self, node, deps):
        try:
            node_set = self.node2deps[node]
        except KeyError:
            node_set = set()
            self.node2deps[node] = node_set
        node_set.update(deps)
        for dep in deps:
            if dep is not node:
                try:
                    dep_set = self.dep2nodes[dep]
                except KeyError:
                    dep_set = set()
                    self.dep2nodes[dep] = dep_set
                dep_set.add(node)
        return node_set
    def lock(self, node):
        deps = self.node2deps.get(node, None)
        if not deps:
            return True
        locked_nodes = self.locked_nodes
        for dep in deps:
            if dep in locked_nodes:
                locked_nodes[dep].add(node)
                return False
        self.locked_nodes[node] = set()
        return True
    def unlock(self, node):
        deps = self.node2deps.pop(node, ())
        nodes = self.dep2nodes.pop(node, ())
        if not deps and not nodes:
            return
        for dep in deps:
            self.dep2nodes[dep].remove(node)
        for dep in nodes:
            self.node2deps[dep].remove(node)
        unlocked_nodes = self.locked_nodes.pop(node, None)
        if not unlocked_nodes:
            return
        self.unlocked_nodes.extend(unlocked_nodes)
    def pop_unlocked(self):
        unlocked_nodes = self.unlocked_nodes
        self.unlocked_nodes = []
        return unlocked_nodes
    def self_test(self):    # noqa
        for node, deps in self.node2deps.items():
            if node in deps:
                raise AssertionError("Node depends from itself: %s" % (node,))
            for dep in deps:
                if node not in self.dep2nodes[dep]:
                    raise AssertionError(
                        "Dependency '%s' doesn't have node '%s'" %
                        (dep, node,))
        for node, deps in self.locked_nodes.items():
            for dep in deps:
                if node not in self.node2deps[dep]:
                    raise AssertionError(
                        "Locked node %s doesn't actually depend from node %s" %
                        (dep, node))
                if dep in self.unlocked_nodes:
                    raise AssertionError("Locked node %s is actually locked" %
                                         (dep,))
        for node in self.unlocked_nodes:
            if node not in self.node2deps:
                raise AssertionError("Unknown unlocked node %s" % (node,))
class _NodesBuilder (object):
    __slots__ = (
        'vfiles',
        'build_manager',
        'task_manager',
        'building_nodes',
        'expensive_nodes',
    )
    def __init__(self, build_manager,
                 jobs=0, keep_going=False, with_backtrace=True,
                 use_sqlite=False, force_lock=False):
        self.vfiles = _VFiles(use_sqlite=use_sqlite, force_lock=force_lock)
        self.building_nodes = {}
        self.expensive_nodes = set(build_manager._expensive_nodes)
        self.build_manager = build_manager
        tm = TaskManager()
        if self.expensive_nodes:
            tm.enable_expensive()
        if not keep_going:
            tm.disable_keep_going()
        if not with_backtrace:
            tm.disable_backtrace()
        tm.start(jobs)
        self.task_manager = tm
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, backtrace):
        self.close()
    def _add_building_node(self, node):
        conflicting_nodes = []
        building_nodes = self.building_nodes
        node_names = {}
        for name, signature in node.get_names_and_signatures():
            other = building_nodes.get(name, None)
            if other is None:
                if name in node_names:
                    raise ErrorNodeDuplicateNames(node)
                node_names[name] = (node, signature)
                continue
            other_node, other_signature = other
            if node is other_node:
                continue
            if other_signature != signature:
                raise ErrorNodeSignatureDifferent(node, other_node)
            conflicting_nodes.append(other_node)
        if conflicting_nodes:
            node.recheck_actual()
            self.build_manager.depends(node, conflicting_nodes)
            return False
        building_nodes.update(node_names)
        return True
    def _remove_building_node(self, node):
        building_nodes = self.building_nodes
        for name in node.get_names():
            del building_nodes[name]
    def is_building(self):
        return bool(self.building_nodes)
    def add_build_task(self, node):
        if node in self.expensive_nodes:
            self.task_manager.add_expensive_task(node, _build_node, node)
        else:
            task_priority = -node.get_weight()  # less is higher
            self.task_manager.add_task(task_priority, node, _build_node, node)
    def build_node(self, node):
        build_manager = self.build_manager
        explain = build_manager.explain
        if not build_manager.lock_node(node):
            return False
        if build_manager.skip_node(node):
            return True
        node.initiate()
        vfile = self.vfiles[node.builder]
        prebuit_nodes = node.prebuild()
        if prebuit_nodes:
            build_manager.depends(node, prebuit_nodes)
            return True
        split_nodes = node.build_split(vfile, explain)
        if split_nodes:
            if node in self.expensive_nodes:
                self.expensive_nodes.update(split_nodes)
            build_manager.depends(node, split_nodes)
            for split_node in split_nodes:
                self._add_building_node(split_node)
            return True
        if node.check_actual(vfile, explain):
            build_manager.actual_node(node)
            return True
        if not self._add_building_node(node):
            return False
        self.add_build_task(node)
        return False
    def build(self, nodes):
        node_tree_changed = False
        for node in nodes:
            if self.build_node(node):
                node_tree_changed = True
            if len(self.building_nodes) > 10:
                if self._get_finished_nodes(block=False):
                    node_tree_changed = True
        return self._get_finished_nodes(block=not node_tree_changed)
    def _get_finished_nodes(self, block=True):
        finished_tasks = self.task_manager.get_finished_tasks(block=block)
        vfiles = self.vfiles
        build_manager = self.build_manager
        for task in finished_tasks:
            node = task.task_id
            error = task.error
            self._remove_building_node(node)
            vfile = vfiles[node.builder]
            if error is None:
                node.save(vfile)
                build_manager.completed_node(node, task.result)
            else:
                node.save_failed(vfile)
                build_manager.failed_node(node, error)
        return finished_tasks or not block
    def clear(self, nodes):
        vfiles = self.vfiles
        build_manager = self.build_manager
        remove_entities = {}
        for node in nodes:
            node.initiate()
            prebuit_nodes = node.prebuild()
            if prebuit_nodes:
                build_manager.depends(node, prebuit_nodes)
                continue
            vfile = vfiles[node.builder]
            node_entities = node.clear(vfile)
            remove_entities.setdefault(vfile, []).extend(node_entities)
            build_manager.removed_node(node)
        for vfile, entities in remove_entities.items():
            vfile.remove_node_entities(entities)
    def close(self):
        try:
            self.task_manager.stop()
            self._get_finished_nodes(block=False)
        finally:
            self.vfiles.close()
class _NodeCondition (object):
    __slots__ = (
        'value',
        'op',
    )
    def __init__(self, condition, result=True):
        self.value = condition
        self.op = operator.truth if result else operator.__not__
    def get_node(self):
        value = self.value
        if isinstance(value, Node):
            return value
        elif isinstance(value, NodeFilter):
            return value.get_node()
        return None
    def get(self):
        value = simplify_value(self.value)
        return self.op(value)
    def __bool__(self):
        return self.get()
    def __nonzero__(self):
        return self.get()
class BuildManager (object):
    __slots__ = (
        '_nodes',
        '_built_targets',
        '_failed_nodes',
        '_node_locker',
        '_module_cache',
        '_node_cache',
        '_node_conditions',
        '_expensive_nodes',
        'completed',
        'actual',
        'skipped',
        'explain',
    )
    def __init__(self):
        self._nodes = _NodesTree()
        self._node_locker = None
        self._node_conditions = {}
        self._expensive_nodes = set()
        self.__reset()
    def __reset(self, explain=False):
        self._built_targets = {}
        self._failed_nodes = {}
        self._module_cache = {}
        self._node_cache = {}
        self.completed = 0
        self.actual = 0
        self.skipped = 0
        self.explain = explain
    def add(self, nodes):
        self._nodes.add(nodes)
    def depends(self, node, deps):
        self._nodes.depends(node, deps)
    def build_if(self, condition, nodes):
        if not isinstance(condition, _NodeCondition):
            condition = _NodeCondition(condition)
        cond_node = condition.get_node()
        if cond_node is not None:
            cond_node = (cond_node,)
        depends = self._nodes.depends
        set_node_condition = self._node_conditions.__setitem__
        for node in to_sequence(nodes):
            if cond_node is not None:
                depends(node, cond_node)
            set_node_condition(node, condition)
    def skip_if(self, condition, nodes):
        self.build_if(_NodeCondition(condition, False), nodes)
    def expensive(self, nodes):
        self._expensive_nodes.update(to_sequence(nodes))
    def module_depends(self, node, deps):
        module_cache = self._module_cache
        node_cache = self._node_cache
        module_nodes = _get_module_nodes(node, module_cache, node_cache)
        for dep in deps:
            dep_nodes = _get_module_nodes(dep, module_cache, node_cache)
            common = module_nodes & dep_nodes
            only_module_nodes = module_nodes - common
            leafs = _get_leaf_nodes(only_module_nodes, common, node_cache)
            for leaf in leafs:
                self._nodes.depends(leaf, (dep,))
    def sync(self, nodes, deep=False):
        node_locker = self._node_locker
        if node_locker is None:
            self._node_locker = node_locker = _NodeLocker()
        if deep:
            node_locker.sync_modules(
                nodes, self._module_cache, self._node_cache)
        else:
            node_locker.sync(nodes)
    def lock_node(self, node):
        node_locker = self._node_locker
        if node_locker is None:
            return True
        return node_locker.lock(node)
    def unlock_node(self, node):
        node_locker = self._node_locker
        if node_locker is not None:
            node_locker.unlock(node)
    def __len__(self):
        return len(self._nodes)
    def self_test(self):
        self._nodes.self_test()
        if self._node_locker is not None:
            self._node_locker.self_test()
    def get_next_nodes(self):
        tails = self._nodes.pop_tails()
        if not tails:
            node_locker = self._node_locker
            if node_locker is not None:
                return node_locker.pop_unlocked()
        return tails
    def skip_node(self, node):
        cond = self._node_conditions.pop(node, None)
        if (cond is None) or cond:
            return False
        self.unlock_node(node)
        self._nodes.remove_tail(node)
        self.skipped += 1
        node.skip()
        return True
    def actual_node(self, node):
        self.unlock_node(node)
        self._nodes.remove_tail(node)
        self.actual += 1
        node.shrink()
    def completed_node(self, node, builder_output):
        self._check_already_built(node)
        self.unlock_node(node)
        self._nodes.remove_tail(node)
        self.completed += 1
        event_node_building_finished(node, builder_output,
                                     self.get_progress_str())
        node.shrink()
    def failed_node(self, node, error):
        self.unlock_node(node)
        self._failed_nodes[node] = error
        event_node_building_failed(node, error)
    def removed_node(self, node):
        self._nodes.remove_tail(node)
        self.completed += 1
        event_node_removed(node, self.get_progress_str())
        node.shrink()
    def get_progress_str(self):
        done = self.completed + self.actual + self.skipped
        total = len(self._nodes) + done
        processed = done + len(self._failed_nodes)
        progress = "%s/%s" % (processed, total)
        return progress
    def close(self):
        self._nodes = _NodesTree()
        self._node_locker = None
        self._node_conditions = {}
    def _check_already_built(self, node):
        entities = node.get_target_entities()
        built_targets = self._built_targets
        for entity in entities:
            entity_sign = entity.signature
            other_entity_sign = built_targets.setdefault(
                entity.id, entity_sign)
            if other_entity_sign != entity_sign:
                event_build_target_twice(entity, node)
    def shrink(self, nodes):
        if not nodes:
            return
        self._nodes.shrink_to(nodes)
    def get_nodes(self):
        return self._nodes.get_nodes()
    def build(self, jobs, keep_going, nodes=None, explain=False,
              with_backtrace=True, use_sqlite=False, force_lock=False):
        self.__reset(explain=explain)
        self.shrink(nodes)
        with _NodesBuilder(self,
                           jobs,
                           keep_going,
                           with_backtrace,
                           use_sqlite=use_sqlite,
                           force_lock=force_lock) as nodes_builder:
            while True:
                tails = self.get_next_nodes()
                if not tails and not nodes_builder.is_building():
                    break
                if not nodes_builder.build(tails):
                    break
        return self.is_ok()
    def is_ok(self):
        return not bool(self._failed_nodes)
    def fails_count(self):
        return len(self._failed_nodes)
    def print_fails(self):
        for node, error in self._failed_nodes.items():
            event_failed_node(node, error)
    def print_build_state(self):
        log_info("Failed nodes: %s", len(self._failed_nodes))
        log_info("Skipped nodes: %s", self.skipped)
        log_info("Completed nodes: %s", self.completed)
        log_info("Actual nodes: %s", self.actual)
    def clear(self, nodes=None, use_sqlite=False, force_lock=False):
        self.__reset()
        self.shrink(nodes)
        with _NodesBuilder(self,
                           use_sqlite=use_sqlite,
                           force_lock=force_lock) as nodes_builder:
            while True:
                tails = self.get_next_nodes()
                if not tails:
                    break
                nodes_builder.clear(tails)
class WriteFileBuilder (Builder):
    NAME_ATTRS = ['target']
    def __init__(self, options, target, binary=False, encoding=None):
        self.binary = binary
        self.encoding = encoding
        self.target = self.get_target_path(target)
    def build(self, source_entities, targets):
        target = self.target
        with open_file(target,
                       write=True,
                       binary=self.binary,
                       encoding=self.encoding) as f:
            f.truncate()
            for src in source_entities:
                src = src.get()
                if self.binary:
                    if is_unicode(src):
                        src = encode_str(src, self.encoding)
                else:
                    if isinstance(src, (bytearray, bytes)):
                        src = decode_bytes(src, self.encoding)
                f.write(src)
        targets.add_target_files(target)
    def get_trace_name(self, source_entities, brief):
        return "Writing content"
    def get_target_entities(self, source_entities):
        return self.target
class CopyFilesBuilder (FileBuilder):
    NAME_ATTRS = ['target']
    SIGNATURE_ATTRS = ['basedir']
    def __init__(self, options, target, basedir=None):
        self.target = self.get_target_dir(target)
        sep = os.path.sep
        self.basedir = tuple(os.path.normcase(os.path.normpath(basedir)) + sep
                             for basedir in to_sequence(basedir))
    def __get_dst(self, file_path):
        for basedir in self.basedir:
            if file_path.startswith(basedir):
                filename = file_path[len(basedir):]
                dirname, filename = os.path.split(filename)
                dst_dir = os.path.join(self.target, dirname)
                return os.path.join(dst_dir, filename)
        filename = os.path.basename(file_path)
        return os.path.join(self.target, filename)
    def build_batch(self, source_entities, targets):
        for src_entity in source_entities:
            src = src_entity.get()
            dst = self.__get_dst(src)
            self.makedirs(os.path.dirname(dst))
            shutil.copyfile(src, dst)
            shutil.copymode(src, dst)
            targets[src_entity].add_targets(dst)
    def get_trace_name(self, source_entities, brief):
        return "Copy files"
    def get_target_entities(self, source_entities):
        get_dst = self.__get_dst
        return (get_dst(src.get()) for src in source_entities)
class CopyFileAsBuilder (FileBuilder):
    NAME_ATTRS = ['target']
    def __init__(self, options, target):
        self.target = self.get_target_path(target)
    def build(self, source_entities, targets):
        source = source_entities[0].get()
        target = self.target
        shutil.copyfile(source, target)
        shutil.copymode(source, target)
        targets.add_targets(target)
    def get_trace_name(self, source_entities, brief):
        return "Copy file"
    def get_target_entities(self, source_entities):
        return self.target
def _get_method_full_name(m):
    full_name = []
    mod = getattr(m, '__module__', None)
    if mod:
        full_name.append(mod)
    name = getattr(m, '__qualname__', None)
    if name:
        full_name.append(name)
    else:
        cls = getattr(m, 'im_class', None)
        if cls is not None:
            cls_name = getattr(cls, '__name__', None)
            if cls_name:
                full_name.append(cls_name)
        name = getattr(m, '__name__', None)
        if name:
            full_name.append(name)
    return '.'.join(full_name)
class ExecuteMethodBuilder (Builder):
    NAME_ATTRS = ('method_name',)
    SIGNATURE_ATTRS = ('args', 'kw')
    def __init__(self,
                 options,
                 method,
                 args,
                 kw,
                 single,
                 make_files,
                 clear_targets):
        self.method_name = _get_method_full_name(method)
        self.method = method
        self.args = args if args else []
        self.kw = kw if kw else {}
        if not clear_targets:
            self.clear = lambda target_entities, side_effect_entities: None
        if single:
            self.split = self.split_single
        if make_files:
            self.make_entity = self.make_file_entity
    def build(self, source_entities, targets):
        return self.method(self, source_entities, targets,
                           *self.args, **self.kw)
    def get_trace_name(self, source_entities, brief):
        name = self.method.__doc__
        if name:
            name = name.strip().split('\n')[0].strip()
        if not name:
            name = self.method_name
        if not brief:
            args = ''
            if self.args:
                args = ','.join(self.args)
            if self.kw:
                if args:
                    args += ','
                args += ','.join("%s=%s" % (k, v) for k, v in self.kw.items())
            if args:
                return "%s(%s)" % (name, args)
        return name
class ErrorDistCommandInvalid(Exception):
    def __init__(self, command):
        msg = "distutils command '%s' is not supported" % (command,)
        super(ErrorDistCommandInvalid, self).__init__(msg)
class DistBuilder (FileBuilder):
    NAME_ATTRS = ('target', 'command', 'formats')
    SIGNATURE_ATTRS = ('script_args', )
    def __init__(self, options, command, args, target):
        target = self.get_target_dir(target)
        script_args = [command]
        if command.startswith('bdist'):
            temp_dir = self.get_build_path()
            script_args += ['--bdist-base', temp_dir]
        elif command != 'sdist':
            raise ErrorDistCommandInvalid(command)
        args = self._get_args(args)
        script_args += args
        formats = self._get_formats(args, command)
        script_args += ['--dist-dir', target]
        self.command = command
        self.target = target
        self.script_args = script_args
        self.formats = formats
    @staticmethod
    def _get_args(args):
        if args:
            return args.split() if is_string(args) else to_sequence(args)
        return tuple()
    @staticmethod
    def _get_formats(args, command):
        if not command.startswith('bdist'):
            return None
        formats = set()
        for arg in args:
            if arg.startswith('--formats='):
                v = arg[len('--formats='):].split(',')
                formats.update(v)
            elif arg.startswith('--plat-name='):
                v = arg[len('--plat-name='):]
                formats.add(v)
        return formats
    def get_trace_name(self, source_entities, brief):
        return "distutils %s" % ' '.join(self.script_args)
    def build(self, source_entities, targets):
        script = source_entities[0].get()
        cmd = [sys.executable, script]
        cmd += self.script_args
        script_dir = os.path.dirname(script)
        out = self.exec_cmd(cmd, script_dir)
        return out
class ExecuteCommandBuilder (Builder):
    NAME_ATTRS = ('targets', 'cwd')
    def __init__(self, options, target=None, target_flag=None, cwd=None):
        self.targets = tuple(map(self.get_target_path, to_sequence(target)))
        self.target_flag = target_flag
        if cwd:
            cwd = self.get_target_dir(cwd)
        self.cwd = cwd
    def _get_cmd_targets(self):
        targets = self.targets
        prefix = self.target_flag
        if not prefix:
            return tuple(targets)
        prefix = prefix.lstrip()
        if not prefix:
            return tuple(targets)
        rprefix = prefix.rstrip()
        if prefix != rprefix:
            return tuple(itertools.chain(*((rprefix, target)
                                           for target in targets)))
        return tuple("%s%s" % (prefix, target) for target in targets)
    def build(self, source_entities, targets):
        cmd = tuple(src.get() for src in source_entities)
        cmd_targets = self._get_cmd_targets()
        if cmd_targets:
            cmd += cmd_targets
        out = self.exec_cmd(cmd, cwd=self.cwd)
        targets.add_target_files(self.targets)
        return out
    def get_target_entities(self, source_entities):
        return self.targets
    def get_trace_name(self, source_entities, brief):
        try:
            return source_entities[0]
        except Exception:
            return self.__class__.__name__
    def get_trace_sources(self, source_entities, brief):
        return source_entities[1:]
class ErrorBatchBuildCustomExt(Exception):
    def __init__(self, trace, ext):
        msg = "Custom extension '%s' is not supported "               "in batch building of node: %s" % (ext, trace)
        super(ErrorBatchBuildCustomExt, self).__init__(msg)
class ErrorBatchBuildWithPrefix(Exception):
    def __init__(self, trace, prefix):
        msg = "Filename prefix '%s' is not supported "               "in batch building of node: %s" % (prefix, trace)
        super(ErrorBatchBuildWithPrefix, self).__init__(msg)
class ErrorBatchBuildWithSuffix(Exception):
    def __init__(self, trace, suffix):
        msg = "Filename suffix '%s' is not supported "               "in batch building of node: %s" % (suffix, trace)
        super(ErrorBatchBuildWithSuffix, self).__init__(msg)
class ErrorBatchCompileWithCustomTarget(Exception):
    def __init__(self, trace, target):
        msg = "Explicit output target '%s' is not supported "               "in batch building of node: %s" % (target, trace)
        super(ErrorBatchCompileWithCustomTarget, self).__init__(msg)
class ErrorCompileWithCustomTarget(Exception):
    def __init__(self, trace, target):
        msg = "Compile several source files using "               "the same target '%s' is not supported: %s" % (target, trace)
        super(ErrorCompileWithCustomTarget, self).__init__(msg)
def _add_prefix(prefix, values):
    prefix = prefix.lstrip()
    if not prefix:
        return values
    if prefix[-1] == ' ':
        prefix = prefix.rstrip()
        return tuple(itertools.chain(*itertools.product((prefix,), values)))
    return tuple("%s%s" % (prefix, value) for value in values)
def _add_ixes(prefix, suffix, values):
    prefix = prefix.lstrip()
    suffix = suffix.strip()
    sep_prefix = prefix and (prefix[-1] == ' ')
    result = []
    for value in values:
        value = "%s%s" % (value, suffix)
        if prefix:
            if sep_prefix:
                result += [prefix, value]
            else:
                result.append("%s%s" % (prefix, value))
        else:
            result.append(value)
    return result
def _preprocessor_options(options):
    options.cppdefines = ListOptionType(
        description="C/C++ preprocessor defines",
        unique=True,
        separators=None)
    options.defines = options.cppdefines
    options.cppdefines_prefix = StrOptionType(
        description="Flag for C/C++ preprocessor defines.", is_hidden=True)
    options.cppdefines_flags = ListOptionType(separators=None)
    options.cppdefines_flags += SimpleOperation(_add_prefix,
                                                options.cppdefines_prefix,
                                                options.cppdefines)
    options.cpppath_flags = ListOptionType(separators=None)
    options.cpppath_prefix = StrOptionType(
        description="Flag for C/C++ preprocessor paths.",
        is_hidden=True)
    options.cpppath = ListOptionType(
        description="C/C++ preprocessor paths to headers",
        value_type=AbsPathOptionType(),
        unique=True,
        separators=None)
    options.include = options.cpppath
    options.cpppath_flags = SimpleOperation(_add_prefix,
                                            options.cpppath_prefix,
                                            options.cpppath)
    options.api_cpppath = ListOptionType(
        value_type=AbsPathOptionType(),
        unique=True,
        description="C/C++ preprocessor paths to API headers",
        separators=None)
    options.cpppath_flags += SimpleOperation(_add_prefix,
                                             options.cpppath_prefix,
                                             options.api_cpppath)
    options.ext_cpppath = ListOptionType(
        value_type=AbsPathOptionType(),
        unique=True,
        description="C/C++ preprocessor path to external headers",
        separators=None)
    options.ext_include = options.ext_cpppath
    options.cpppath_flags += SimpleOperation(_add_prefix,
                                             options.cpppath_prefix,
                                             options.ext_cpppath)
    options.sys_cpppath = ListOptionType(
        value_type=AbsPathOptionType(),
        description="C/C++ preprocessor path to standard headers",
        separators=None)
def _compiler_options(options):
    options.language = EnumOptionType(values=[('c++', 'cpp'), 'c'],
                                      default='c++',
                                      description='Current language',
                                      is_hidden=True)
    options.pic = BoolOptionType(
        description="Generate position-independent code.", default=True)
    options.objsuffix = StrOptionType(
        description="Object file suffix.", is_hidden=True)
    options.cxxflags = ListOptionType(
        description="C++ compiler flags", separators=None)
    options.cflags = ListOptionType(
        description="C++ compiler flags", separators=None)
    options.ccflags = ListOptionType(
        description="Common C/C++ compiler flags", separators=None)
    options.occflags = ListOptionType(
        description="Common C/C++ compiler optimization flags",
        separators=None)
    options.cc = AbsPathOptionType(description="C/C++ compiler program")
    options.cc_name = StrOptionType(is_tool_key=True,
                                    ignore_case=True,
                                    description="C/C++ compiler name")
    options.cc_ver = VersionOptionType(is_tool_key=True,
                                       description="C/C++ compiler version")
    options.cc_cmd = ListOptionType(separators=None,
                                    description="C/C++ compiler full command",
                                    is_hidden=True)
    options.cc_cmd = options.cc
    options.If().language.eq('c++').cc_cmd += options.cxxflags
    options.If().language.eq('c').cc_cmd += options.cflags
    options.cc_cmd += options.ccflags + options.occflags +         options.cppdefines_flags + options.cpppath_flags
    options.cxxstd = EnumOptionType(values=['default',
                                            ('c++98', 'c++03'),
                                            ('c++11', 'c++0x'),
                                            ('c++14', 'c++1y')],
                                    default='default',
                                    description='C++ language standard.')
def _resource_compiler_options(options):
    options.rc = AbsPathOptionType(
        description="C/C++ resource compiler program")
    options.ressuffix = StrOptionType(
        description="Compiled resource file suffix.",
        is_hidden=True)
    options.rcflags = ListOptionType(
        description="C/C++ resource compiler flags",
        separators=None)
    options.rc_cmd = ListOptionType(
        description="C/C++ resource resource compiler full command",
        separators=None,
        is_hidden=True)
    options.rc_cmd = [options.rc] + options.rcflags +         options.cppdefines_flags + options.cpppath_flags
def _linker_options(options):
    options.libprefix = StrOptionType(
        description="Static library archiver prefix.", is_hidden=True)
    options.libsuffix = StrOptionType(
        description="Static library archiver suffix.", is_hidden=True)
    options.libflags = ListOptionType(
        description="Static library archiver flags", separators=None)
    options.olibflags = ListOptionType(
        description="Static library archiver optimization flags",
        separators=None)
    options.lib = AbsPathOptionType(
        description="Static library archiver program")
    options.lib_cmd = ListOptionType(
        description="Static library archiver full command",
        separators=None,
        is_hidden=True)
    options.lib_cmd = [options.lib] + options.libflags + options.olibflags
    options.shlibprefix = StrOptionType(description="Shared library prefix.",
                                        is_hidden=True)
    options.shlibsuffix = StrOptionType(description="Shared library suffix.",
                                        is_hidden=True)
    options.libpath = ListOptionType(value_type=AbsPathOptionType(),
                                     description="Paths to external libraries",
                                     unique=True,
                                     separators=None)
    options.libpath_prefix = StrOptionType(
        description="Flag for library paths.",
        is_hidden=True)
    options.libpath_flags = ListOptionType(separators=None)
    options.libpath_flags = SimpleOperation(_add_prefix,
                                            options.libpath_prefix,
                                            options.libpath)
    options.libs = ListOptionType(value_type=StrOptionType(),
                                  description="Linking external libraries",
                                  unique=True,
                                  separators=None)
    options.libs_prefix = StrOptionType(
        description="Prefix flag for libraries.", is_hidden=True)
    options.libs_suffix = StrOptionType(
        description="Suffix flag for libraries.", is_hidden=True)
    options.libs_flags = ListOptionType(separators=None)
    options.libs_flags = SimpleOperation(_add_ixes,
                                         options.libs_prefix,
                                         options.libs_suffix,
                                         options.libs)
    options.progsuffix = StrOptionType(
        description="Program suffix.", is_hidden=True)
    options.linkflags = ListOptionType(
        description="Linker flags", separators=None)
    options.olinkflags = ListOptionType(
        description="Linker optimization flags", separators=None)
    options.link = AbsPathOptionType(description="Linker program")
    options.link_cmd = ListOptionType(description="Linker full command",
                                      separators=None,
                                      is_hidden=True)
    options.link_cmd = [options.link] + options.linkflags +         options.olinkflags + options.libpath_flags + options.libs_flags
def _get_cpp_options():
    options = Options()
    _preprocessor_options(options)
    _compiler_options(options)
    _resource_compiler_options(options)
    _linker_options(options)
    return options
def _get_res_options():
    options = Options()
    _preprocessor_options(options)
    _resource_compiler_options(options)
    return options
class HeaderChecker (Builder):
    SIGNATURE_ATTRS = ('cpppath', )
    def __init__(self, options):
        cpppath = list(options.cpppath.get())
        cpppath += options.ext_cpppath.get()
        cpppath += options.sys_cpppath.get()
        self.cpppath = cpppath
    def build(self, source_entities, targets):
        has_headers = True
        cpppath = self.cpppath
        for header in source_entities:
            found = find_file_in_paths(cpppath, header.get())
            if not found:
                has_headers = False
                break
        targets.add_targets(has_headers)
class CommonCompiler (FileBuilder):
    NAME_ATTRS = ('prefix', 'suffix', 'ext')
    SIGNATURE_ATTRS = ('cmd', )
    def __init__(self, options, ext, cmd):
        self.prefix = options.prefix.get()
        self.suffix = options.suffix.get()
        self.ext = ext
        self.cmd = list(cmd)
        target = options.target.get()
        if target:
            self.target = self.get_target_path(target, self.ext, self.prefix)
        else:
            self.target = None
        ext_cpppath = list(options.ext_cpppath.get())
        ext_cpppath += options.sys_cpppath.get()
        self.ext_cpppath = tuple(set(os.path.normcase(
            os.path.abspath(folder)) + os.path.sep for folder in ext_cpppath))
    def get_target_entities(self, source_values):
        return self.get_obj_path(source_values[0].get())
    def get_obj_path(self, source):
        if self.target:
            return self.target
        return self.get_source_target_path(source,
                                           ext=self.ext,
                                           prefix=self.prefix,
                                           suffix=self.suffix)
    def get_default_obj_ext(self):
        """
        Returns a default extension of output object files.
        """
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def check_batch_split(self, source_entities):
        default_ext = self.get_default_obj_ext()
        if self.ext != default_ext:
            raise ErrorBatchBuildCustomExt(
                self.get_trace(source_entities), self.ext)
        if self.prefix:
            raise ErrorBatchBuildWithPrefix(
                self.get_trace(source_entities), self.prefix)
        if self.suffix:
            raise ErrorBatchBuildWithSuffix(
                self.get_trace(source_entities), self.suffix)
        if self.target:
            raise ErrorBatchCompileWithCustomTarget(
                self.get_trace(source_entities), self.target)
    def split_batch(self, source_entities):
        self.check_batch_split(source_entities)
        return self.split_batch_by_build_dir(source_entities)
    def split(self, source_entities):
        if self.target and (len(source_entities) > 1):
            raise ErrorCompileWithCustomTarget(
                self.get_trace(source_entities), self.target)
        return self.split_single(source_entities)
    def get_trace_name(self, source_entities, brief):
        if brief:
            name = self.cmd[0]
            name = os.path.splitext(os.path.basename(name))[0]
        else:
            name = ' '.join(self.cmd)
        return name
class CommonCppCompiler (CommonCompiler):
    def __init__(self, options):
        super(CommonCppCompiler, self).__init__(options,
                                                ext=options.objsuffix.get(),
                                                cmd=options.cc_cmd.get())
class CommonResCompiler (CommonCompiler):
    def __init__(self, options):
        super(CommonResCompiler, self).__init__(options,
                                                ext=options.ressuffix.get(),
                                                cmd=options.rc_cmd.get())
class CommonCppLinkerBase(FileBuilder):
    CPP_EXT = (".cc", ".cp", ".cxx", ".cpp", ".CPP", ".c++", ".C", ".c")
    NAME_ATTRS = ('target', )
    SIGNATURE_ATTRS = ('cmd', )
    def __init__(self, options):
        self.compilers = self.get_source_builders(options)
    def get_cpp_exts(self, _cpp_ext=CPP_EXT):
        return _cpp_ext
    def get_res_exts(self):
        return '.rc',
    def make_compiler(self, options):
        """
        It should return a builder of C/C++ compiler
        """
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def make_res_compiler(self, options):
        """
        It should return a builder of C/C++ resource compiler
        """
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def add_source_builders(self, builders, exts, builder):
        if builder:
            for ext in exts:
                builders[ext] = builder
    def get_source_builders(self, options):
        builders = {}
        compiler = self.make_compiler(options)
        self.add_source_builders(builders, self.get_cpp_exts(), compiler)
        rc_compiler = self.make_res_compiler(options)
        self.add_source_builders(builders, self.get_res_exts(), rc_compiler)
        return builders
    def replace(self, options, source_entities):
        cwd = os.getcwd()
        def _add_sources():
            if current_builder is None:
                new_sources.extend(current_sources)
                return
            src_node = Node(current_builder, current_sources, cwd)
            new_sources.append(src_node)
        new_sources = []
        builders = self.compilers
        current_builder = None
        current_sources = []
        for src_file in source_entities:
            ext = os.path.splitext(src_file.get())[1]
            builder = builders.get(ext, None)
            if current_builder is builder:
                current_sources.append(src_file)
            else:
                if current_sources:
                    _add_sources()
                current_builder = builder
                current_sources = [src_file]
        if current_sources:
            _add_sources()
        return new_sources
    def get_target_entities(self, source_values):
        return self.target
    def get_trace_name(self, source_entities, brief):
        if brief:
            name = self.cmd[0]
            name = os.path.splitext(os.path.basename(name))[0]
        else:
            name = ' '.join(self.cmd)
        return name
class CommonCppArchiver(CommonCppLinkerBase):
    def __init__(self, options, target):
        super(CommonCppArchiver, self).__init__(options)
        prefix = options.libprefix.get()
        ext = options.libsuffix.get()
        self.target = self.get_target_path(target, ext=ext, prefix=prefix)
        self.cmd = options.lib_cmd.get()
        self.shared = False
class CommonCppLinker(CommonCppLinkerBase):
    def __init__(self, options, target, shared):
        super(CommonCppLinker, self).__init__(options)
        if shared:
            prefix = options.shlibprefix.get()
            ext = options.shlibsuffix.get()
        else:
            prefix = options.prefix.get()
            ext = options.progsuffix.get()
        self.target = self.get_target_path(target, prefix=prefix, ext=ext)
        self.cmd = options.link_cmd.get()
        self.shared = shared
    def get_weight(self, source_entities):
        return 2 * len(source_entities)
class ToolCommonCpp(Tool):
    def __init__(self, options):
        options.If().cc_name.is_true().build_dir_name += '_' +             options.cc_name + '_' + options.cc_ver
        self.Object = self.compile
        self.Compile = self.compile
        self.Resource = self.compile_resource
        self.CompileResource = self.compile_resource
        self.Library = self.link_static_library
        self.LinkLibrary = self.link_static_library
        self.LinkStaticLibrary = self.link_static_library
        self.SharedLibrary = self.link_shared_library
        self.LinkSharedLibrary = self.link_shared_library
        self.Program = self.link_program
        self.LinkProgram = self.link_program
    @classmethod
    def options(cls):
        options = _get_cpp_options()
        options.set_group("C/C++ compiler")
        return options
    def check_headers(self, options):
        return HeaderChecker(options)
    CheckHeaders = check_headers
    def compile(self, options):
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def compile_resource(self, options):
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def link_static_library(self, options, target):
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def link_shared_library(self, options, target, def_file=None):
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
    def link_program(self, options, target):
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
class ToolCommonRes(Tool):
    def __init__(self, options):
        self.Object = self.compile
        self.Compile = self.compile
    @classmethod
    def options(cls):
        options = _get_res_options()
        options.set_group("C/C++ resource compiler")
        return options
    def compile(self, options):
        """
        It should return a builder of C/C++ resource compiler
        """
        raise NotImplementedError(
            "Abstract method. It should be implemented in a child class.")
class ZipFilesBuilder (FileBuilder):
    NAME_ATTRS = ['target']
    SIGNATURE_ATTRS = ['rename', 'basedir']
    def __init__(self, options, target, rename=None, basedir=None, ext=None):
        if ext is None:
            ext = ".zip"
        self.target = self.get_target_path(target, ext=ext)
        self.rename = tuple(rename for rename in to_sequence(rename))
        sep = os.path.sep
        self.basedir = tuple(os.path.normcase(os.path.normpath(basedir)) + sep
                             for basedir in to_sequence(basedir))
    def __open_arch(self, large=False):
        try:
            return zipfile.ZipFile(self.target,
                                   "w",
                                   zipfile.ZIP_DEFLATED,
                                   large)
        except RuntimeError:
            pass
        return zipfile.ZipFile(self.target, "w", zipfile.ZIP_STORED, large)
    def __get_arcname(self, file_path):
        for arc_name, path in self.rename:
            if file_path == path:
                return arc_name
        for basedir in self.basedir:
            if file_path.startswith(basedir):
                return file_path[len(basedir):]
        return os.path.basename(file_path)
    def __add_files(self, arch, source_entities):
        for entity in source_entities:
            if isinstance(entity, FileEntityBase):
                filepath = entity.get()
                arcname = self.__get_arcname(filepath)
                arch.write(filepath, arcname)
            else:
                arcname = entity.name
                data = entity.get()
                if is_unicode(data):
                    data = encode_str(data)
                arch.writestr(arcname, data)
    def build(self, source_entities, targets):
        target = self.target
        arch = self.__open_arch()
        try:
            self.__add_files(arch, source_entities)
        except zipfile.LargeZipFile:
            arch.close()
            arch = None
            arch = self.__open_arch(large=True)
            self.__add_files(arch, source_entities)
        finally:
            if arch is not None:
                arch.close()
        targets.add_targets(target)
    def get_trace_name(self, source_entities, brief):
        return "Create Zip"
    def get_target_entities(self, source_entities):
        return self.target
class TarFilesBuilder (FileBuilder):
    NAME_ATTRS = ['target']
    SIGNATURE_ATTRS = ['rename', 'basedir']
    def __init__(self, options, target, mode, rename, basedir, ext):
        if not mode:
            mode = "w:bz2"
        if not ext:
            if mode == "w:bz2":
                ext = ".tar.bz2"
            elif mode == "w:gz":
                ext = ".tar.gz"
            elif mode == "w":
                ext = ".tar"
        self.target = self.get_target_path(target, ext)
        self.mode = mode
        self.rename = rename if rename else tuple()
        self.basedir = os.path.normcase(
            os.path.normpath(basedir)) if basedir else None
    def __get_arcname(self, file_path):
        for arc_name, path in self.rename:
            if file_path == path:
                return arc_name
        basedir = self.basedir
        if basedir:
            if file_path.startswith(basedir):
                return file_path[len(basedir):]
        return os.path.basename(file_path)
    def __add_file(self, arch, filepath):
        arcname = self.__get_arcname(filepath)
        arch.add(filepath, arcname)
    @staticmethod
    def __add_entity(arch, entity):
        arcname = entity.name
        data = entity.get()
        if is_unicode(data):
            data = encode_str(data)
        tinfo = tarfile.TarInfo(arcname)
        tinfo.size = len(data)
        arch.addfile(tinfo, io.BytesIO(data))
    def build(self, source_entities, targets):
        target = self.target
        arch = tarfile.open(name=self.target, mode=self.mode)
        try:
            for entity in source_entities:
                if isinstance(entity, FileEntityBase):
                    self.__add_file(arch, entity.get())
                else:
                    self.__add_entity(arch, entity)
        finally:
            arch.close()
        targets.add_targets(target)
    def get_trace_name(self, source_entities, brief):
        return "Create Tar"
    def get_target_entities(self, source_entities):
        return self.target
class FindFilesBuilder (FileBuilder):
    NAME_ATTRS = ['mask']
    SIGNATURE_ATTRS = ['exclude_mask', 'exclude_subdir_mask']
    def __init__(self, options, mask,
                 exclude_mask=None,
                 exclude_subdir_mask=None):
        self.mask = mask
        self.exclude_mask = exclude_mask
        self.exclude_subdir_mask = exclude_subdir_mask
    def make_entity(self, value, tags=None):
        return DirEntity(name=value, tags=tags)
    def build(self, source_entities, targets):
        paths = [src.get() for src in source_entities]
        args = {'paths': paths}
        if self.mask is not None:
            args['mask'] = self.mask
        if self.exclude_mask is not None:
            args['exclude_mask'] = self.exclude_mask
        if self.exclude_subdir_mask is not None:
            args['exclude_subdir_mask'] = self.exclude_subdir_mask
        args['found_dirs'] = found_dirs = set()
        files = find_files(**args)
        targets.add_target_files(files)
        found_dirs = map(DirEntity, found_dirs)
        targets.add_implicit_dep_entities(found_dirs)
    def get_trace_name(self, source_entities, brief):
        trace = "Find files"
        if self.mask:
            trace += "(%s)" % self.mask
        return trace
    def check_actual(self, target_entities):
        return None
    def clear(self, target_entities, side_effect_entities):
        pass
class InstallDistBuilder (FileBuilder):
    NAME_ATTRS = ('user',)
    def __init__(self, options, user):
        self.user = user
    def get_trace_name(self, source_entities, brief):
        return "distutils install"
    def build(self, source_entities, targets):
        script = source_entities[0].get()
        cmd = [sys.executable, script, "install"]
        if self.user:
            cmd.append("--user")
        script_dir = os.path.dirname(script)
        out = self.exec_cmd(cmd, script_dir)
        return out
class BuiltinTool(Tool):
    def execute_command(self, options,
                        target=None, target_flag=None, cwd=None):
        return ExecuteCommandBuilder(options, target=target,
                                     target_flag=target_flag, cwd=cwd)
    ExecuteCommand = execute_command
    Command = ExecuteCommand
    def execute_method(self, options,
                       method, args=None, kw=None, single=True,
                       make_files=True, clear_targets=True):
        return ExecuteMethodBuilder(options, method=method, args=args, kw=kw,
                                    single=single, make_files=make_files,
                                    clear_targets=clear_targets)
    ExecuteMethod = execute_method
    Method = ExecuteMethod
    def find_files(self, options, mask=None,
                   exclude_mask=None, exclude_subdir_mask=None):
        return FindFilesBuilder(options,
                                mask,
                                exclude_mask,
                                exclude_subdir_mask)
    FindFiles = find_files
    def copy_files(self, options, target, basedir=None):
        return CopyFilesBuilder(options, target, basedir=basedir)
    CopyFiles = copy_files
    def copy_file_as(self, options, target):
        return CopyFileAsBuilder(options, target)
    CopyFileAs = copy_file_as
    def write_file(self, options, target, binary=False, encoding=None):
        return WriteFileBuilder(options, target,
                                binary=binary, encoding=encoding)
    WriteFile = write_file
    def create_dist(self, options, target, command, args=None):
        return DistBuilder(options, target=target, command=command, args=args)
    CreateDist = create_dist
    def install_dist(self, options, user=True):
        return InstallDistBuilder(options, user=user)
    InstallDist = install_dist
    def create_zip(self, options, target, rename=None, basedir=None, ext=None):
        return ZipFilesBuilder(options, target=target, rename=rename,
                               basedir=basedir, ext=ext)
    CreateZip = create_zip
    def create_tar(self, options,
                   target, mode=None, rename=None, basedir=None, ext=None):
        return TarFilesBuilder(options, target=target, mode=mode,
                               rename=rename, basedir=basedir, ext=ext)
    CreateTar = create_tar
@event_warning
def event_tools_unable_load_module(settings, module, err):
    log_warning("Unable to load module: %s, error: %s", module, err)
@event_warning
def event_tools_tool_failed(settings, ex, tool_info):
    tool_class = tool_info.tool_class
    module = tool_class.__module__
    try:
        filename = sys.modules[module].__file__
    except Exception:
        filename = module[module.rfind('.') + 1:] + '.py'
    names = ','.join(tool_info.names)
    log_error("Failed to initialize tool: name: %s, class: %s, file: %s",
              names, tool_class.__name__, filename)
    log_error(ex)
def _tool_setup_stub(cls, options):
    pass
class ErrorToolInvalid(Exception):
    def __init__(self, tool_class):
        msg = "Invalid tool type: '%s'" % (tool_class,)
        super(ErrorToolInvalid, self).__init__(msg)
class ErrorToolInvalidSetupMethod(Exception):
    def __init__(self, method):
        msg = "Invalid tool setup method: '%s'" % (method,)
        super(ErrorToolInvalidSetupMethod, self).__init__(msg)
class ErrorToolNotFound(Exception):
    def __init__(self, tool_name, loaded_paths):
        loaded_paths = ', '.join(loaded_paths)
        msg = "Tool '%s' has not been found in the following paths: %s" % (
            tool_name, loaded_paths)
        super(ErrorToolNotFound, self).__init__(msg)
class ToolInfo(object):
    __slots__ = (
        'tool_class',
        'names',
        'options',
        'setup_methods',
    )
    def __getattr__(self, attr):
        if attr == 'options':
            self.options = self.tool_class.options()
            return self.options
        raise AttributeError("%s instance has no attribute '%s'" %
                             (type(self), attr))
    def get_tool(self, options, setup, ignore_errors):
        tool_options = options.override()
        try:
            tool_options.merge(self.options)
            tool_class = self.tool_class
            setup(tool_class, tool_options)
            tool_class.setup(tool_options)
            if tool_options.has_changed_key_options():
                raise NotImplementedError()
            tool_obj = tool_class(tool_options)
            return tool_obj, tool_options
        except NotImplementedError:
            tool_options.clear()
        except Exception as ex:
            tool_options.clear()
            event_tools_tool_failed(ex, self)
            if not ignore_errors:
                raise
        return None, None
class ToolsManager(object):
    __slots__ = (
        'tool_classes',
        'tool_names',
        'tool_info',
        'all_setup_methods',
        'loaded_paths'
    )
    def __init__(self):
        self.tool_classes = {}
        self.tool_names = {}
        self.all_setup_methods = {}
        self.tool_info = {}
        self.loaded_paths = []
    def empty(self):
        return not bool(self.tool_classes)
    @staticmethod
    def __add_to_map(values_map, names, value):
        for name in names:
            try:
                value_list = values_map[name]
                if value in value_list:
                    continue
            except KeyError:
                value_list = []
                values_map[name] = value_list
            value_list.insert(0, value)
    def add_tool(self, tool_class, names):
        if not issubclass(tool_class, Tool):
            raise ErrorToolInvalid(tool_class)
        if names:
            names = tuple(to_sequence(names))
            self.tool_names.setdefault(tool_class, set()).update(names)
            self.__add_to_map(self.tool_classes, names, tool_class)
    def add_setup(self, setup_method, names):
        if not hasattr(setup_method, '__call__'):
            raise ErrorToolInvalidSetupMethod(setup_method)
        names = to_sequence(names)
        self.__add_to_map(self.all_setup_methods, names, setup_method)
    def load_tools(self, paths, reload=False):
        for path in to_sequence(paths):
            path = expand_file_path(path)
            if path in self.loaded_paths:
                if not reload:
                    continue
            else:
                self.loaded_paths.append(path)
            module_files = find_files(path, mask="*.py")
            if not module_files:
                continue
            self._load_tools_package(path, module_files)
    @staticmethod
    def _load_tools_package(path, module_files):
        try:
            package = load_package(path, generate_name=True)
            package_name = package.__name__
        except ImportError:
            package_name = None
        for module_file in module_files:
            try:
                load_module(module_file, package_name)
            except Exception as ex:
                event_tools_unable_load_module(module_file, ex)
    def __get_tool_info_list(self, name):
        tools_info = []
        if (type(name) is type) and issubclass(name, Tool):
            tool_classes = (name, )
        else:
            tool_classes = self.tool_classes.get(name, tuple())
        for tool_class in tool_classes:
            tool_info = self.tool_info.get(tool_class, None)
            if tool_info is None:
                names = self.tool_names.get(tool_class, [])
                tool_info = ToolInfo()
                tool_info.tool_class = tool_class
                tool_info.names = names
                self.tool_info[tool_class] = tool_info
                setup_methods = set()
                tool_info.setup_methods = setup_methods
                for name in names:
                    setup_methods.update(self.all_setup_methods.get(name, []))
                if not setup_methods:
                    setup_methods.add(_tool_setup_stub)
            tools_info.append(tool_info)
        return tools_info
    def get_tool(self, tool_name, options, ignore_errors):
        tool_info_list = self.__get_tool_info_list(tool_name)
        for tool_info in tool_info_list:
            get_tool = tool_info.get_tool
            for setup in tool_info.setup_methods:
                tool_obj, tool_options = get_tool(options, setup,
                                                  ignore_errors)
                if tool_obj is not None:
                    tool_names = self.tool_names.get(tool_info.tool_class, [])
                    return tool_obj, tool_names, tool_options
        raise ErrorToolNotFound(tool_name, self.loaded_paths)
_tools_manager = ToolsManager()
def get_tools_manager():
    return _tools_manager
def tool(*tool_names):
    def _tool(tool_class):
        _tools_manager.add_tool(tool_class, tool_names)
        return tool_class
    return _tool
def tool_setup(*tool_names):
    def _tool_setup(setup_method):
        _tools_manager.add_setup(setup_method, tool_names)
        return setup_method
    return _tool_setup
@event_status
def event_extracted_tools(settings, path):
    log_info("Extracted embedded tools into: '%s'" % (path,))
@event_warning
def event_extract_tools_failed(settings, error):
    log_warning("Failed to extract embedded tools: %s" % (error,))
_EMBEDDED_TOOLS = []   # only used by standalone script
def _extract_embedded_tools(info=get_aql_info(),
                            embedded_tools=_EMBEDDED_TOOLS):
    if not embedded_tools:
        return None
    embedded_tools = embedded_tools[0]
    if not embedded_tools:
        return None
    path = os.path.join(_get_user_config_dir(), info.module, '.embedded_tools')
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        return path
    try:
        zipped_tools = base64.b64decode(embedded_tools)
        with io.BytesIO(zipped_tools) as handle:
            with zipfile.ZipFile(handle) as zip_handle:
                zip_handle.extractall(path)
    except Exception as ex:
        event_extract_tools_failed(ex)
        return None
    event_extracted_tools(path)
    return path
class ErrorProjectInvalidMethod(Exception):
    def __init__(self, method):
        msg = "Invalid project method: '%s'" % (method,)
        super(ErrorProjectInvalidMethod, self).__init__(msg)
class ErrorProjectUnknownTarget(Exception):
    def __init__(self, target):
        msg = "Unknown build target: '%s'" % (target,)
        super(ErrorProjectUnknownTarget, self).__init__(msg)
class ErrorProjectBuilderMethodWithKW(Exception):
    def __init__(self, method):
        msg = "Keyword arguments are not allowed in builder method: '%s'" % (
            method,)
        super(ErrorProjectBuilderMethodWithKW, self).__init__(msg)
class ErrorProjectBuilderMethodUnbound(Exception):
    def __init__(self, method):
        msg = "Unbound builder method: '%s'" % (method,)
        super(ErrorProjectBuilderMethodUnbound, self).__init__(msg)
class ErrorProjectBuilderMethodFewArguments(Exception):
    def __init__(self, method):
        msg = "Too few arguments in builder method: '%s'" % (method,)
        super(ErrorProjectBuilderMethodFewArguments, self).__init__(msg)
class ErrorProjectBuilderMethodInvalidOptions(Exception):
    def __init__(self, value):
        msg = "Type of 'options' argument must be Options, instead of: "               "'%s'(%s)" % (type(value), value)
        super(ErrorProjectBuilderMethodInvalidOptions, self).__init__(msg)
def _get_user_config_dir():
    return os.path.join(os.path.expanduser('~'), '.config')
def _add_packages_from_sys_path(paths):
    local_path = os.path.normcase(os.path.expanduser('~'))
    for path in sys.path:
        path = os.path.normcase(path)
        if path.endswith('-packages') and not path.startswith(local_path):
            if path not in paths:
                paths.append(path)
def _add_packages_from_sysconfig(paths):
    try:
        from distutils.sysconfig import get_python_lib
        path = get_python_lib()
        if path not in paths:
            paths.append(path)
    except Exception:
        pass
def _get_site_packages():
    try:
        return site.getsitepackages()
    except Exception:
        pass
    paths = []
    _add_packages_from_sys_path(paths)
    _add_packages_from_sysconfig(paths)
    return paths
def _get_aqualid_install_dir():
    try:
        import aql
        return os.path.dirname(aql.__file__)
    except Exception:
        return None
def _get_default_tools_path(info=get_aql_info()):
    aql_module_name = info.module
    tool_dirs = _get_site_packages()
    tool_dirs.append(site.USER_SITE)
    tool_dirs.append(_get_user_config_dir())
    tool_dirs = [os.path.join(path, aql_module_name) for path in tool_dirs]
    aql_dir = _get_aqualid_install_dir()
    if aql_dir:
        tool_dirs.insert(-2, aql_dir)  # insert before the local tools
    tool_dirs = [os.path.join(path, 'tools') for path in tool_dirs]
    return tool_dirs
def _read_config(config_file, cli_config, options):
    tools_path = cli_config.tools_path
    cli_config.tools_path = None
    cli_config.read_file(config_file, {'options': options})
    if cli_config.tools_path:
        tools_path.insert(0, cli_config.tools_path)
    cli_config.tools_path = tools_path
class ProjectConfig(object):
    __slots__ = ('directory', 'makefile', 'targets', 'options', 'arguments',
                 'verbose', 'silent', 'no_output', 'jobs', 'keep_going',
                 'search_up', 'default_tools_path', 'tools_path',
                 'no_tool_errors',
                 'clean', 'list_options', 'list_tool_options',
                 'list_targets',
                 'debug_profile', 'debug_profile_top', 'debug_memory',
                 'debug_explain', 'debug_backtrace',
                 'debug_exec',
                 'use_sqlite', 'force_lock',
                 'show_version',
                 )
    def __init__(self, args=None):
        paths_type = value_list_type(UniqueList, AbsFilePath)
        strings_type = value_list_type(UniqueList, str)
        cli_options = (
            CLIOption("-C", "--directory", "directory", AbsFilePath, '',
                      "Change directory before reading the make files.",
                      'FILE PATH', cli_only=True),
            CLIOption("-f", "--makefile", "makefile", FilePath, 'make.aql',
                      "Path to a make file.",
                      'FILE PATH', cli_only=True),
            CLIOption("-l", "--list-options", "list_options", bool, False,
                      "List current options and exit."),
            CLIOption("-L", "--list-tool-options", "list_tool_options",
                      strings_type, [],
                      "List tool options and exit.",
                      "TOOL_NAME", cli_only=True),
            CLIOption("-t", "--list-targets", "list_targets", bool, False,
                      "List all available targets and exit.", cli_only=True),
            CLIOption("-c", "--config", "config", AbsFilePath, None,
                      "The configuration file used to read CLI arguments.",
                      cli_only=True),
            CLIOption("-R", "--clean", "clean", bool, False,
                      "Cleans targets.", cli_only=True),
            CLIOption("-u", "--up", "search_up", bool, False,
                      "Search up directory tree for a make file.",
                      cli_only=True),
            CLIOption("-e", "--no-tool-errors", "no_tool_errors", bool, False,
                      "Stop on any error during initialization of tools."),
            CLIOption("-I", "--tools-path", "tools_path", paths_type, [],
                      "Path to tools and setup scripts.", 'FILE PATH, ...'),
            CLIOption("-k", "--keep-going", "keep_going", bool, False,
                      "Keep going when some targets can't be built."),
            CLIOption("-j", "--jobs", "jobs", int, None,
                      "Number of parallel jobs to process targets.", 'NUMBER'),
            CLIOption("-v", "--verbose", "verbose", bool, False,
                      "Verbose mode."),
            CLIOption("-s", "--silent", "silent", bool, False,
                      "Don't print any messages except warnings and errors."),
            CLIOption(None, "--no-output", "no_output", bool, False,
                      "Don't print builder's output messages."),
            CLIOption(None, "--debug-memory", "debug_memory", bool, False,
                      "Display memory usage."),
            CLIOption("-P", "--debug-profile", "debug_profile",
                      AbsFilePath, None,
                      "Run under profiler and save the results "
                      "in the specified file.",
                      'FILE PATH'),
            CLIOption("-T", "--debug-profile-top", "debug_profile_top",
                      int, 30,
                      "Show the specified number of top functions "
                      "from profiler report.",
                      'FILE PATH'),
            CLIOption(None, "--debug-explain", "debug_explain", bool, False,
                      "Show the reasons why targets are being rebuilt"),
            CLIOption(None, "--debug-exec", "debug_exec", bool, False,
                      "Full trace of all executed commands."),
            CLIOption("--bt", "--debug-backtrace", "debug_backtrace",
                      bool, False, "Show call stack back traces for errors."),
            CLIOption(None, "--force-lock", "force_lock", bool, False,
                      "Forces to lock AQL DB file.", cli_only=True),
            CLIOption(None, "--use-sqlite", "use_sqlite", bool, False,
                      "Use SQLite DB."),
            CLIOption("-V", "--version", "version", bool, False,
                      "Show version and exit.", cli_only=True),
        )
        cli_config = CLIConfig(cli_options, args)
        options = builtin_options()
        user_config = os.path.join(_get_user_config_dir(), 'default.cfg')
        if os.path.isfile(user_config):
            _read_config(user_config, cli_config, options)
        config = cli_config.config
        if config:
            _read_config(config, cli_config, options)
        arguments = {}
        ignore_options = set(ProjectConfig.__slots__)
        ignore_options.add('config')
        for name, value in cli_config.items():
            if (name not in ignore_options) and (value is not None):
                arguments[name] = value
        options.update(arguments)
        self.options = options
        self.arguments = arguments
        self.directory = os.path.abspath(cli_config.directory)
        makefile = cli_config.makefile
        if makefile.find(os.path.sep) != -1:
            makefile = os.path.abspath(makefile)
        self.makefile = makefile
        self.search_up = cli_config.search_up
        self.tools_path = cli_config.tools_path
        self.default_tools_path = _get_default_tools_path()
        self.no_tool_errors = cli_config.no_tool_errors
        self.targets = cli_config.targets
        self.verbose = cli_config.verbose
        self.silent = cli_config.silent
        self.show_version = cli_config.version
        self.no_output = cli_config.no_output
        self.keep_going = cli_config.keep_going
        self.clean = cli_config.clean
        self.list_options = cli_config.list_options
        self.list_tool_options = cli_config.list_tool_options
        self.list_targets = cli_config.list_targets
        self.jobs = cli_config.jobs
        self.force_lock = cli_config.force_lock
        self.use_sqlite = cli_config.use_sqlite
        self.debug_profile = cli_config.debug_profile
        self.debug_profile_top = cli_config.debug_profile_top
        self.debug_memory = cli_config.debug_memory
        self.debug_explain = cli_config.debug_explain
        self.debug_backtrace = cli_config.debug_backtrace
        self.debug_exec = cli_config.debug_exec
class BuilderWrapper(object):
    __slots__ = ('project', 'options', 'tool', 'method', 'arg_names')
    def __init__(self, tool, method, project, options):
        self.arg_names = self.__check_builder_method(method)
        self.tool = tool
        self.method = method
        self.project = project
        self.options = options
    @staticmethod
    def __check_builder_method(method):
        if not hasattr(method, '__call__'):
            raise ErrorProjectInvalidMethod(method)
        f_args, f_varargs, f_kw, f_defaults = get_function_args(method)
        if f_kw:
            raise ErrorProjectBuilderMethodWithKW(method)
        min_args = 1  # at least one argument: options
        if isinstance(method, types.MethodType):
            if method.__self__ is None:
                raise ErrorProjectBuilderMethodUnbound(method)
        if len(f_args) < min_args:
            raise ErrorProjectBuilderMethodFewArguments(method)
        return frozenset(f_args)
    @staticmethod
    def _add_sources(name, value, sources,
                     _names=('sources', 'source')):
        if name in _names:
            if is_sequence(value):
                sources.extend(value)
            else:
                sources.append(value)
            return True
        return False
    @staticmethod
    def _add_deps(value, deps,
                  _node_types=(Node, NodeFilter, EntityBase)):
        if is_sequence(value):
            deps.extend(v for v in value if isinstance(v, _node_types))
        else:
            if isinstance(value, _node_types):
                deps.append(value)
    def _get_builder_args(self, kw):
        builder_args = {}
        sources = []
        deps = []
        options = kw.pop("options", None)
        if options is not None:
            if not isinstance(options, Options):
                raise ErrorProjectBuilderMethodInvalidOptions(options)
        else:
            options = self.options
        options = options.override()
        for name, value in kw.items():
            if self._add_sources(name, value, sources):
                continue
            self._add_deps(value, deps)
            if name in self.arg_names:
                builder_args[name] = value
            else:
                options.append_value(name, value, op_iupdate)
        return options, deps, sources, builder_args
    def __call__(self, *args, **kw):
        options, deps, sources, builder_args = self._get_builder_args(kw)
        sources += args
        sources = flatten_list(sources)
        builder = self.method(options, **builder_args)
        node = Node(builder, sources)
        node.depends(deps)
        self.project.add_nodes((node,))
        return node
class ToolWrapper(object):
    def __init__(self, tool, project, options):
        self.project = project
        self.options = options
        self.tool = tool
    def __getattr__(self, attr):
        method = getattr(self.tool, attr)
        if attr.startswith('_') or not isinstance(method, types.MethodType):
            return method
        builder = BuilderWrapper(self.tool, method, self.project, self.options)
        setattr(self, attr, builder)
        return builder
class ProjectTools(object):
    def __init__(self, project):
        self.project = project
        self.tools_cache = {}
        tools = get_tools_manager()
        config = self.project.config
        tools.load_tools(config.default_tools_path)
        if tools.empty():
            embedded_tools_path = _extract_embedded_tools()
            if embedded_tools_path:
                tools.load_tools(embedded_tools_path)
        tools.load_tools(config.tools_path)
        self.tools = tools
    def _get_tools_options(self):
        tools_options = {}
        for name, tool in self.tools_cache.items():
            tool = next(iter(tool.values()))
            tools_options.setdefault(tool.options, []).append(name)
        return tools_options
    def _get_tool_names(self):
        return sorted(self.tools_cache)
    def __add_tool(self, tool_name, options):
        options_ref = options.get_hash_ref()
        try:
            return self.tools_cache[tool_name][options_ref]
        except KeyError:
            pass
        project = self.project
        ignore_errors = not project.config.no_tool_errors
        tool, tool_names, tool_options = self.tools.get_tool(tool_name,
                                                             options,
                                                             ignore_errors)
        tool = ToolWrapper(tool, project, tool_options)
        set_attr = self.__dict__.setdefault
        for name in tool_names:
            set_attr(name, tool)
            self.tools_cache.setdefault(name, {})[options_ref] = tool
        return tool
    def __getattr__(self, name,
                    _func_types=(types.FunctionType, types.MethodType)):
        options = self.project.options
        tool = BuiltinTool(options)
        tool_method = getattr(tool, name, None)
        if tool_method and isinstance(tool_method, _func_types):
            return BuilderWrapper(tool, tool_method, self.project, options)
        return self.__add_tool(name, options)
    def __getitem__(self, name):
        return getattr(self, name)
    def get_tools(self, *tool_names, **kw):
        options = kw.pop('options', None)
        tools_path = kw.pop('tools_path', None)
        if tools_path:
            self.tools.load_tools(tools_path)
        if options is None:
            options = self.project.options
        if kw:
            options = options.override()
            options.update(kw)
        tools = [self.__add_tool(tool_name, options)
                 for tool_name in tool_names]
        return tools
    def get_tool(self, tool_name, **kw):
        return self.get_tools(tool_name, **kw)[0]
    def try_tool(self, tool_name, **kw):
        try:
            return self.get_tools(tool_name, **kw)[0]
        except ErrorToolNotFound:
            return None
    def add_tool(self, tool_class, tool_names=tuple()):
        self.tools.add_tool(tool_class, tool_names)
        return self.__add_tool(tool_class, self.project.options)
def _text_targets(targets):
    text = ["", "  Targets:", "==================", ""]
    max_name = ""
    for names, is_built, description in targets:
        max_name = max(max_name, *names, key=len)
    name_format = "{is_built} {name:<%s}" % len(max_name)
    for names, is_built, description in targets:
        if len(names) > 1 and text[-1]:
            text.append('')
        is_built_mark = "*" if is_built else " "
        for name in names:
            text.append(name_format.format(name=name, is_built=is_built_mark))
        text[-1] += ' :  ' + description
        if len(names) > 1:
            text.append('')
    text.append('')
    return text
class Project(object):
    def __init__(self, config):
        self.targets = config.targets
        self.options = config.options
        self.arguments = config.arguments
        self.config = config
        self.scripts_cache = {}
        self.configs_cache = {}
        self.aliases = {}
        self.alias_descriptions = {}
        self.defaults = []
        self.build_manager = BuildManager()
        self.tools = ProjectTools(self)
    def __getattr__(self, attr):
        if attr == 'script_locals':
            self.script_locals = self.__get_script_locals()
            return self.script_locals
        raise AttributeError("No attribute '%s'" % (attr,))
    def __get_script_locals(self):
        script_locals = {
            'options':          self.options,
            'tools':            self.tools,
            'Tool':             self.tools.get_tool,
            'TryTool':          self.tools.try_tool,
            'Tools':            self.tools.get_tools,
            'AddTool':          self.tools.add_tool,
            'LoadTools':        self.tools.tools.load_tools,
            'FindFiles':        find_files,
            'GetProject':       self.get_project,
            'GetProjectConfig': self.get_project_config,
            'GetBuildTargets':  self.get_build_targets,
            'File':             self.make_file_entity,
            'Entity':           self.make_entity,
            'Dir':              self.make_dir_entity,
            'Config':           self.read_config,
            'Script':           self.read_script,
            'SetBuildDir':      self.set_build_dir,
            'Depends':          self.depends,
            'Requires':         self.requires,
            'RequireModules':   self.require_modules,
            'Sync':             self.sync_nodes,
            'BuildIf':          self.build_if,
            'SkipIf':           self.skip_if,
            'Alias':            self.alias_nodes,
            'Default':          self.default_build,
            'AlwaysBuild':      self.always_build,
            'Expensive':        self.expensive,
            'Build':            self.build,
            'Clear':            self.clear,
            'DirName':          self.node_dirname,
            'BaseName':         self.node_basename,
        }
        return script_locals
    def get_project(self):
        return self
    def get_project_config(self):
        return self.config
    def get_build_targets(self):
        return self.targets
    def make_file_entity(self, filepath, options=None):
        if options is None:
            options = self.options
        file_type = FileTimestampEntity             if options.file_signature == 'timestamp'             else FileChecksumEntity
        return file_type(filepath)
    def make_dir_entity(self, filepath):
        return DirEntity(filepath)
    def make_entity(self, data, name=None):
        return SimpleEntity(data=data, name=name)
    def _get_config_options(self, config, options):
        if options is None:
            options = self.options
        options_ref = options.get_hash_ref()
        config = os.path.normcase(os.path.abspath(config))
        options_set = self.configs_cache.setdefault(config, set())
        if options_ref in options_set:
            return None
        options_set.add(options_ref)
        return options
    def _remove_overridden_options(self, result):
        for arg in self.arguments:
            try:
                del result[arg]
            except KeyError:
                pass
    def read_config(self, config, options=None):
        options = self._get_config_options(config, options)
        if options is None:
            return
        config_locals = {'options': options}
        dir_name, file_name = os.path.split(config)
        with Chdir(dir_name):
            result = exec_file(file_name, config_locals)
        tools_path = result.pop('tools_path', None)
        if tools_path:
            self.tools.tools.load_tools(tools_path)
        self._remove_overridden_options(result)
        options.update(result)
    def read_script(self, script):
        script = os.path.normcase(os.path.abspath(script))
        scripts_cache = self.scripts_cache
        script_result = scripts_cache.get(script, None)
        if script_result is not None:
            return script_result
        dir_name, file_name = os.path.split(script)
        with Chdir(dir_name):
            script_result = exec_file(file_name, self.script_locals)
        scripts_cache[script] = script_result
        return script_result
    def add_nodes(self, nodes):
        self.build_manager.add(nodes)
    def set_build_dir(self, build_dir):
        build_dir = os.path.abspath(expand_file_path(build_dir))
        if self.options.build_dir != build_dir:
            self.options.build_dir = build_dir
    def build_if(self, condition, nodes):
        self.build_manager.build_if(condition, nodes)
    def skip_if(self, condition, nodes):
        self.build_manager.skip_if(condition, nodes)
    def depends(self, nodes, dependencies):
        dependencies = tuple(to_sequence(dependencies))
        depends = self.build_manager.depends
        for node in to_sequence(nodes):
            node.depends(dependencies)
            depends(node, node.dep_nodes)
    def requires(self, nodes, dependencies):
        dependencies = tuple(
            dep for dep in to_sequence(dependencies) if isinstance(dep, Node))
        depends = self.build_manager.depends
        for node in to_sequence(nodes):
            depends(node, dependencies)
    def require_modules(self, nodes, dependencies):
        dependencies = tuple(
            dep for dep in to_sequence(dependencies) if isinstance(dep, Node))
        module_depends = self.build_manager.module_depends
        for node in to_sequence(nodes):
            module_depends(node, dependencies)
    def sync_nodes(self, *nodes):
        nodes = flatten_list(nodes)
        nodes = tuple(node for node in nodes if isinstance(node, Node))
        self.build_manager.sync(nodes)
    def alias_nodes(self, alias, nodes, description=None):
        for alias, node in itertools.product(to_sequence(alias),
                                             to_sequence(nodes)):
            self.aliases.setdefault(alias, set()).add(node)
            if description:
                self.alias_descriptions[alias] = description
    def default_build(self, nodes):
        for node in to_sequence(nodes):
            self.defaults.append(node)
    def always_build(self, nodes):
        null_value = NullEntity()
        for node in to_sequence(nodes):
            node.depends(null_value)
    def expensive(self, nodes):
        self.build_manager.expensive(nodes)
    def _add_alias_nodes(self, target_nodes, aliases):
        try:
            for alias in aliases:
                target_nodes.update(self.aliases[alias])
        except KeyError as ex:
            raise ErrorProjectUnknownTarget(ex.args[0])
    def _add_default_nodes(self, target_nodes):
        for node in self.defaults:
            if isinstance(node, Node):
                target_nodes.add(node)
            else:
                self._add_alias_nodes(target_nodes, (node,))
    def _get_build_nodes(self):
        target_nodes = set()
        self._add_alias_nodes(target_nodes, self.targets)
        if not target_nodes:
            self._add_default_nodes(target_nodes)
        if not target_nodes:
            target_nodes = None
        return target_nodes
    def _get_jobs_count(self, jobs=None):
        if jobs is None:
            jobs = self.config.jobs
        if not jobs:
            jobs = 0
        else:
            jobs = int(jobs)
        if not jobs:
            jobs = cpu_count()
        if jobs < 1:
            jobs = 1
        elif jobs > 32:
            jobs = 32
        return jobs
    def build(self, jobs=None):
        jobs = self._get_jobs_count(jobs)
        if not self.options.batch_groups.is_set():
            self.options.batch_groups = jobs
        build_nodes = self._get_build_nodes()
        config = self.config
        keep_going = config.keep_going,
        explain = config.debug_explain
        with_backtrace = config.debug_backtrace
        force_lock = config.force_lock
        use_sqlite = config.use_sqlite
        is_ok = self.build_manager.build(jobs=jobs,
                                         keep_going=bool(keep_going),
                                         nodes=build_nodes,
                                         explain=explain,
                                         with_backtrace=with_backtrace,
                                         use_sqlite=use_sqlite,
                                         force_lock=force_lock)
        return is_ok
    def clear(self):
        build_nodes = self._get_build_nodes()
        force_lock = self.config.force_lock
        use_sqlite = self.config.use_sqlite
        self.build_manager.clear(nodes=build_nodes,
                                 use_sqlite=use_sqlite,
                                 force_lock=force_lock)
    def list_targets(self):
        targets = []
        node2alias = {}
        for alias, nodes in self.aliases.items():
            key = frozenset(nodes)
            target_info = node2alias.setdefault(key, [[], ""])
            target_info[0].append(alias)
            description = self.alias_descriptions.get(alias, None)
            if description:
                if len(target_info[1]) < len(description):
                    target_info[1] = description
        build_nodes = self._get_build_nodes()
        self.build_manager.shrink(build_nodes)
        build_nodes = self.build_manager.get_nodes()
        for nodes, aliases_and_description in node2alias.items():
            aliases, description = aliases_and_description
            aliases.sort(key=str.lower)
            max_alias = max(aliases, key=len)
            aliases.remove(max_alias)
            aliases.insert(0, max_alias)
            is_built = (build_nodes is None) or nodes.issubset(build_nodes)
            targets.append((tuple(aliases), is_built, description))
        targets.sort(key=lambda names: names[0][0].lower())
        return _text_targets(targets)
    def list_options(self, brief=False):
        result = self.options.help_text("Builtin options:", brief=brief)
        result.append("")
        tool_names = self.tools._get_tool_names()
        if tool_names:
            result.append("Available options of tools: %s" %
                          (', '.join(tool_names)))
        if result[-1]:
            result.append("")
        return result
    def list_tools_options(self, tools, brief=False):
        tools = set(to_sequence(tools))
        result = []
        for tools_options, names in self.tools._get_tools_options().items():
            names_set = tools & set(names)
            if names_set:
                tools -= names_set
                options_name = "Options of tool: %s" % (', '.join(names))
                result += tools_options.help_text(options_name, brief=brief)
        if result and result[-1]:
            result.append("")
        return result
    def node_dirname(self, node):
        return NodeDirNameFilter(node)
    def node_basename(self, node):
        return NodeBaseNameFilter(node)
@event_status
def event_reading_scripts(settings):
    log_info("Reading scripts...")
@event_status
def event_reading_scripts_done(settings, elapsed):
    log_info("Reading scripts finished (%s)", elapsed)
@event_error
def event_aql_error(settings, error):
    log_error(error)
@event_status
def event_building(settings):
    log_info("Building targets...")
@event_status
def event_building_done(settings, success, elapsed):
    status = "finished" if success else "failed"
    log_info("Building targets %s (%s)", status, elapsed)
@event_status
def event_build_summary(settings, elapsed):
    log_info("Total time: %s", elapsed)
def _find_make_script(script):
    if os.path.isabs(script):
        return script
    cwd = split_path(os.path.abspath('.'))
    path_sep = os.path.sep
    while cwd:
        script_path = path_sep.join(cwd) + path_sep + script
        if os.path.isfile(script_path):
            return os.path.normpath(script_path)
        cwd.pop()
    return script
def _start_memory_tracing():
    try:
        import tracemalloc
    except ImportError:
        return
    tracemalloc.start()
def _stop_memory_tracing():
    try:
        import tracemalloc
    except ImportError:
        return
    snapshot = tracemalloc.take_snapshot()
    _log_memory_top(snapshot)
    tracemalloc.stop()
def _log_memory_top(snapshot, group_by='lineno', limit=30):
    try:
        import tracemalloc
        import linecache
    except ImportError:
        return
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(group_by)
    log_info("Top %s lines", limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        log_info("#%s: %s:%s: %.1f KiB",
                 index, filename, frame.lineno, stat.size / 1024)
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            log_info('    %s', line)
    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        log_info("%s other: %.1f KiB", len(other), size / 1024)
    total = sum(stat.size for stat in top_stats)
    log_info("Total allocated size: %.1f KiB", total / 1024)
def _print_memory_status():
    _stop_memory_tracing()
    mem_usage = memory_usage()
    num_objects = len(gc.get_objects())
    obj_mem_usage = sum(sys.getsizeof(obj) for obj in gc.get_objects())
    log_info("GC objects: %s, size: %.1f KiB, heap memory usage: %s Kb",
             num_objects, obj_mem_usage / 1024, mem_usage)
def _set_build_dir(options, makefile):
    build_dir = options.build_dir.get()
    if os.path.isabs(build_dir):
        return
    makefile_dir = os.path.abspath(os.path.dirname(makefile))
    options.build_dir = os.path.join(makefile_dir, build_dir)
def _read_make_script(prj):
    prj_cfg = prj.config
    makefile = expand_file_path(prj_cfg.makefile)
    if prj_cfg.search_up:
        makefile = _find_make_script(makefile)
    _set_build_dir(prj_cfg.options, makefile)
    event_reading_scripts()
    with Chrono() as elapsed:
        prj.read_script(makefile)
    event_reading_scripts_done(elapsed)
def _list_options(prj):
    prj_cfg = prj.config
    text = []
    if prj_cfg.list_options:
        text += prj.list_options(brief=not prj_cfg.verbose)
    if prj_cfg.list_tool_options:
        text += prj.list_tools_options(prj_cfg.list_tool_options,
                                       brief=not prj_cfg.verbose)
    log_info('\n'.join(text))
def _build(prj):
    event_building()
    with Chrono() as elapsed:
        success = prj.build()
    event_building_done(success, elapsed)
    if not success:
        prj.build_manager.print_fails()
    return success
def _main(prj_cfg):
    with Chrono() as total_elapsed:
        ev_settings = EventSettings(brief=not prj_cfg.verbose,
                                    with_output=not prj_cfg.no_output,
                                    trace_exec=prj_cfg.debug_exec)
        set_event_settings(ev_settings)
        with Chdir(prj_cfg.directory):
            if prj_cfg.debug_memory:
                _start_memory_tracing()
            prj = Project(prj_cfg)
            _read_make_script(prj)
            success = True
            if prj_cfg.clean:
                prj.clear()
            elif prj_cfg.list_targets:
                text = prj.list_targets()
                log_info('\n'.join(text))
            elif prj_cfg.list_options or prj_cfg.list_tool_options:
                _list_options(prj)
            else:
                success = _build(prj)
            if prj_cfg.debug_memory:
                _print_memory_status()
    event_build_summary(total_elapsed)
    status = int(not success)
    return status
def _patch_sys_modules():
    aql_module = sys.modules.get('aql', None)
    if aql_module is not None:
        sys.modules.setdefault(get_aql_info().module, aql_module)
    else:
        aql_module = sys.modules.get(get_aql_info().module, None)
        if aql_module is not None:
            sys.modules.setdefault('aql', aql_module)
def _run_main(prj_cfg):
    debug_profile = prj_cfg.debug_profile
    if not debug_profile:
        status = _main(prj_cfg)
    else:
        profiler = cProfile.Profile()
        status = profiler.runcall(_main, prj_cfg)
        profiler.dump_stats(debug_profile)
        p = pstats.Stats(debug_profile)
        p.strip_dirs()
        p.sort_stats('cumulative')
        p.print_stats(prj_cfg.debug_profile_top)
    return status
def _log_error(ex, with_backtrace):
    if with_backtrace:
        err = traceback.format_exc()
    else:
        if isinstance(ex, KeyboardInterrupt):
            err = "Keyboard Interrupt"
        else:
            err = to_unicode(ex)
    event_aql_error(err)
def main():
    with_backtrace = True
    try:
        _patch_sys_modules()
        prj_cfg = ProjectConfig()
        with_backtrace = prj_cfg.debug_backtrace
        if prj_cfg.show_version:
            log_info(dump_aql_info())
            return 0
        if prj_cfg.silent:
            set_log_level(LOG_WARNING)
        status = _run_main(prj_cfg)
    except (Exception, KeyboardInterrupt) as ex:
        _log_error(ex, with_backtrace)
        status = 1
    return status

_AQL_VERSION_INFO.date = "2015-12-10"