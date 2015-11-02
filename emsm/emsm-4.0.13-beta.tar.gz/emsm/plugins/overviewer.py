#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2014-2015 Benedikt Schmitt <benedikt@benediktschmitt.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
About
-----

This plugins integrates the overviewer mapper into the EMSM.
"""


# std
import os
import sys
import subprocess
import logging

# third party
import termcolor

# local
import emsm
from emsm.core.base_plugin import BasePlugin


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = OSError


PLUGIN = "Overviewer"

log = logging.getLogger(__file__)


class Overviewer(BasePlugin):

    VERSION = "4.0.0-beta"

    DESCRIPTION = __doc__

    def __init__(self, app, name):
        """
        """
        BasePlugin.__init__(self, app, name)
        self._setup_argparser()


        return None

    def _setup_argparser(self):
        """
        Sets the argument parser up.
        """
        parser = self.argparser()
        parser.description = "Integrates the *overviewer* mapper into the EMSM."
        return None

    def _check_overviewer(self):

    def _overviewer(self, args):
        """
        """


    def run(self, args):
        """
        """
        # Run the mapper for all selected worlds in alphabetical order.
        worlds = self.app().worlds().get_selected()
        worlds.sort(key = lambda w: w.name())
        for world in worlds:
            print(world)
        return None
