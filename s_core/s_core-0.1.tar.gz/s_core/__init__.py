# -*- coding: utf-8 -*-
"""
s_core
========
    s_core core decomposition of complex network in weigthed graph
"""
__author__   = 'Moreno Bonaventura <morenobonaventura@gmail.com>'

import sys

if sys.version_info[:2] < (2, 6):
    m = "Python version 2.6 or later is required for s_core (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys


#These are import orderwise
import s_core.weighted_core_number
from s_core.weighted_core_number import *
