# This file is part of maggit.
#
# Copyright 2015 Matthieu Gautier <dev@mgautier.fr>
#
# Pit is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# Additional permission under the GNU Affero GPL version 3 section 7:
#
# If you modify this Program, or any covered work, by linking or
# combining it with other code, such other code is not for that reason
# alone subject to any of the requirements of the GNU Affero GPL
# version 3.
#
# You should have received a copy of the GNU Affero General Public License
# along with maggit.  If not, see http://www.gnu.org/licenses
#
# In summary:
# - You can use this program for no cost.
# - You can use this program for both personal and commercial reasons.
# - You do not have to share your own program's code which uses this program.
# - You have to share modifications (e.g bug-fixes, improvements) you've made to this program.

import ctypes
from mmap import mmap, ACCESS_READ
from itertools import takewhile
from collections import namedtuple
import os, stat

__all__ = ('index_content', 'EntryHeader')

_wrapping_struct_cache = {}
def read_ctypes(stream, ctypes_):
    try:
        wrapping_struct, size = _wrapping_struct_cache[ctypes_]
    except KeyError:
        wrapping_struct = type('Wrap_%s'%ctypes_, (ctypes.BigEndianStructure, ), {'_fields_':(('v', ctypes_),)})
        size = ctypes.sizeof(wrapping_struct)
        _wrapping_struct_cache[ctypes_] = wrapping_struct, size

    ret =  wrapping_struct.from_buffer_copy(stream.read(size)).v
    return ret

class index_header(ctypes.BigEndianStructure):
    _fields_ = [ ('magic'   , ctypes.c_uint8*4),
                 ('version' , ctypes.c_int32),
                 ('nb_entries', ctypes.c_int32)
               ]

class extension_header(ctypes.BigEndianStructure):
    _fields_ = [ ('magic'   , ctypes.c_uint8*4),
                 ('size' , ctypes.c_int32)
               ]

class entry_header(ctypes.BigEndianStructure):
    _fields_ = [ ('ctime_seconds', ctypes.c_int32),
                 ('ctime_nano',    ctypes.c_int32),
                 ('mtime_seconds', ctypes.c_int32),
                 ('mtime_nano',    ctypes.c_int32),
                 ('dev',           ctypes.c_int32),
                 ('ino',           ctypes.c_int32),
                 ('pad',           ctypes.c_uint32, 16),
                 ('type',          ctypes.c_uint32, 4),
                 ('pad2',          ctypes.c_uint32, 3),
                 ('perm',          ctypes.c_uint32, 9),
                 ('uid',           ctypes.c_int32),
                 ('gid',           ctypes.c_int32),
                 ('size',          ctypes.c_int32),
                 ('sha',           ctypes.c_uint8*20),
                 ('assume_valid',  ctypes.c_uint16, 1),
                 ('extend',        ctypes.c_uint16, 1),
                 ('stage',         ctypes.c_uint16, 2),
                 ('length',        ctypes.c_uint16, 12),
               ]
    _pack_ = 0

class entryv3_header(ctypes.BigEndianStructure):
    _fields_ = [ ('reserved',      ctypes.c_uint16, 1),
                 ('skip',          ctypes.c_uint16, 1),
                 ('intent_to_add', ctypes.c_uint16, 1)
               ]

class EntryHeader(namedtuple("EntryHeader", "st_mode st_ino st_dev st_nlink st_uid st_gid st_size st_atime st_mtime st_ctime st_atime_ns st_mtime_ns st_ctime_ns mode sha assume_valid stage name extend skip_worktree intent_to_add")):
    __slots__ = ()

    @staticmethod
    def from_header(header, name, extendHeader=None):
        st_ino  = int(header.ino)
        st_dev  = int(header.dev)
        st_nblink= None
        st_uid, st_gid = int(header.uid), int(header.gid)
        st_size = int(header.size)
        st_atime, st_atime_ns = None, None
        st_mtime, st_mtime_ns = int(header.mtime_seconds), int(header.mtime_nano)
        st_ctime, st_ctime_ns = int(header.ctime_seconds), int(header.ctime_nano)
        st_mode = None
        type_ = int(header.type)
        perm = int(header.perm)
        mode = type_, perm
        sha = bytes(header.sha)
        assume_valid = bool(header.assume_valid)
        extend = bool(header.extend)
        stage = int(header.stage)
        name  = name
        skip_worktree, intent_to_add = None, None
        if extend:
            skip_worktree = bool(extendHeader.skip)
            intent_to_add = bool(extendHeader.intent_to_add)

        return EntryHeader(st_mode, st_ino, st_dev, st_nblink, st_uid, st_gid, st_size, st_atime, st_mtime, st_ctime, st_atime_ns, st_mtime_ns, st_ctime_ns, mode, sha, assume_valid, stage, name, extend, skip_worktree, intent_to_add)
        




def read_string(stream, size):
    out = stream.read(size)
    if size == 0xFFF:
        b = stream.read(1)
        if ord(b):
            out += b
    else:
        assert ord(stream.read(1)) == 0
    return out

def index_content(filename):
    with filename.open('rb') as f:
        size = os.fstat(f.fileno()).st_size
        header = read_ctypes(f, index_header)
        assert bytes(header.magic) == b'DIRC'
        version = header.version
        nb_entries = header.nb_entries

        index = 0
        buff = bytearray(64)
        entries = []
        for nr in range(nb_entries):
            header = read_ctypes(f, entry_header)
            f.seek(62-ctypes.sizeof(entry_header), 1)
            index += 62
            v3header = None
            if version >= 3 and header.extend:
                v3header = read_ctypes(f, entryv3_header)
                index += ctypes.sizeof(entryv3_header)
            name = read_string(f, header.length)
            index += len(name)+1
            padding = index % 8
            if padding:
                index += 8-padding
                f.read(8-padding)
            entries.append(EntryHeader.from_header(header, name, v3header))

        extensions = []
        maxread = size - 12 -20
        while index < maxread:
            header = read_ctypes(f, extension_header)
            extensions.append((bytes(header.magic), int(header.size)))
            f.read(header.size)
            index += ctypes.sizeof(extension_header) + header.size
    return entries, extensions

