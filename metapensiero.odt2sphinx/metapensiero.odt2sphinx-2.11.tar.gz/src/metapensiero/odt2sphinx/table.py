# -*- coding: utf-8 -*-
# :Project:   metapensiero.odt2sphinx
# :Created:   ven 13 nov 2015 13:47:57 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   Python Software Foundation License
# :Copyright: Copyright (C) 2015 Lele Gaifax
#

class AsciiTable(object):
    def __init__(self, num_rows, num_cols, real_column_widths):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.real_column_widths = real_column_widths
        self.rows = []

    def add_row(self, is_header):
        self.rows.append(AsciiRow(len(self.rows), is_header, self.num_cols))

    def __getitem__(self, row_col):
        row, col = row_col
        return self.rows[row][col]

    def __setitem__(self, row_col, cell):
        row, col = row_col
        self.rows[row][col] = cell

    def render(self):
        col_widths = [0] * self.num_cols
        row_heights = [0] * self.num_rows

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
                if cell.is_master_cell:
                    if cell.columns_span > 1:
                        width = cell.compute_full_width(col_widths) + 1
                        if cell.width > width:
                            tot_width = 3 * (cell.columns_span - 1)
                            enlarge_by = (cell.width - width) // cell.columns_span + 1
                            for c in range(cell.column, cell.column+cell.columns_span):
                                tot_width += col_widths[c]
                                if tot_width + enlarge_by > cell.width:
                                    enlarge_by = cell.width - tot_width
                                col_widths[c] += enlarge_by
                                tot_width += enlarge_by
                    if cell.rows_span > 1:
                        height = cell.compute_full_height(row_heights) + 1
                        if cell.height > height:
                            tot_height = cell.rows_span - 1
                            raise_by = (cell.height - height) // cell.rows_span + 1
                            for r in range(cell.row, cell.row+cell.rows_span):
                                tot_height += row_heights[r]
                                if tot_height + raise_by > cell.height:
                                    raise_by = cell.height - tot_height
                                row_heights[r] += raise_by
                                tot_height += raise_by

        if self.real_column_widths:
            # Compute maximum ratio between between number of characters of each
            # column and its real measure
            max_ratio = 0.0
            for c in range(self.num_cols):
                max_ratio = max(max_ratio, col_widths[c] / self.real_column_widths[c])

            # Now compute new column widths to bring the table layout closer to the original
            adapted_col_widths = []
            for c in range(self.num_cols):
                ratio = col_widths[c] / self.real_column_widths[c]
                if ratio and (max_ratio - ratio) > 0.2:
                    adapted_col_widths.append(int(col_widths[c] * max_ratio / ratio))
                else:
                    adapted_col_widths.append(col_widths[c])
        else:
            adapted_col_widths = col_widths

        hrows = 0
        for row in self.rows:
            if row.is_header:
                hrows += 1
            else:
                break

        rows = []

        for r, row in enumerate(self.rows):
            if not rows:
                rows.append(row.render_horizontal_border(adapted_col_widths))
            rows.append(row.render(row_heights[r], adapted_col_widths))
            hrows -= 1
            char = '=' if hrows == 0 else '-'
            rows.append(row.render_horizontal_border(adapted_col_widths, char=char))

        return '\n' + '\n'.join(rows) + '\n'


class AsciiRow(object):
    def __init__(self, row, is_header, num_cols):
        self.row = row
        self.is_header = is_header
        self.cells = [None] * num_cols

    def __getitem__(self, col):
        return self.cells[col]

    def __setitem__(self, col, cell):
        self.cells[col] = cell

    def render_horizontal_border(self, col_widths, char='-'):
        row = []
        for c, cell in enumerate(self.cells):
            if cell.rows_span > 1:
                if cell.is_master_column:
                    width = cell.compute_full_width(col_widths)
                    line = cell.pop_line()
                    if self.is_header:
                        line = line.center(width)
                    row.append(' %-*s ' % (width, line))
            else:
                row.append(char * (col_widths[c] + 2))
        return '+' + '+'.join(row) + '+'

    def render(self, row_height, col_widths):
        rows = []
        for r in range(row_height):
            row = ['|']
            for c, cell in enumerate(self.cells):
                if cell.is_master_column:
                    width = cell.compute_full_width(col_widths)
                    line = cell.pop_line()
                    if self.is_header:
                        line = line.center(width)
                    row.append(' %-*s ' % (width, line))
                if cell.columns_span == 1:
                    row.append('|')
            rows.append(''.join(row))
        return '\n'.join(rows)


class AsciiCell(object):
    def __init__(self, row, column, rows_span, columns_span, master_cell=None):
        self.row = row
        self.column = column
        self.rows_span = rows_span
        self.columns_span = columns_span
        self.master_cell = master_cell
        self.content_lines = None
        self.width = self.height = 0

    @property
    def is_master_cell(self):
        return self.master_cell is None

    @property
    def is_master_column(self):
        return self.master_cell is None or (self.columns_span == self.master_cell.columns_span)

    def set_content(self, content):
        lines = self.content_lines = content.strip().splitlines() or [""]
        self.height = len(lines)
        self.width = max(len(l) for l in lines)

    def pop_line(self):
        lines = (self.master_cell or self).content_lines
        return lines.pop(0) if lines else ""

    def compute_full_width(self, col_widths):
        if self.columns_span == 1:
            width = col_widths[self.column]
        else:
            width = sum(col_widths[c]
                        for c in range(self.column,
                                       self.column + self.columns_span))
            width += 3 * (self.columns_span - 1)
        return width

    def compute_full_height(self, row_heights):
        if self.rows_span == 1:
            height = row_heights[self.row]
        else:
            height = sum(row_heights[r]
                         for r in range(self.row, self.row + self.rows_span))
            height += self.rows_span - 1
        return height
