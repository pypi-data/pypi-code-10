# -*- coding: utf-8 -*-
# :Project:   metapensiero.odt2sphinx
# :Created:   Mar 10 nov 2015 17:59:15 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   Python Software Foundation License
# :Copyright: Copyright (C) 2015 Lele Gaifax
#

import io
import itertools
import pathlib
import re
import sys
import textwrap


# Special markers used to delimit spans: this is needed because in reST
# there must be a non-word character before and after the inline formatting,
# that is the syntax “something**bold**” is not valid. We therefore add the
# following markers around the spans, and eventually use cleanup_span_edges()
# to either remove them or inject a space.

span_prefix = '\N{ZERO WIDTH SPACE} '
span_prefix_re = re.compile(r'(\w?)( *)' + span_prefix)

span_suffix = ' \N{ZERO WIDTH SPACE}'
span_suffix_re = re.compile(span_suffix + r'( *)(\w?)')

line_break = '\N{ZERO WIDTH SPACE}\N{PILCROW SIGN}'
line_break_re = re.compile(line_break)

surrounding_spaces_re = re.compile(r'(\s*)(.+)(\s*)')
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
    text = span_prefix_re.sub(_cleanup_prefix, text)
    text = span_suffix_re.sub(_cleanup_suffix, text)
    text = line_break_re.sub('\n\n', text)
    text = multiple_spaces_re.sub(' ', text)
    return text.strip()


invalid_filename_characters_re = re.compile(r'[^-\w]+')


def make_filename(text, unique=True, generated_filenames=set()):
    fname = text.encode('ascii', 'replace').decode()
    fname = invalid_filename_characters_re.sub('_', fname).strip('_')
    if unique:
        if fname in generated_filenames:
            for n in itertools.count(1):
                nfname = '%s%s' % (fname, n)
                if nfname not in generated_filenames:
                    fname = nfname
                    break
        generated_filenames.add(fname)
    return fname


class Compound(object):
    def __init__(self):
        self.items = []
        self.append = self.items.append

    def __str__(self):
        return ''.join(map(str, self.items))

    def __repr__(self):
        content = self.__str__()
        if len(content) > 50:
            content = content[:20] + ' … ' + content[-20:]
        return '<%s: %r>' % (self.__class__.__name__, content)

    def emit(self, output):
        output.write(self.__str__() + '\n')

    def footer_emit(self, output):
        pass


class Text(Compound):
    def __str__(self):
        return self.text

    @property
    def text(self):
        return cleanup_special_markup(super().__str__())


class Paragraph(Compound):
    def __init__(self, indent=0, wrap=90):
        super().__init__()
        self.indent = indent
        self.wrap = wrap

    def __str__(self):
        text = super().__str__()
        if self.wrap:
            text = textwrap.fill(text, self.wrap)
        if self.indent:
            text = textwrap.indent(text, '    ' * self.indent)
        return cleanup_special_markup(text) + '\n'


class Anchor(Text):
    def __init__(self, href):
        super().__init__()
        self.href = href

    def __str__(self):
        return '`%s <%s>`_' % (self.text, self.href)


class Span(Compound):
    def __init__(self, text, font_style, text_position):
        super().__init__()

        # Avoid decorating whitespace-only chunks
        if not text.strip():
            font_style = None

        if font_style is not None:
            splitted = surrounding_spaces_re.match(text)
            text = splitted.group(2)
            if text:
                # Add special markers around the span, see cleanup_span_edges()
                if font_style == 'italic':
                    text = span_prefix + '*' + text + '*' + span_suffix
                elif font_style == 'underline':
                    text = span_prefix + '*' + text + '*' + span_suffix
                elif font_style == 'bold':
                    text = span_prefix + '**' + text + '**' + span_suffix
                elif font_style == 'fixed':
                    text = span_prefix + '``' + text + '``' + span_suffix
                if splitted.group(1):
                    text = ' ' + text
                if splitted.group(3):
                    text += ' '

        if text_position is not None:
            text = span_prefix + ':' + text_position + ':`' + text + '`' + span_suffix

        self.append(text)


