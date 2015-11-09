#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

def wrap(*lines, **options):
    """ Combines the lines given in the list argument into a single string 
    wrapped to fit inside an 80-character (by default) display.  Both the 
    indentation and the terminal width can be controlled using keyword 
    arguments. """

    indent = options.get('indent', 0) * ' '
    columns = options.get('columns', 79)

    input = ''.join(lines)
    words = re.split('( )+', input)

    line = indent
    lines = []

    for word in words:
        if len(line) + len(word) + 1 < columns:
            line += word
        else:
            lines.append(line)
            line = indent + word.strip()

    lines.append(line)

    return '\n'.join(lines)

def plural(count, singular, plural=None):
    if plural is None: plural = singular + 's'
    return singular if count == 1 else plural

def indent(string, indent='  '):
    return indent + string.replace('\n', '\n' + indent)

def table(format, title, table):
    """
    Print tabular data nicely.

    Parameters
    ----------
    format: str
        The alignment of each column.  The given string should contain one 
        letter for each column.  Only 'l', 'c', and 'r' (for left, center and 
        right alignment respectively) are understood.  If no format is 
        specified, all of the columns will be left-aligned.  Leading spaces are 
        interpreted as an indent.

    title: str
        The title of the table.  Will be printed first and separated from the 
        rest of the table by and underline.

    table: 2D iterable
        The tabular data to be formatted.  Any two dimensional data structure 
        (e.g. list-of-lists, list-of-tuples, etc.) will be understood.  Strings 
        in the first iterable are treated specially.  They are assumed to 
        represent horizontal rules, and so are expanded to the length of the 
        full table and printed alone on the line.
    """

    indent = ' ' * (len(format) - len(format.strip()))
    format = format.strip()

    # Make sure everything in the table is a string.

    for i, row in enumerate(table):
        for j, cell in enumerate(row):
            table[i][j] = str(cell)

    # Find the widest cells in each column.

    column_widths = {}

    for row in table:
        for i, cell in enumerate(row):
            if i not in column_widths or len(cell) > column_widths[i]:
                column_widths[i] = len(cell)

    # Print the table.

    print(indent + title)
    print(indent + '=' * max(len(title), sum(column_widths.values()) + len(column_widths) - 1))

    for row in table:
        for i, cell in enumerate(row):
            column_width = column_widths[i]
            padding = ' ' * (column_width - len(cell))
            if format[i] == 'l': cell_text = cell + padding
            if format[i] == 'r': cell_text = padding + cell
            if i == 0: cell_text = indent + cell_text
            print(cell_text, end=' ')
        print()


if __name__ == "__main__":

    print(wrap(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ',
            'lobortis posuere rutrum. Nam eu aliquam dolor. Fusce eleifend ',
            'facilisis nisi in blandit. Donec vitae turpis ipsum. In leo ',
            'justo, sollicitudin id tristique at, accumsan vitae nunc. In ',
            'dapibus, lorem sed congue porta, urna enim vulputate nunc, sit ',
            'amet luctus elit lectus vitae ipsum. Maecenas at velit velit. ',
            'Ut dignissim massa sit amet nisl pretium quis pharetra eros ',
            'pharetra. Nulla scelerisque arcu et sapien commodo ac mollis ',
            'turpis facilisis. Aenean ut justo at nibh posuere pulvinar. ',
            'Pellentesque ornare laoreet libero eget vulputate. Fusce ',
            'vehicula, metus ac commodo adipiscing, turpis eros semper ',
            'dolor, vel scelerisque purus tellus quis leo. Donec pulvinar ',
            'ullamcorper arcu, quis scelerisque orci ornare nec. Donec ',
            'vitae urna ac arcu ultricies posuere. Morbi fermentum molestie ',
            'libero, eu ultricies orci placerat eget.', 
            columns=40, indent=4))
