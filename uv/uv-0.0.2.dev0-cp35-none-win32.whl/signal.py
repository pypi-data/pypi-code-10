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

from .handle import HandleType, Handle
from .library import ffi, lib, detach
from .loop import Loop

__all__ = ['Signal']


@ffi.callback('uv_signal_cb')
def signal_callback(uv_handle, signum):
    handle = detach(uv_handle)
    if handle.on_signal: handle.on_signal(handle, signum)


@HandleType.SIGNAL
class Signal(Handle):
    __slots__ = ['signal', 'on_signal']

    def __init__(self, loop: Loop=None, on_signal: callable=None):
        self.signal = ffi.new('uv_signal_t*')
        self.on_signal = on_signal
        super().__init__(self.signal, loop)
        lib.uv_signal_init(self.loop.uv_loop, self.signal)

    @property
    def signum(self):
        return self.signal.signum

    def start(self, signum: int, callback=None):
        self.on_signal = callback
        lib.uv_signal_start(self.signal, signal_callback, signum)

    def stop(self):
        lib.uv_signal_stop(self.signal)