class Heading(Text):
    def __init__(self, decoration):
        super().__init__()
        self.decoration = decoration
        self.footer_items = []

    def __str__(self):
        title = self.text
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

    def __str__(self):
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
        if self.content is not None:
            content = self.content + '\n' + super().__str__()
        else:
            content = super().__str__()
        append(textwrap.indent(content, '   '))
        return '\n'.join(result)


def convert_mf_to_png(content):
    from subprocess import run
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(suffix='.mf', delete=False) as f:
        f.write(content)
        mf = pathlib.Path(f.name)

    try:
        try:
            run(['loffice', '--convert-to', 'png', '--outdir', str(mf.parent), str(mf)])
        except FileNotFoundError as e:
            raise RuntimeError("Could not convert a MF image to PNG (maybe"
                               " LibreOffice is not installed on the system?): %s" % e)
    finally:
        mf.unlink()

    png = mf.with_suffix('.png')

    if not png.exists():
        raise RuntimeError("Could not convert a MF image to PNG: most probably you"
                           " have an instance of LibreOffice already running, close"
                           " it and retry please")

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
    def __init__(self, basedir, name, content, width=None, height=None):

        self.original_name = name
        self.original_content = content
        self.path = basedir.joinpath('images', name).with_suffix('.png')
        super().__init__('%s image' % self, self.path, width=width, height=height)

    def __str__(self):
        return '|%s|' % make_filename(str(self.path), False)

    def __repr__(self):
        return super().__str__()

    def footer_emit(self, output):
        output.write(super().__str__())
        output.write('\n')

        if self.path.parent.is_dir():
            content = self.original_content
            endswith = self.original_name.endswith
            if endswith('.wmf') or endswith('.svm') or content.startswith(b'VCLMTF'):
                content = convert_mf_to_png(content)
            elif not self.name.endswith('.png'):
                content = convert_to_png(content)
            with self.path.open('wb') as f:
                f.write(content)


class List(Compound):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind

    def __str__(self):
        prefix = self.kind + ' '
        pl = len(prefix)
        result = ['']
        for item in self.items:
            text = textwrap.indent(str(item), ' '*pl)
            result.append(prefix + text[pl:])
            # Use the proper autonumeration prefix for the remaining items
            if prefix != '* ' and not prefix.startswith('#'):
                prefix = '#' + prefix[1:]
        return '\n'.join(result)


class ListItem(Compound):
    pass


class Table(Compound):
    def rows(self):
        for item in self.items:
            if isinstance(item, TableRow):
                yield item, False
            elif isinstance(item, TableHeader):
                for subitem in item.items:
                    if isinstance(subitem, TableRow):
                        yield subitem, True

    def __repr__(self):
        return '<%s: %r>' % (self.__class__.__name__,
                             '\n'.join(repr(row) for row,_ in self.rows()))

    def __str__(self):
        from .table import AsciiTable, AsciiCell

        rows = list(self.rows())
        nrows = len(rows)
        ncols = 0
        for row, _ in rows:
            ncols = max(len(row.items), ncols)

        table = AsciiTable(nrows, ncols)
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
                cell = table[r,c] = AsciiCell(r, rs, c, cs)
                cell.setContent(str(col))
                for r1 in range(r, r+rs):
                    for c1 in range(c, c+cs):
                        if table[r1,c1] is None:
                            table[r1,c1] = AsciiCell(r, r+rs-r1, c, c+cs-c1, cell)

        return table.render()


class TableRow(Compound):
    def __repr__(self):
        cells = []
        for cell in self.items:
            cs = cell.columns_span
            rs = cell.rows_span
            s = str(cell).strip()
            cells.append('%dx%d : %r' % (cs, rs, s))
        return '<%s: %r>' % (self.__class__.__name__, ' | '.join(cells))


class TableHeader(Compound):
    pass


class TableRowCell(Compound):
    def __init__(self, rows_span, columns_span):
        super().__init__()
        self.rows_span = rows_span
        self.columns_span = columns_span


