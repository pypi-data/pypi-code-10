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

import typing

from .error import UVError
from .handle import HandleType, Handle
from .library import ffi, lib, detach, dummy_callback
from .loop import Loop

__all__ = ['Async']

AsyncCallback = typing.Callable[['Async'], None]


@ffi.callback('uv_async_cb')
def uv_async_cb(uv_async):
    async = detach(uv_async)
    async.callback(async)


@HandleType.ASYNC
class Async(Handle):
    """
    Implements the LibUV async handle. Async handles are the only thread safe
    handles. They allow us to send a callback to the event loop from another
    thread which then gets called from within the event loop's thread.

    :raises UVError: something went wrong during the initialization of the handle

    :ivar uv_async: underlying CFFI async handle

    :param Loop loop: underlying event loop
    """

    __slots__ = ['uv_async', 'callback']

    def __init__(self, loop: Loop = None, callback: callable = None):
        self.uv_async = ffi.new('uv_async_t*')
        self.callback = callback or dummy_callback
        super().__init__(self.uv_async, loop)
        code = lib.uv_async_init(self.loop.uv_loop, self.uv_async, uv_async_cb)
        if code < 0: raise UVError(code)

    def send(self, callback: callable=None):
        """
        Wakeup the event loop and overwrite the current callback if specified. After
        the event loop woke up the callback will be called from within the event
        loop's thread. Warning: It is not guaranteed that the callback is called
        once for every send call.

        This method is thread safe and raises UVError if anything goes wrong
        during the wakeup request.

        :param callback: overwrite the previous set callback
        :param callback: overwrite the previous set callback

        :raises UVError: something went wrong during the initialization of the handle
        :raises OSError: fasdfd
        """
        self.callback = callback or self.callback
        code = lib.uv_async_send(self.uv_async)
        if code < 0: raise UVError(code)

    __call__ = send
