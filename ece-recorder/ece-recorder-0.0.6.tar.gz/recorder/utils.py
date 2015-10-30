#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

from string import Formatter

class EmptyNoneType(object):

    def __nonzero__(self):
        return False

    def __str__(self):
        return ''

    def __getattr__(self, name):
        return EmptyNone

    def __getitem__(self, idx):
        return EmptyNone

EmptyNone = EmptyNoneType()

class EmptyNoneFormatter(Formatter):

    def get_value(self, field_name, args, kwds):
        v = Formatter.get_value(self, field_name, args, kwds)
        if v is None:
            return EmptyNone
        return v

def format(string, *args, **kwargs):
    return EmptyNoneFormatter().format(string, *args, **kwargs)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
