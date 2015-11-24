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

import signal

import enum
from .error import UVError
from .handle import HandleType, Handle
from .library import ffi, lib, detach, c_require, dummy_callback
from .loop import Loop
from .stream import Stream


def disable_stdio_inheritance():
    lib.uv_disable_stdio_inheritance()


def kill(pid: int, signum: int):
    code = lib.uv_kill(pid, signum)
    if code < 0: raise UVError(code)


class StdIOFlags(enum.IntEnum):
    IGNORE = lib.UV_IGNORE

    INHERIT_FD = lib.UV_INHERIT_FD
    INHERIT_STREAM = lib.UV_INHERIT_STREAM

    CREATE_PIPE = lib.UV_CREATE_PIPE
    READABLE_PIPE = lib.UV_READABLE_PIPE
    WRITABLE_PIPE = lib.UV_WRITABLE_PIPE


PIPE = StdIOFlags.CREATE_PIPE


class ProcessFlags(enum.IntEnum):
    SETUID = lib.UV_PROCESS_SETUID
    SETGID = lib.UV_PROCESS_SETGID
    DETACHED = lib.UV_PROCESS_DETACHED

    WINDOWS_HIDE = lib. UV_PROCESS_WINDOWS_HIDE
    WINDOWS_VERBATIM_ARGUMENTS = lib.UV_PROCESS_WINDOWS_VERBATIM_ARGUMENTS


@ffi.callback('uv_exit_cb')
def exit_callback(uv_process, exit_status, term_signal):
    process = detach(uv_process)
    process.on_exit(process, exit_status, term_signal)


def fill_stdio_container(uv_stdio, fileobj=None):
    if isinstance(fileobj, Stream):
        uv_stdio.data.stream = fileobj.stream
        flags = StdIOFlags.INHERIT_STREAM
    elif fileobj is not None:
        uv_stdio.data.fd = fileobj if isinstance(fileobj, int) else fileobj.fileno()
        flags = StdIOFlags.INHERIT_FD
    elif fileobj is PIPE:
        flags = (StdIOFlags.CREATE_PIPE | StdIOFlags.READABLE_PIPE |
                 StdIOFlags.WRITABLE_PIPE)
    else:
        flags = StdIOFlags.IGNORE
    uv_stdio.flags = flags
    return uv_stdio


@HandleType.PROCESS
class Process(Handle):
    def __init__(self, arguments, uid: int=None, gid: int=None, cwd: str=None,
                 env: dict=None, flags: int=0, loop: Loop=None, stdin=None,
                 stdout=None, stderr=None, stdio=None, on_exit: callable=dummy_callback):
        self.options = ffi.new('uv_process_options_t*')
        c_dependencies = []

        c_file = ffi.new('char []', str(arguments[0]).encode())
        self.options.file = c_file
        c_dependencies.append(c_file)

        c_args_list = [ffi.new('char []', str(arg).encode()) for arg in arguments]
        c_args = ffi.new('char *[]', c_args_list)
        self.options.args = c_args
        c_dependencies += [c_args_list, c_args]

        if cwd is not None:
            c_cwd = ffi.new('char []', str(cwd).encode())
            self.options.cwd = c_cwd
            c_dependencies.append(c_cwd)

        if env is not None:
            c_env_list = [ffi.new('char []', '%s=%s' % item) for item in env.items()]
            c_env = ffi.new('char *[]', c_env_list)
            self.options.env = c_env
            c_dependencies += [c_env_list, c_env]

        if uid is not None:
            flags |= ProcessFlags.SETUID
            self.options.uid = lib.uid_from_int(uid)

        if gid is not None:
            flags |= ProcessFlags.SETGID
            self.options.gid = lib.gid_from_int(gid)

        stdio_count = 3
        if stdio is not None: stdio_count += len(stdio)
        self.options.stdio_count = stdio_count

        c_stdio = ffi.new('uv_stdio_container_t[]', 3 + stdio_count)
        fill_stdio_container(c_stdio[0], stdin)
        fill_stdio_container(c_stdio[1], stdout)
        fill_stdio_container(c_stdio[2], stderr)
        if stdio is not None:
            for index, fileobj in enumerate(stdio):
                fill_stdio_container(c_stdio[index + 3], fileobj)
        self.options.stdio = c_stdio
        c_dependencies.append(c_stdio)

        self.options.flags = flags
        self.options.exit_cb = exit_callback

        c_require(self.options, c_dependencies)

        self.process = ffi.new('uv_process_t*')
        self.on_exit = on_exit
        super().__init__(self.process, loop)
        code = lib.uv_spawn(self.loop.uv_loop, self.process, self.options)
        if code < 0: raise UVError(code)

    @property
    def pid(self) -> int:
        return self.process.pid

    def kill(self, signum: int=signal.SIGKILL):
        code = lib.uv_process_kill(self.process, signum)
        if code < 0: raise UVError(code)
