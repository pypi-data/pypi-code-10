# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Define unit tests to test core functionality."""

from __future__ import absolute_import

import importlib

import pytest
from mock import patch
from pkg_resources import EntryPoint

from jsonresolver import JSONResolver


class MockEntryPoint(EntryPoint):
    def load(self):
        if self.name == 'importfail':
            raise ImportError()
        else:
            return importlib.import_module(self.name)


def _mock_entry_points(name):
    data = {
        'espresso': [MockEntryPoint('demo.simple', 'demo.simple')],
        'someotherstuff': [],
        'doubletrouble': [MockEntryPoint('demo.simple', 'demo.simple'),
                          MockEntryPoint('demo.simple', 'demo.simple')],
        'importfail': [MockEntryPoint('importfail',
                                      'test.importfail')],
    }
    names = data.keys() if name is None else [name]
    for key in names:
        for entry_point in data[key]:
            yield entry_point


@patch('pkg_resources.iter_entry_points', _mock_entry_points)
def test_entry_point_group():
    resolver = JSONResolver(entry_point_group='espresso')
    assert resolver.resolve('http://localhost:4000/test') == {'test': 'test'}


def test_plugins():
    resolver = JSONResolver(plugins=['demo.simple'])
    assert resolver.resolve('http://localhost:4000/test') == {'test': 'test'}
