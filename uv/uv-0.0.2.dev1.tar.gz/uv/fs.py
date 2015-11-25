# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Maximilian Köhl <mail@koehlma.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import enum
from collections import namedtuple
from .error import UVError
from .handle import HandleType
from .library import ffi, lib, detach, detach_loop, dummy_callback
from .loop import Loop
from .request import Request, RequestType

Timespec = namedtuple('Timespec', ['sec', 'nsec'])

Stat = namedtuple('Stat', ['dev', 'mode', 'nlink', 'uid', 'gid', 'rdev',
                           'ino', 'size', 'blksize', 'blocks', 'flags', 'gen',
                           'atim', 'mtim', 'ctim', 'birthtim'])

Dirent = namedtuple('Dirent', ['name', 'type'])

requests = set()


def unpack_timespec(uv_timespec):
    return Timespec(uv_timespec.tv_sec, uv_timespec.tv_nsec)


def unpack_stat(uv_stat):
    return Stat(uv_stat.st_dev, uv_stat.st_mode, uv_stat.st_nlink, uv_stat.st_uid,
                uv_stat.st_gid, uv_stat.st_rdev, uv_stat.st_ino, uv_stat.st_size,
                uv_stat.st_blksize, uv_stat.st_blocks, uv_stat.st_flags, uv_stat.st_gen,
                unpack_timespec(uv_stat.st_atim), unpack_timespec(uv_stat.st_mtim),
                unpack_timespec(uv_stat.st_ctim), unpack_timespec(uv_stat.st_birthtim))


def unpack_dirent(uv_dirent):
    return Dirent(ffi.string(uv_dirent.name).decode(), DirentType(uv_dirent.type))


class FSType(enum.IntEnum):
    UNKNOWN = lib.UV_FS_UNKNOWN
    CUSTOM = lib.UV_FS_CUSTOM
    OPEN = lib.UV_FS_OPEN
    CLOSE = lib.UV_FS_CLOSE
    READ = lib.UV_FS_READ
    WRITE = lib.UV_FS_WRITE
    SENDFILE = lib.UV_FS_SENDFILE
    STAT = lib.UV_FS_STAT
    LSTAT = lib.UV_FS_LSTAT
    FSTAT = lib.UV_FS_FSTAT
    FTRUNCATE = lib.UV_FS_FTRUNCATE
    UTIME = lib.UV_FS_UTIME
    FUTIME = lib.UV_FS_FUTIME
    ACCESS = lib.UV_FS_ACCESS
    CHMOD = lib.UV_FS_CHMOD
    FCHMOD = lib.UV_FS_FCHMOD
    FSYNC = lib.UV_FS_FSYNC
    FDATASYNC = lib.UV_FS_FDATASYNC
    UNLINK = lib.UV_FS_UNLINK
    RMDIR = lib.UV_FS_RMDIR
    MKDIR = lib.UV_FS_MKDIR
    MKDTEMP = lib.UV_FS_MKDTEMP
    RENAME = lib.UV_FS_RENAME
    SCANDIR = lib.UV_FS_SCANDIR
    LINK = lib.UV_FS_LINK
    SYMLINK = lib.UV_FS_SYMLINK
    READLINK = lib.UV_FS_READLINK
    CHOWN = lib.UV_FS_CHOWN
    FCHOWN = lib.UV_FS_FCHOWN


class DirentType(enum.IntEnum):
    UNKNOWN = lib.UV_DIRENT_UNKNOWN
    FILE = lib.UV_DIRENT_FILE
    DIR = lib.UV_DIRENT_DIR
    LINK = lib.UV_DIRENT_LINK
    FIFO = lib.UV_DIRENT_FIFO
    SOCKET = lib.UV_DIRENT_SOCKET
    CHAR = lib.UV_DIRENT_CHAR
    BLOCK = lib.UV_DIRENT_BLOCK


@RequestType.FS
class FSRequest(Request):
    __slots__ = ['uv_fs', 'data', 'callback']

    def __init__(self, data, callback: callable=dummy_callback):
        self.uv_fs = ffi.new('uv_fs_t*')
        super().__init__(self.uv_fs)
        self.data = data
        self.callback = callback
        requests.add(self)

    @property
    def result(self):
        return self.uv_fs.result

    @property
    def path(self):
        return ffi.string(self.uv_fs.path).decode()

    @property
    def fs_type(self):
        return FSType(self.uv_fs.fs_type)

    @property
    def loop(self):
        return detach_loop(self.uv_fs.loop)

    @property
    def stat(self):
        return unpack_stat(self.uv_fs.statbuf)


@ffi.callback('uv_fs_cb')
def fs_callback(uv_request):
    request = detach(uv_request)
    lib.uv_fs_req_cleanup(uv_request)
    requests.remove(request)
    request.callback(request)


def stat(path: str, callback: callable=None, loop: Loop=None):
    loop = loop or Loop.default_loop()
    request = FSRequest(None, callback=callback)
    code = lib.uv_fs_stat(loop.uv_loop, request.uv_fs, path.encode(), fs_callback)
    if code < 0: raise UVError(code)
    return request


def close(fileno: int, callback: callable=None, loop: Loop=None):
    loop = loop or Loop.default_loop()
    uv_file = lib.file_from_int(fileno)
    request = FSRequest(callback)
    code = lib.uv_fs_close(loop.uv_loop, request.uv_fs, uv_file, fs_callback)
    if code < 0: raise UVError(code)
    return request


def open(path: str, flags: int, mode: int=0o777, callback: callable=None,
         loop: Loop=None):
    loop = loop or Loop.default_loop()
    c_path = path.encode()
    request = FSRequest(None, callback=callback)
    code = lib.uv_fs_open(loop.uv_loop, request.uv_fs, c_path, flags, mode, fs_callback)
    if code < 0: raise UVError(code)
    return request


@HandleType.FILE
class File:
    pass
