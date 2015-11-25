# -*- coding: utf-8 -*-
u"""
This module implements the class that deals with tables.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from builtins import super
from future import standard_library
standard_library.install_aliases()
from .base_classes import LatexObject, Container, Command, UnsafeCommand, \
    Float, Environment
from .package import Package
from .errors import TableRowSizeError
from .utils import dumps_list, NoEscape, escape_latex

from collections import Counter
import re


def _get_table_width(table_spec):
    u"""Calculate the width of a table based on its spec.

    Args
    ----
    table_spec: str
        The LaTeX column specification for a table.


    Returns
    -------
    int
        The width of a table which uses the specification supplied.
    """

    column_letters = [u'l', u'c', u'r', u'p', u'm', u'b']

    # Remove things like {\bfseries}
    cleaner_spec = re.sub(ur'{[^}]*}', u'', table_spec)
    spec_counter = Counter(cleaner_spec)

    return sum(spec_counter[l] for l in column_letters)


class Tabular(Environment):
    u"""A class that represents a tabular."""

    _repr_attributes_mapping = {
        u'table_spec': u'arguments',
        u'pos': u'options',
    }

    def __init__(self, table_spec, data=None, pos=None, **kwargs):
        u"""
        Args
        ----
        table_spec: str
            A string that represents how many columns a table should have and
            if it should contain vertical lines and where.
        pos: list

        References
        ----------
        * https://en.wikibooks.org/wiki/LaTeX/Tables#The_tabular_environment
        """

        self.width = _get_table_width(table_spec)

        super(Tabular, self).__init__(data=data, options=pos,
                         arguments=table_spec, **kwargs)

    def add_hline(self, start=None, end=None):
        u"""Add a horizontal line to the table.

        Args
        ----
        start: int
            At what cell the line should begin
        end: int
            At what cell the line should end
        """

        if start is None and end is None:
            self.append(NoEscape(ur'\hline'))
        else:
            if start is None:
                start = 1
            elif end is None:
                end = self.width

            if self.escape:
                start = escape_latex(start)
                end = escape_latex(end)

            self.append(UnsafeCommand(u'cline', start + u'-' + end))

    def add_empty_row(self):
        u"""Add an empty row to the table."""

        self.append(NoEscape((self.width - 1) * u'&' + ur'\\'))

    def add_row(self, cells, **_3to2kwargs):
        if 'strict' in _3to2kwargs: strict = _3to2kwargs['strict']; del _3to2kwargs['strict']
        else: strict = True
        if 'mapper' in _3to2kwargs: mapper = _3to2kwargs['mapper']; del _3to2kwargs['mapper']
        else: mapper = None
        if 'escape' in _3to2kwargs: escape = _3to2kwargs['escape']; del _3to2kwargs['escape']
        else: escape = None
        u"""Add a row of cells to the table.

        Args
        ----
        cells: iterable, such as a `list` or `tuple`
            Each element of the iterable will become a the content of a cell.
        mapper: callable
            A function that should be called on all entries of the list after
            converting them to a string, for instance bold
        strict: bool
            Check for correct count of cells in row or not.
        """

        if escape is None:
            escape = self.escape

        # Propagate packages used in cells
        for c in cells:
            if isinstance(c, LatexObject):
                for p in c.packages:
                    self.packages.add(p)

        # Count cell contents
        cell_count = 0

        for c in cells:
            if isinstance(c, MultiColumn):
                cell_count += c.size
            else:
                cell_count += 1

        if strict and cell_count != self.width:
            msg = u"Number of cells added to table ({}) " \
                u"did not match table width ({})".format(cell_count, self.width)
            raise TableRowSizeError(msg)

        self.append(dumps_list(cells, escape=escape, token=u'&',
                               mapper=mapper) + NoEscape(ur'\\'))


class MultiColumn(Container):
    u"""A class that represents a multicolumn inside of a table."""

    # TODO: Make this subclass CommandBase and Container

    def __init__(self, size, **_3to2kwargs):
        if 'data' in _3to2kwargs: data = _3to2kwargs['data']; del _3to2kwargs['data']
        else: data = None
        if 'align' in _3to2kwargs: align = _3to2kwargs['align']; del _3to2kwargs['align']
        else: align = u'c'
        u"""
        Args
        ----
        size: int
            The amount of columns that this cell should fill.
        align: str
            How to align the content of the cell.
        data: str, list or `~.LatexObject`
            The content of the cell.
        """

        self.size = size
        self.align = align

        super(MultiColumn, self).__init__(data=data)

    def dumps(self):
        u"""Represent the multicolumn as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        args = [self.size, self.align, self.dumps_content()]
        string = Command(self.latex_name, args).dumps()

        return string


class MultiRow(Container):
    u"""A class that represents a multirow in a table."""

    # TODO: Make this subclass CommandBase and Container

    packages = [Package(u'multirow')]

    def __init__(self, size, **_3to2kwargs):
        if 'data' in _3to2kwargs: data = _3to2kwargs['data']; del _3to2kwargs['data']
        else: data = None
        if 'width' in _3to2kwargs: width = _3to2kwargs['width']; del _3to2kwargs['width']
        else: width = u'*'
        u"""
        Args
        ----
        size: int
            The amount of rows that this cell should fill.
        width: str
            Width of the cell. The default is ``*``, which means the content's
            natural width.
        data: str, list or `~.LatexObject`
            The content of the cell.
        """

        self.size = size
        self.width = width

        super(MultiRow, self).__init__(data=data)

    def dumps(self):
        u"""Represent the multirow as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        args = [self.size, self.width, self.dumps_content()]
        string = Command(self.latex_name, args).dumps()

        return string


class Table(Float):
    u"""A class that represents a table float."""


class Tabu(Tabular):
    u"""A class that represents a tabu (more flexible table)."""

    packages = [Package(u'tabu')]


class LongTable(Tabular):
    u"""A class that represents a longtable (multipage table)."""

    packages = [Package(u'longtable')]


class LongTabu(LongTable, Tabu):
    u"""A class that represents a longtabu (more flexible multipage table)."""
