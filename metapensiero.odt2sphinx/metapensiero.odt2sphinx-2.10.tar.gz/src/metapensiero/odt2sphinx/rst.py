# -*- coding: utf-8 -*-
# :Project:   metapensiero.odt2sphinx
# :Created:   Mar 10 nov 2015 17:59:15 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   Python Software Foundation License
# :Copyright: Copyright (C) 2015 Lele Gaifax
#

import io
import pathlib
import re
import subprocess
import sys
import textwrap

from .out import make_filename, Emitter, ReSTEmitter, SphinxEmitter


# Special markers used to delimit spans: this is needed because in reST
# there must be a non-word character before and after the inline formatting,
# that is the syntax “something**bold**” is not valid. We therefore add the
# following markers around the spans, and eventually use cleanup_span_edges()
# to either remove them or inject a space.

span_prefix = '\N{ZERO WIDTH SPACE} '
span_prefix_re = re.compile(r'(\w?)( *)' + span_prefix)

span_suffix = ' \N{ZERO WIDTH SPACE}'
span_suffix_re = re.compile(span_suffix + r'( *)(\w?)')

adiacent_spans_1_re = re.compile(r'(\*\*|``)' + span_suffix + span_prefix + r'\1')
adiacent_spans_2_re = re.compile(r'(?<!\*)(\*)' + span_suffix + span_prefix + r'\1(?!\*)')
adiacent_spans_3_re = re.compile(r'(\*\*|``) +\1')
adiacent_spans_4_re = re.compile(r'(?<!\*)(\*) +\1(?!\*)')

line_break = '\N{ZERO WIDTH SPACE}\N{PILCROW SIGN}'
line_break_re = re.compile(line_break)

surrounding_spaces_re = re.compile(r'(\s*)(.*[^\s])(\s*)')
multiple_spaces_re = re.compile('  +')


def _cleanup_prefix(match):
    result = match.group(1)
    if result:
        result += r'\ ' if not match.group(2) else ' '
    else:
        result = match.group(2)
    return result or ' '


def _cleanup_suffix(match):
    result = match.group(2)
    if result:
        result = (r'\ ' if not match.group(1) else ' ') + result
    else:
        result = match.group(1)
    return result


def cleanup_special_markup(text):
    text = adiacent_spans_1_re.sub('', text)
    text = adiacent_spans_2_re.sub('', text)
    text = span_prefix_re.sub(_cleanup_prefix, text)
    text = span_suffix_re.sub(_cleanup_suffix, text)
    text = adiacent_spans_3_re.sub(' ', text)
    text = adiacent_spans_4_re.sub(' ', text)
    text = multiple_spaces_re.sub(' ', text)
    return text.strip() if text != ' ' else ' '


def aggregate(items):
    "Reduce consecutive similar elements to a single one."
    it = iter(items)
    value = next(it)
    for nextvalue in it:
        if isinstance(value, Compound) and value & nextvalue:
            if not getattr(nextvalue, 'already_aggregated', False):
                value += nextvalue
        else:
            yield value
            value = nextvalue
    yield value


class Elements(list):
    def __init__(self):
        self.footer_items = []

    def add_footer_item(self, item):
        self.footer_items.append(item)


class Compound(object):
    has_footer_content = False

    def __init__(self):
        self.items = []
        self.already_aggregated = False

    def append(self, item):
        self.items.append(item)

    def text(self):
        return ''.join(str(item) for item in aggregate(self.items)
                       if not getattr(item, 'already_aggregated', False))

    def __str__(self):
        return self.text()

    def __repr__(self):
        return '<%s: %d items>' % (self.__class__.__name__, len(self.items))

    def __and__(self, other):
        "Determine whether `other` is similar enough that it can be aggregated."
        return False

    def __iadd__(self, other):
        "Aggregate `other` into this element, borrowing its items."
        self.items.extend(other.items)
        # Reset this to false, so for example aggregated Anchors won't produce
        # any footer content
        other.has_footer_content = False
        other.already_aggregated = True
        return self

    def emit(self, output):
        text = str(self)
        if text:
            output.write(text + '\n')


class Text(Compound):
    def text(self):
        return cleanup_special_markup(super().text())

    def __repr__(self):
        text = ''.join(map(str, self.items))
        if len(text) > 20:
            text = text[:20] + '…'
        return '<%s: %r>' % (self.__class__.__name__, text)


