# -*- coding: utf-8 -*-
u"""
This module implements the classes that deal with LaTeX lists.

These lists are specifically enumerate, itemize and description.

..  :copyright: (c) 2015 by Sean McLemon.
    :license: MIT, see License for more details.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from .base_classes import Environment, Command


class List(Environment):
    u"""A base class that represents a list."""

    def add_item(self, s):
        u"""Add an item to the list.

        Args
        ----
        s: str or `~.LatexObject`
            The item itself.
        """
        self.append(Command(u'item'))
        self.append(s)


class Enumerate(List):
    u"""A class that represents an enumerate list."""


class Itemize(List):
    u"""A class that represents an itemize list."""


class Description(List):
    u"""A class that represents a description list."""

    def add_item(self, label, s):
        u"""Add an item to the list.

        Args
        ----
        label: str
            Description of the item.
        s: str or `~.LatexObject`
            The item itself.
        """
        self.append(Command(u'item', options=label))
        self.append(s)
