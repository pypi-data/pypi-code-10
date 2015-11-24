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

from .error import UVError
from .handle import HandleType, Handle
from .library import ffi, lib, detach
from .loop import Loop


@ffi.callback('uv_timer_cb')
def _timer_callback(uv_handle):
    handle = detach(uv_handle)
    if handle.on_timeout: handle.on_timeout(handle)


@HandleType.TIMER
class Timer(Handle):
    __slots__ = ['timer', 'on_timeout']

    def __init__(self, loop: Loop=None, on_timeout: callable=None):
        self.timer = ffi.new('uv_timer_t*')
        self.on_timeout = on_timeout
        super().__init__(self.timer, loop)
        lib.uv_timer_init(self.loop.uv_loop, self.timer)

    @property
    def repeat(self) -> int:
        return lib.uv_timer_get_repeat(self.timer)

    @repeat.setter
    def repeat(self, repeat: int):
        lib.uv_timer_set_repeat(self.timer, repeat)

    def start(self, timeout: int, callback: callable=None, repeat: int=0):
        if callback is not None: self.on_timeout = callback
        lib.uv_timer_start(self.timer, _timer_callback, timeout, repeat)

    def stop(self):
        lib.uv_timer_stop(self.timer)

    def again(self):
        code = lib.uv_timer_again(self.timer)
        if code < 0: raise UVError(code)