class Paragraph(Text):
    def __init__(self, indent=0, wrap=90):
        super().__init__()
        self.indent = indent
        self.wrap = wrap

    def text(self):
        text = super().text()
        if self.wrap:
            text = textwrap.fill(text, self.wrap)
        text = line_break_re.sub('\n\n', text)
        if self.indent:
            text = textwrap.indent(text, '    ' * self.indent)
        return text + '\n'


class Anchor(Text):
    def __init__(self, href, embedded_uri=True):
        super().__init__()
        self.href = href
        self.has_footer_content = not embedded_uri

    def __and__(self, other):
        "Allow aggregation of consecutive anchors pointing to the same href."
        return self.__class__ is other.__class__ and self.href == other.href

    def text(self):
        text = super().text()
        if self.has_footer_content:
            return '`%s`__' % text
        else:
            return '`%s <%s>`_' % (text, self.href)

    def append(self, item):
        # Eliminate font style from the spans, since reST does not handle `*Foo*`_
        if isinstance(item, Span):
            item.font_style = None
        super().append(item)

    def footer_emit(self, output):
        output.write('\n__ %s\n' % self.href)


class Span(Compound):
    def __init__(self, text, font_style, text_position):
        super().__init__()
        self.font_style = font_style
        self.text_position = text_position
        self.items.append(text)

    def __and__(self, other):
        "Allow aggregation of consecutive spans with the same style."
        return self.__class__ is other.__class__ and (
            self.font_style == other.font_style
            and self.text_position == other.text_position)

    def text(self):
        text = super().text()

        # Avoid decorating whitespace-only chunks
        font_style = None if not text.strip() else self.font_style

        if font_style is not None:
            splitted = surrounding_spaces_re.match(text)
            text = splitted.group(2)
            if text:
                # Add special markers around the span, see cleanup_span_edges()
                if font_style in ('italic', 'underline'):
                    text = span_prefix + '*' + text + '*' + span_suffix
                elif font_style == 'bold':
                    text = span_prefix + '**' + text + '**' + span_suffix
                elif font_style == 'fixed':
                    text = span_prefix + '``' + text + '``' + span_suffix
                if splitted.group(1):
                    text = ' ' + text
                if splitted.group(3):
                    text += ' '

        if self.text_position is not None:
            text = span_prefix + ':' + self.text_position + ':`' + text + '`' + span_suffix

        return text


class Heading(Text):
    def __init__(self, decoration):
        super().__init__()
        self.decoration = decoration
        self.footer_items = []

    def text(self):
        title = super().text()
        tlen = len(title)
        if isinstance(self.decoration, tuple):
            tlen += 2
            above, below = self.decoration
            heading = '%s\n %s\n%s\n\n' % (above*tlen, title, below*tlen)
        else:
            heading = '%s\n%s\n\n' % (title, self.decoration*tlen)
        return heading

    def add_footer_item(self, item):
        self.footer_items.append(item)


class Directive(Compound):
    def __init__(self, name, title=None, content=None, **options):
        super().__init__()
        self.name = name
        self.title = title
        self.content = content
        self.options = options

    def __and__(self, other):
        "Allow aggregation of consecutive admonitions."
        return self.__class__ is other.__class__ and self.name == other.name and self.name in {
            "admonition", "attention", "caution", "danger", "error",
            "hint", "important", "note", "tip", "warning" }

    def __iadd__(self, other):
        "Aggregate `other` into this element, concatenating their items."
        self.items.append('')
        self.items.extend(other.items)
        return self

    def text(self):
        result = []
        append = result.append
        if self.title is not None:
            append('.. %s:: %s' % (self.name, self.title))
        else:
            append('.. %s::' % self.name)
        for key in sorted(self.options):
            value = self.options[key]
            if value is not None:
                append('   :%s: %s' % (key, value))
        append('')
        content = '' if self.content is None else self.content + '\n'
        content += '\n'.join(map(str, self.items))
        append(textwrap.indent(content, '   '))
        return '\n'.join(result)


def convert_mf_to_png(content, kind):
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(suffix='.'+kind, delete=False) as f:
        f.write(content)
        mf = pathlib.Path(f.name)

    try:
        try:
            subprocess.check_output(['loffice', '--convert-to', 'png',
                                     '--outdir', str(mf.parent), str(mf)])
        except FileNotFoundError as e:
            raise RuntimeError("Could not convert a %s image to PNG (maybe"
                               " LibreOffice is not installed on the system?):"
                               " %s" % (kind.upper(), e))
    finally:
        mf.unlink()

    png = mf.with_suffix('.png')

    if not png.exists():
        raise RuntimeError("Could not convert a %s image to PNG: most probably you"
                           " have an instance of LibreOffice already running, close"
                           " it and retry please" % kind.upper())

    with png.open('rb') as f:
        content = f.read()
    png.unlink()

    return content


