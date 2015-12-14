#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Martin Raspaud

# Author(s):

#   Martin Raspaud <martin.raspaud@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
"""

from ConfigParser import RawConfigParser
import sys
from collections import OrderedDict
cfg = RawConfigParser()
cfg.read(sys.argv[1])

res = dict()

for sec in cfg.sections():
    hdr, secname = sec.split(":")
    stuff = dict()
    for key, val in cfg.items(sec):
        if "," in val:
            stuff[key] = [x.strip() for x in val.split(",")]
        else:
            stuff[key] = val
    if "name" not in stuff:
        stuff["name"] = secname
    if hdr in res:
        res[hdr].append(stuff)
    else:
        res[hdr] = [stuff]

import yaml
print yaml.dump(res, default_flow_style=False)
