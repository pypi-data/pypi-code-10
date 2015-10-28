#!/usr/bin/env python
# encoding: utf-8

#
# The MIT License (MIT)
#
# Copyright (c) 2013-2015 CNRS
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# AUTHORS
# Hervé BREDIN -- http://herve.niderb.fr/

from __future__ import unicode_literals

import simplejson as json
import pyannote.core.json


TVD_JSON = 'tvd'


def object_hook(d):
    """
    Usage
    -----
    >>> with open('file.json', 'r') as f:
    ...   json.load(f, object_hook=object_hook)
    """

    from .episode import Episode

    if TVD_JSON in d:
        if d[TVD_JSON] == 'Episode':
            return Episode.from_json(d)

    d = pyannote.core.json.object_hook(d)

    return d


def load(path):
    with open(path, 'r') as f:
        data = json.load(f, encoding='utf-8', object_hook=object_hook)
    return data


def dump(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, encoding='utf-8', for_json=True)