def convert_to_png(content):
    from PIL import Image

    image = Image.open(io.BytesIO(content))
    aspng = io.BytesIO()
    image.save(aspng, 'PNG')

    return aspng.getvalue()


class Image(Directive):
    has_footer_content = True

    def __init__(self, basedir, name, content, width=None, height=None):
        self.original_name = name
        self.original_content = content
        self.path = basedir.joinpath('images', name).with_suffix('.png')
        super().__init__('%s image' % self, self.path, width=width, height=height)

    def __str__(self):
        return '|%s|' % make_filename(str(self.path), False)

    def footer_emit(self, output):
        output.write(self.text())
        output.write('\n')

        if self.path.parent.is_dir():
            content = self.original_content
            endswith = self.original_name.endswith
            if endswith('.wmf'):
                content = convert_mf_to_png(content, 'wmf')
            elif endswith('.svm'):
                content = convert_mf_to_png(content, 'svm')
            elif not self.name.endswith('.png'):
                content = convert_to_png(content)
            with self.path.open('wb') as f:
                f.write(content)


class List(Compound):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind

    def text(self):
        prefix = self.kind + ' '
        pl = len(prefix)
        result = ['']
        for item in self.items:
            text = textwrap.indent(str(item).lstrip(), ' '*pl)
            result.append(prefix + text[pl:])
            # Use the proper autonumeration prefix for the remaining items
            if prefix != '* ' and not prefix.startswith('#'):
                prefix = '#' + prefix[1:]
        return '\n'.join(result)

    def __repr__(self):
        return '<%s kind %r: %d items>' % (self.__class__.__name__, self.kind, len(self.items))


class ListItem(Compound):
    pass


class Table(Compound):
    def __init__(self):
        super().__init__()
        self.column_widths = []

    def __repr__(self):
        return '<%s: %d rows>' % (self.__class__.__name__, len(self.items))

    def add_column(self, width):
        self.column_widths.append(width)

    def rows(self):
        for item in self.items:
            if isinstance(item, TableRow):
                yield item, False
            elif isinstance(item, TableHeader):
                for subitem in item.items:
                    if isinstance(subitem, TableRow):
                        yield subitem, True

    def text(self):
        from .table import AsciiTable, AsciiCell

        rows = list(self.rows())
        nrows = len(rows)
        ncols = 0
        for row, _ in rows:
            ncols = max(len(row.items), ncols)

        table = AsciiTable(nrows, ncols, self.column_widths)
        for row, is_header in rows:
            table.add_row(is_header)

        for r, (row, _) in enumerate(rows):
            freecells = [c for c in range(ncols) if table[r,c] is None]
            for col in row.items:
                c = freecells.pop(0)
                cs = col.columns_span
                if cs > 1:
                    freecells = freecells[cs-1:]
                rs = col.rows_span
                cell = table[r,c] = AsciiCell(r, c, rs, cs)
                cell.set_content(str(col))
                for r1 in range(r, r+rs):
                    for c1 in range(c, c+cs):
                        if table[r1,c1] is None:
                            table[r1,c1] = AsciiCell(r, c, r+rs-r1, c+cs-c1, cell)

        return table.render()


class TableHeader(Compound):
    def __repr__(self):
        return '<%s: %d rows>' % (self.__class__.__name__, len(self.items))


class TableRow(Compound):
    def __repr__(self):
        return '<%s: %d cells>' % (self.__class__.__name__, len(self.items))


class TableRowCell(Compound):
    def __init__(self, rows_span, columns_span):
        super().__init__()
        self.rows_span = rows_span
        self.columns_span = columns_span


