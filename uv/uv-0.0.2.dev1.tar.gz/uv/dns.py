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

"""
This module provides all the DNS related utilities.
"""

import socket

import typing
from collections import namedtuple
from .error import UVError
from .library import ffi, lib, detach, c_require, dummy_callback
from .loop import Loop
from .request import RequestType, Request

pending_requests = set()

AddrInfo = namedtuple('AddrInfo', ['family', 'type', 'protocol', 'canonname', 'address'])
NameInfo = namedtuple('NameInfo', ['host', 'service'])

Address4 = namedtuple('Address4', ['host', 'port'])
Address6 = namedtuple('Address6', ['host', 'port', 'flowinfo', 'scope_id'])


def unpack_addrinfo(c_addrinfo) -> typing.List[AddrInfo]:
    """
    Python <-> C utility function.

    Unpacks a C addrinfo struct into a corresponding Python AddrInfo-tuple.

    :param c_addrinfo:
    """
    items, c_next = [], c_addrinfo

    while c_next:
        family = c_next.ai_family
        socktype = c_next.ai_socktype
        protocol = c_next.ai_protocol
        if c_next.ai_canonname:
            canonname = ffi.string(c_next.ai_canonname).decode()
        else:
            canonname = None
        address = unpack_sockaddr(c_next.ai_addr) if c_next.ai_addr else None
        items.append(AddrInfo(family, socktype, protocol, canonname, address))
        c_next = c_next.ai_next

    if c_addrinfo:
        lib.uv_freeaddrinfo(c_addrinfo)

    return items


def unpack_sockaddr(c_sockaddr):
    if c_sockaddr.sa_family == socket.AF_INET:
        c_sockaddr_in = ffi.cast('struct sockaddr_in*', c_sockaddr)
        port = socket.ntohs(c_sockaddr_in.sin_port)
        c_host = ffi.new('char[16]')
        lib.uv_ip4_name(c_sockaddr_in, c_host, 16)
        return Address4(ffi.string(c_host).decode(), port)
    elif c_sockaddr.sa_family == socket.AF_INET6:
        c_sockaddr_in6 = ffi.cast('struct sockaddr_in6*', c_sockaddr)
        port = socket.ntohs(c_sockaddr_in6.sin6_port)
        c_host = ffi.new('char[40]')
        lib.uv_ip6_name(c_sockaddr_in6, c_host, 40)
        c_additional = ffi.new('unsigned long[2]')
        lib.py_ipv6_get_additional(c_sockaddr_in6, c_additional)
        return Address6(ffi.string(c_host).decode(), port, *c_additional)


def ip_addr(ip: str, port: int):
    c_sockaddr = ffi.new('struct sockaddr *')
    c_ip = ip.encode()
    code = lib.uv_ip4_addr(c_ip, port, ffi.cast('struct sockaddr_in*', c_sockaddr))
    if not code:
        return c_sockaddr
    if not lib.uv_ip6_addr(c_ip, port, ffi.cast('struct sockaddr_in6*', c_sockaddr)):
        raise UVError(code)
    return c_sockaddr


@ffi.callback('uv_getaddrinfo_cb')
def getaddrinfo_callback(uv_getaddrinfo, status, _):
    request = detach(uv_getaddrinfo)
    pending_requests.remove(request)
    if status == 0: request.populate()
    request.callback(request, status, request.addrinfo)


@RequestType.GETADDRINFO
class GetAddrInfo(Request):
    __slots__ = ['uv_getaddrinfo', 'callback', 'addrinfo']

    def __init__(self, callback: callable=dummy_callback):
        self.uv_getaddrinfo = ffi.new('uv_getaddrinfo_t*')
        super().__init__(self.uv_getaddrinfo)
        self.callback = callback
        self.addrinfo = []
        pending_requests.add(self)

    def populate(self):
        if self.uv_getaddrinfo.addrinfo:
            self.addrinfo = unpack_addrinfo(self.uv_getaddrinfo.addrinfo)
            self.uv_getaddrinfo.addrinfo = ffi.NULL


def getaddrinfo(host: str, port: int, family: int=0, socktype: int=0, protocol: int=0,
                flags: int=0, callback: callable=None, loop: Loop=None):
    loop = loop or Loop.default_loop()

    request = GetAddrInfo(callback)

    c_hints = ffi.new('struct addrinfo*')
    c_hints.ai_family = family
    c_hints.ai_socktype = socktype
    c_hints.ai_protocol = protocol
    c_hints.ai_flags = flags

    c_require(request.uv_getaddrinfo, c_hints)

    info_callback = getaddrinfo_callback if callback else ffi.NULL

    service = str(port).encode()

    code = lib.uv_getaddrinfo(loop.uv_loop, request.uv_getaddrinfo, info_callback,
                              host.encode(), service, c_hints)

    if code < 0: raise UVError(code)

    if callback is None:
        request.populate()
        return request.addrinfo

    return request


@ffi.callback('uv_getnameinfo_cb')
def getnameinfo_callback(uv_getnameinfo, status, c_hostname, c_service):
    request = detach(uv_getnameinfo)
    hostname = ffi.string(c_hostname).decode()
    service = ffi.string(c_service).decode()
    request.callback(request, status, hostname, service)


@RequestType.GETNAMEINFO
class GetNameInfo(Request):
    __slots__ = ['getnameinfo', 'callback']

    def __init__(self, callback: callable=dummy_callback):
        self.getnameinfo = ffi.new('uv_getnameinfo_t*')
        super().__init__(self.getnameinfo)
        self.callback = callback
        pending_requests.add(self)

    @property
    def host(self):
        return ffi.string(self.getnameinfo.host).decode()

    @property
    def service(self):
        return ffi.string(self.getnameinfo.service).decode()


def getnameinfo(ip: str, port: int, flags: int=0, callback: callable=None,
                loop: Loop=None):
    loop = loop or Loop.default_loop()

    request = GetNameInfo(callback)
    info_callback = getnameinfo_callback if callback else ffi.NULL
    c_sockaddr = ip_addr(ip, port)

    code = lib.uv_getnameinfo(loop.uv_loop, request.getnameinfo, info_callback,
                              c_sockaddr, flags)

    if code < 0: raise UVError(code)

    if callback is None:
        return NameInfo(request.host, request.service)

    return request
