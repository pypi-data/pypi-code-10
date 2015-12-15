#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import itertools

import labkit.conformer.conformer

def list_opts():
    return [
        ('DEFAULT',
         itertools.chain(labkit.OPTS,
                         labkit.OPTS,)),
        ('api',
         itertools.chain(labkit.api.OPTS,
                         [labkit.API_OPT])),
        ]
# list_opts()
