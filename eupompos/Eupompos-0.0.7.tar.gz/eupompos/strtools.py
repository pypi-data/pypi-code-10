#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#    Eupompos Copyright (C) 2012 Xavier Faure
#    Contact: suizozukan arrobas orange dot fr
#
#    This file is part of Eupompos.
#    Eupompos is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Eupompos is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Eupompos.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
        ❏Eupompos❏ ./eupompos/strtools.py
        ________________________________________________________________________

        Tools to be used with strings objects.
        ________________________________________________________________________

        o add_prefix_to_lines()
"""

################################################################################
def add_prefix_to_lines(_lines, _prefix):
    """
            add_prefix_to_lines()
            ____________________________________________________________________

            Add a prefix to each line in _lines.

                e.g. :
                        abc\ndef -> PREFIXabc\nPREFIXdef
            ____________________________________________________________________

            PARAMETERS :
                o _lines        : either (str)some lines with \n inside
                                  either a list of (str)lines
                o _prefix       : (str)the prefix to be added

            RETURN VALUE :
                o (str)the expected string.
    """
    res = []

    if isinstance(_lines, str):
        for line in _lines.split("\n"):
            res.append(_prefix+line)

    else:
        for line in _lines:
            res.append(_prefix+line)

    return "\n".join(res)
