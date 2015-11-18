# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2014)
#
# This file is part of GWpy.
#
# GWpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWpy.  If not, see <http://www.gnu.org/licenses/>.

"""Utilities for the GWpy command-line interface (CLI)
"""

import argparse

from .. import version

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'
__version__ = version.version


class GPSAction(argparse.Action):
    """Custom `~argparse.Action` to convert date strings (or times) to GPS

    The input values are passed to the `~gwpy.time.to_gps` method which
    will return a `~gwpy.time.LIGOTimeGPS` output.

    See Also
    --------
    argparse.Action
        for details on how to use this object
    """
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            values = float(values)
        except (TypeError, ValueError):
            pass
        setattr(namespace, self.dest, to_gps(values))
