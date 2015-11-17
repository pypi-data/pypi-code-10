# -*- coding: utf-8 -*-
# :Project:   metapensiero.odt2sphinx
# :Created:   ven 13 nov 2015 13:47:57 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   Python Software Foundation License
# :Copyright: Copyright (C) 2015 Lele Gaifax
#

class AsciiTable(object):
    def __init__(self, nrows, ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.rows = []

    def add_row(self, is_header):
        self.rows.append(AsciiRow(len(self.rows), is_header, self.ncols))

    def __getitem__(self, row_col):
        row, col = row_col
        return self.rows[row][col]

    def __setitem__(self, row_col, cell):
        row, col = row_col
        self.rows[row][col] = cell

    def __repr__(self):
        #return '\n' + '\n'.join(repr(r) for r in self.rows)
        return self.render()

    def render(self):
        col_widths = [0] * self.ncols
        row_heights = [0] * self.nrows

        # First pass: compute max width and height considering only single-col/row cells
        for r, row in enumerate(self.rows):
            for c, cell in enumerate(row.cells):
                if cell.columns_span == 1 and cell.width:
                    col_widths[c] = max(col_widths[c], cell.width)
                if cell.rows_span == 1 and cell.height:
                    row_heights[r] = max(row_heights[r], cell.height)

        # Second pass: considering only multi-col/multi-row cells, distribute
        # extra-width/height on existing sizes
        for row in self.rows:
            for cell in row.cells:
                if cell.master is None:
                    if cell.columns_span > 1 and cell.width:
                        width = sum(col_widths[c]
                                    for c in range(cell.column,
                                                   cell.column+cell.columns_span))
                        width += 3 * (cell.columns_span - 1)
                        if cell.width > width:
                            tot_width = 3 * (cell.columns_span - 1)
                            enlarge_by = (cell.width - width) // cell.columns_span + 1
                            for c in range(cell.column, cell.column+cell.columns_span):
                                tot_width += col_widths[c]
                                if tot_width + enlarge_by > cell.width:
                                    enlarge_by = cell.width - tot_width
                                col_widths[c] += enlarge_by
                                tot_width += enlarge_by
                    if cell.rows_span > 1 and cell.height:
                        height = sum(row_heights[r]
                                     for r in range(cell.row, cell.row+cell.rows_span))
                        height += cell.rows_span - 1
                        if cell.height > height:
                            tot_height = cell.rows_span - 1
                            raise_by = (cell.height - height) // cell.rows_span + 1
                            for r in range(cell.row, cell.row+cell.rows_span):
                                tot_height += row_heights[r]
                                if tot_height + raise_by > cell.height:
                                    raise_by = cell.height - tot_height
                                row_heights[r] += raise_by
                                tot_height += raise_by

        hrows = 0
        for row in self.rows:
            if row.is_header:
                hrows += 1
            else:
                break

        rows = []

        for r, row in enumerate(self.rows):
            if not rows:
                rows.append(row.render_horizontal_border(col_widths))
            rows.append(row.render(row_heights[r], col_widths))
            hrows -= 1
            char = '=' if hrows == 0 else '-'
            rows.append(row.render_horizontal_border(col_widths, char=char))

        return '\n' + '\n'.join(rows)


class AsciiRow(object):
    def __init__(self, row, is_header, ncols):
        self.row = row
        self.is_header = is_header
        self.cells = [None] * ncols

    def __getitem__(self, col):
        return self.cells[col]

    def __setitem__(self, col, cell):
        self.cells[col] = cell

    def __repr__(self):
        return ' | '.join(repr(c) for c in self.cells)

    def render_horizontal_border(self, col_widths, char='-'):
        row = []
        for c, cell in enumerate(self.cells):
            if cell.columns_span == 1:
                width = col_widths[c]
            else:
                width = sum(col_widths[c]
                            for c in range(cell.column,
                                           cell.column+cell.columns_span))
                width += 3 * (cell.columns_span - 1)
            mcell = cell.master
            if cell.rows_span > 1 and cell.content:
                content = cell.content.pop(0)
                if self.is_header:
                    content = content.center(width)
                row.append(' %-*s ' % (width, content))
            elif mcell is not None and mcell.rows_span > 1 and mcell.content:
                content = mcell.content.pop(0)
                if self.is_header:
                    content = content.center(width)
                row.append(' %-*s ' % (width, content))
            else:
                row.append((char if cell.rows_span==1 else ' ') * (col_widths[c] + 2))
        return '+' + '+'.join(row) + '+'

    def render(self, row_height, col_widths):
        rows = []
        for r in range(row_height):
            row = ['|']
            for c, cell in enumerate(self.cells):
                if cell.columns_span == 1:
                    width = col_widths[c]
                else:
                    width = sum(col_widths[c]
                                for c in range(cell.column,
                                               cell.column+cell.columns_span))
                    width += 3 * (cell.columns_span - 1)
                if cell.content:
                    content = cell.content.pop(0)
                    if self.is_header:
                        content = content.center(width)
                    row.append(' %-*s ' % (width, content))
                else:
                    mcell = cell.master
                    if mcell is not None and mcell.rows_span > 1 and mcell.content:
                        content = mcell.content.pop(0)
                        if self.is_header:
                            content = content.center(width)
                        row.append(' %-*s ' % (width, content))
                    elif mcell is None or mcell.columns_span == 1:
                        row.append(' ' * (width + 2))
                if cell.columns_span == 1:
                    row.append('|')
            rows.append(''.join(row))
        return '\n'.join(rows)


class AsciiCell(object):
    def __init__(self, row, rows_span, column, columns_span, master=None):
        self.row = row
        self.rows_span = rows_span
        self.column = column
        self.columns_span = columns_span
        self.master = master
        self.content = None
        self.width = self.height = 0

    def setContent(self, content):
        lines = self.content = content.splitlines()
        self.height = len(lines)
        self.width = max(len(l) for l in lines)

    def __repr__(self):
        return '%d,%d:%d,%d%s' % (
            self.row, self.column,
            self.row+self.rows_span-1, self.column+self.columns_span-1,
            "" if self.content is None
            else (' (%dx%d) %r' % (self.height, self.width, self.content[0])))