class Stack(object):
    def __init__(self, root, debug):
        self.items = [root]
        self.debug = debug
        self.current_heading = None

    @property
    def top(self):
        return self.items[-1]

    def __iadd__(self, item):
        "Add an item to the element on the top of the stack."

        if self.debug:
            print("DEBUG: adding %r to %r" % (item, self.top), file=sys.stderr)

        self.top.append(item)

        if item.has_footer_content:
            (self.current_heading or self.items[0]).add_footer_item(item)

        return self

    def __lshift__(self, item):
        "Push an item on the stack."

        if self.debug:
            if len(self.items) > 1:
                print("DEBUG: stacking %r over %r" % (item, self.top), file=sys.stderr)
            else:
                print("DEBUG: stacking %r" % (item,), file=sys.stderr)

        self.items.append(item)

        if isinstance(item, Heading):
            self.current_heading = item
        elif item.has_footer_content:
            (self.current_heading or self.items[0]).add_footer_item(item)
        return item

    def __invert__(self):
        "Pop an item, if one is present."

        if len(self.items) > 1:
            item = self.items.pop()
            self.top.append(item)
            if self.debug:
                if len(self.items) > 1:
                    print("DEBUG: unstacked %r, left %r" % (item, self.top), file=sys.stderr)
                else:
                    print("DEBUG: unstacked %r" % (item,), file=sys.stderr)
            return item


class Writer(object):
    def __init__(self, target, encoding, download_source_link=False,
                 embed_uris=False, debug=False,
                 ignore_original_column_widths=False):
        self.target = target
        self.encoding = encoding
        self.download_source_link = download_source_link
        self.embed_uris = embed_uris
        self.debug = debug
        self.ignore_original_column_widths = ignore_original_column_widths
        self.elements = Elements()
        self.stack = Stack(self.elements, debug)

        if target != '-':
            if target.suffix == '.rst':
                self.monolithic_output = True
                self.dir = target.parent
            else:
                self.monolithic_output = False
                self.dir = target
        else:
            self.dir = pathlib.Path()

    def add_heading(self, decoration):
        # Headings are top level items, rewind the stack

        while ~self.stack:
            continue

        self.stack << Heading(decoration)

    def title_start(self):
        self.add_heading(('=', '='))

    def title_end(self):
        ~self.stack

    def subtitle_start(self):
        self.add_heading(('-', '-'))

    def subtitle_end(self):
        ~self.stack

    def h0_start(self):
        self.add_heading('#')

    def h0_end(self):
        ~self.stack

    def h1_start(self):
        self.add_heading('=')

    def h1_end(self):
        ~self.stack

    def h2_start(self):
        self.add_heading('-')

    def h2_end(self):
        ~self.stack

    def h3_start(self):
        self.add_heading('~')

    def h3_end(self):
        ~self.stack

    def h4_start(self):
        self.add_heading('+')

    def h4_end(self):
        ~self.stack

    def h5_start(self):
        self.add_heading('`')

    def h5_end(self):
        ~self.stack

    def h6_start(self):
        self.add_heading('^')

    def h6_end(self):
        ~self.stack

    def p_start(self):
        self.stack << Paragraph()

    def p_end(self):
        ~self.stack

    def text(self, text, font_style=None, text_position=None):
        self.stack += Span(text, font_style, text_position)

    def a_start(self, href):
        self.stack << Anchor(href, self.embed_uris)

    def a_end(self):
        ~self.stack

    def image(self, name, content, width=None, height=None):
        self.stack += Image(self.dir, name, content, width, height)

    def highlight_start(self, kind):
        self.stack << Directive(kind)

    def highlight_end(self):
        ~self.stack

    def list_start(self, kind):
        self.stack << List(kind)

    def list_end(self):
        ~self.stack

    def list_item_start(self):
        self.stack << ListItem()

    def list_item_end(self):
        ~self.stack

    def table_start(self):
        self.stack << Table()

    def table_end(self):
        ~self.stack

    def table_header_start(self):
        self.stack << TableHeader()

    def table_header_end(self):
        ~self.stack

    def table_column(self, repeat, width):
        if not self.ignore_original_column_widths:
            for i in range(repeat):
                self.stack.top.add_column(width)

    def row_start(self):
        self.stack << TableRow()

    def row_end(self):
        ~self.stack

    def cell_start(self, rows_span, columns_span):
        self.stack << TableRowCell(rows_span, columns_span)

    def cell_end(self):
        ~self.stack

    def table_of_content(self, title, depth):
        self.stack += Directive('contents', title, depth=depth)

    def writeout(self):
        if self.target == '-':
            emitter = Emitter(self.elements)
        else:
            if not self.dir.is_dir():
                self.dir.mkdir()

            if self.monolithic_output:
                emitter = ReSTEmitter(self.elements, self.target, self.encoding)
            else:
                emitter = SphinxEmitter(self.elements, self.dir, self.encoding,
                                        self.download_source_link)
        emitter()