class Stack(object):
    def __init__(self, root, debug):
        self.items = [root]
        self.item = root
        self.debug = debug

    def __getattr__(self, attr):
        return getattr(self.item, attr)

    ## Use special operator methods, to avoid clashes between
    ## push and pop actions and methods of the current item

    def __lshift__(self, item):
        "Push an item on the stack."

        if self.debug:
            if len(self.items) > 1:
                print("DEBUG: stacking %r over %r" % (item, self.item), file=sys.stderr)
            else:
                print("DEBUG: stacking %r" % (item,), file=sys.stderr)
        self.items.append(item)
        self.item = item
        return item

    def __invert__(self):
        "Pop an item, if one is present."

        if len(self.items) > 1:
            item = self.items.pop()
            self.item = self.items[-1]
            self.item.append(item)
            if self.debug:
                if len(self.items) > 1:
                    print("DEBUG: unstacked %r, left %r" % (item, self.item), file=sys.stderr)
                else:
                    print("DEBUG: unstacked %r" % (item,), file=sys.stderr)
            return item


class Emitter(object):
    def __init__(self, elements, output=None):
        self.elements = elements
        self.output = output or sys.stdout
        self.current_heading = None

    def change_heading(self, heading):
        if self.current_heading is not None:
            for element in self.current_heading.footer_items:
                element.footer_emit(self.output)
        self.current_heading = heading

    def __call__(self):
        for element in self.elements:
            if isinstance(element, Heading):
                self.change_heading(element)
            element.emit(self.output)
        self.change_heading(None)


class MonolithicEmitter(Emitter):
    def __init__(self, elements, target, encoding):
        self.encoding = encoding
        output = target.open('w', encoding=encoding)
        output.write('.. -*- coding: %s -*-\n\n' % encoding)
        super().__init__(elements, output)
        imgdir = target.parent / 'images'
        if not imgdir.is_dir():
            imgdir.mkdir()


class SphinxEmitter(MonolithicEmitter):
    def __init__(self, elements, dir, encoding, download_source_link):
        super().__init__(elements, dir / 'index.rst', encoding)
        self.dir = dir
        self.index = self.output
        self.filenames = []
        if download_source_link:
            self.download_source = Directive('only', 'html',
                                             "Original document:"
                                             " :download:`%s <%s>`" %
                                             (download_source_link.name,
                                              download_source_link))
        else:
            self.download_source = None

    def change_heading(self, heading):
        super().change_heading(heading)

        if heading is None:
            # finalization
            self.index.write(str(Directive('toctree',
                                           content='\n'.join(self.filenames),
                                           maxdepth=2)))
            if self.download_source is not None:
                self.index.write("\n\n----\n%s" % self.download_source)
        else:
            # TODO: find a better way to recognize the splitting-level

            # Split on top level sections, but ignore spurious empty headings
            if heading.decoration == '=' and heading.text.strip():
                if self.download_source is not None and len(self.filenames):
                    self.output.write("\n\n----\n%s" % self.download_source)

                newfn = make_filename(heading.text)
                self.filenames.append(newfn)
                rst = self.dir.joinpath(newfn).with_suffix('.rst')
                self.output = rst.open('w', encoding=self.encoding)
                self.output.write('.. -*- coding: %s -*-\n\n' % self.encoding)


class Writer(object):
    def __init__(self, target, encoding, download_source_link=False, debug=False):
        self.target = target
        self.encoding = encoding
        self.download_source_link = download_source_link
        self.debug = debug
        self.elements = []
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

    def get_current_heading(self):
        for element in reversed(self.elements):
            if isinstance(element, Heading):
                return element

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
        self.stack.append(Span(text, font_style, text_position))

    def a_start(self, href):
        self.stack << Anchor(href)

    def a_end(self):
        ~self.stack

    def image(self, name, content, width=None, height=None):
        image = Image(self.dir, name, content, width, height)
        self.stack.append(image)
        self.get_current_heading().add_footer_item(image)

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

    def row_start(self):
        self.stack << TableRow()

    def row_end(self):
        ~self.stack

    def cell_start(self, rows_span, columns_span):
        self.stack << TableRowCell(rows_span, columns_span)

    def cell_end(self):
        ~self.stack

    def writeout(self):
        if self.target == '-':
            emitter = Emitter(self.elements)
        else:
            if not self.dir.is_dir():
                self.dir.mkdir()

            if self.monolithic_output:
                emitter = MonolithicEmitter(self.elements, self.target, self.encoding)
            else:
                emitter = SphinxEmitter(self.elements, self.dir, self.encoding,
                                        self.download_source_link)
        emitter()
