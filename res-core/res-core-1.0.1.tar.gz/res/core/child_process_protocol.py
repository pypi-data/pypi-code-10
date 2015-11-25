"""
Resystem common service package.
Released under New BSD License.
Copyright © 2015, Vadim Markovtsev :: Angry Developers LLC
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Angry Developers LLC nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL VADIM MARKOVTSEV BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


import asyncio
import sys
import os

from .logger import Logger


class ChildProcessProtocol(asyncio.SubprocessProtocol, Logger):
    def __init__(self, children, argv):
        super(ChildProcessProtocol, self).__init__()
        self._children = children
        self._argv = argv
        self.terminating = False

    @property
    def children(self):
        return self._children

    @property
    def transport(self):
        return self.children[self]

    def pipe_data_received(self, fd, data):
        os.write(fd, data)

    def process_exited(self):
        if self.terminating:
            self.info("Process %d exited with return code %d",
                      self.transport.get_pid(),
                      self.transport.get_returncode())
            return
        self.warning("Process %d exited with return code %d => restarting...",
                     self.transport.get_pid(), self.transport.get_returncode())
        del self.children[self]
        asyncio.async(self.restart())

    @asyncio.coroutine
    def restart(self):
        t, p = yield from asyncio.get_event_loop().subprocess_exec(
            lambda: ChildProcessProtocol(self.children, self._argv),
            sys.executable, *self._argv, stdin=None)
        self.children[p] = t
