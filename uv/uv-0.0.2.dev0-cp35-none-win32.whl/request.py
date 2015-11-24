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

from .library import ffi, lib, attach

__all__ = ['RequestType', 'Request']

_request_type_implementations = {}


class RequestType(enum.IntEnum):
    UNKNOWN = lib.UV_UNKNOWN_REQ
    CONNECT = lib.UV_CONNECT
    WRITE = lib.UV_WRITE
    SHUTDOWN = lib.UV_SHUTDOWN
    SEND = lib.UV_UDP_SEND
    FS = lib.UV_FS
    WORK = lib.UV_WORK
    GETADDRINFO = lib.UV_GETADDRINFO
    GETNAMEINFO = lib.UV_GETNAMEINFO

    def __call__(self, implementation):
        _request_type_implementations[self] = implementation
        return implementation

    def get(self):
        return _request_type_implementations.get(self, Request)


@RequestType.UNKNOWN
class Request:
    __slots__ = ['uv_request', 'c_attachment']

    def __init__(self, request):
        self.uv_request = ffi.cast('uv_req_t*', request)
        self.c_attachment = attach(self.uv_request, self)

    @property
    def type(self):
        return RequestType(self.uv_request.type).get()

    def cancel(self):
        lib.uv_cancel(self.uv_request)
