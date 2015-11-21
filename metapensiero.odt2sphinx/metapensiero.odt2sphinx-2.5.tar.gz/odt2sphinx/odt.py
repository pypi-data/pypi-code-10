# -*- coding: utf-8 -*-

from operator import itemgetter
import subprocess
import sys
import zipfile

from xml.etree import cElementTree as et


class Reader(object):
    style_map = {
        'Title': 'title',
        'Subtitle': 'subtitle',
        'Heading': 'h0',
        'Heading_20_1': 'h1',
        'Heading_20_2': 'h2',
        'Heading_20_3': 'h3',
        'Heading_20_4': 'h4',
    }
    ns = dict(
        office="urn:oasis:names:tc:opendocument:xmlns:office:1.0",
        style="urn:oasis:names:tc:opendocument:xmlns:style:1.0",
        text="urn:oasis:names:tc:opendocument:xmlns:text:1.0",
        table="urn:oasis:names:tc:opendocument:xmlns:table:1.0",
        tableooo="http://openoffice.org/2009/table",
        draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
        fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
        xlink="http://www.w3.org/1999/xlink",
        dc="http://purl.org/dc/elements/1.1/",
        meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
        number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0",
        svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
        chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0",
        dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0",
        math="http://www.w3.org/1998/Math/MathML",
        form="urn:oasis:names:tc:opendocument:xmlns:form:1.0",
        script="urn:oasis:names:tc:opendocument:xmlns:script:1.0",
        ooo="http://openoffice.org/2004/office",
        ooow="http://openoffice.org/2004/writer",
        oooc="http://openoffice.org/2004/calc",
        dom="http://www.w3.org/2001/xml-events",
        xforms="http://www.w3.org/2002/xforms",
        xsd="http://www.w3.org/2001/XMLSchema",
        xsi="http://www.w3.org/2001/XMLSchema-instance",
        rpt="http://openoffice.org/2005/report",
        of="urn:oasis:names:tc:opendocument:xmlns:of:1.2",
        rdfa="http://docs.oasis-open.org/opendocument/meta/rdfa#",
        field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0",
        formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0",
        )

    def __init__(self, filename, debug=False):
        self.debug = debug
        self.filename = filename
        self.dirname = self.filename.parent
        self.archive = zipfile.ZipFile(filename.open('rb'))
        self.xml_content = self._load_xml('content.xml')
        self.xml_styles = self._load_xml('styles.xml')
        self.meta = self._load_xml('meta.xml')
        self._load_styles()
        self._load_list_styles()
        self._styles_stack = [(None, None)]

    def _load_xml(self, fname):
        buffer = self.archive.read(fname)
        root = et.fromstring(buffer)
        if self.debug:
            subprocess.check_output(['/usr/bin/xmllint', '--format', '--output', fname, '-'],
                                    input=buffer)
        return root

    def _load_list_styles(self):
        self.list_styles = {}
        stylenodes = self.xml_styles.findall('.//{%(text)s}list-style' % self.ns)
        stylenodes.extend(
            self.xml_content.findall('.//{%(text)s}list-style' % self.ns))
        for node in stylenodes:
            name = node.get('{%(style)s}name' % self.ns)
            styles = []
            for child in node.getchildren():
                props = {'level': int(child.get('{%(text)s}level' % self.ns))}
                if child.tag == '{%(text)s}list-level-style-number' % self.ns:
                    format = child.get('{%(style)s}num-format' % self.ns)
                    suffix = child.get('{%(style)s}num-suffix' % self.ns)
                    props['kind'] = format + (suffix or '.')
                elif child.tag == '{%(text)s}list-level-style-bullet' % self.ns:
                    props['kind'] = '*'
                styles.append(props)
            # The list should be already in level order, but just in case...
            self.list_styles[name] = sorted(styles, key=itemgetter('level'))

    def _load_styles(self):
        self.styles = {None: None}
        stylenodes = self.xml_styles.findall('.//{%(style)s}style' % self.ns)
        stylenodes.extend(
            self.xml_content.findall('.//{%(style)s}style' % self.ns))

        for node in stylenodes:
            name = node.get('{%(style)s}name' % self.ns)
            style = dict(name=name)
            for aname in ('display-name', 'family', 'parent-style-name',
                          'next-style-name', 'class'):
                style[aname] = node.get('{%(style)s}' % self.ns + aname)

            for child in node.getchildren():
                if child.tag == '{%(style)s}text-properties' % self.ns:
                    font_style = child.get('{%(fo)s}font-style' % self.ns)
                    if font_style == 'italic':
                        style['font-style'] = 'italic'
                    font_weight = child.get('{%(fo)s}font-weight' % self.ns)
                    if font_weight == 'bold':
                        style['font-style'] = 'bold'
                    underline_style = child.get(
                        '{%(style)s}text-underline-style' % self.ns)
                    if underline_style == 'solid':
                        style['font-style'] = 'underline'
                    text_position = child.get('{%(style)s}text-position' % self.ns)
                    if text_position:
                        if text_position.startswith('sub '):
                            style['text-position'] = 'subscript'
                        elif text_position.startswith('super '):
                            style['text-position'] = 'superscript'

            # Special case. We know that the "Source_xx_Text" styles
            # are for source code.
            if name.startswith("Source_") and name.endswith("_Text"):
                style['font-style'] = 'fixed'

            self.styles[name] = style

        self.style_map = dict(self.style_map)
        for key, style in self.styles.items():
            if style is None:
                continue
            display_name = style['display-name'] or style['name']
            h = None
            if display_name.startswith('Heading'):
                h = 0
                if len(display_name) > 7:
                    try:
                        h = int(display_name[8:])
                    except ValueError:
                        h = None
            if display_name == 'Titre':
                h = 0
            if display_name.startswith('Titre '):
                try:
                    h = int(display_name[6:])
                except ValueError:
                    h = None
            if h is not None:
                self.style_map[key] = 'h%s' % h
            if display_name.lower() in ['note', 'information']:
                self.style_map[key] = 'note'
            if display_name.lower() in ['warning', 'avertissement']:
                self.style_map[key] = 'warning'
            if display_name.lower() in ('tip', 'trucs & astuces'):
                self.style_map[key] = 'tip'
        if self.debug:
            print(self.style_map, file=sys.stderr)

    def recurse_node(self, node, visitor):
        last_font_style, last_text_position = self._styles_stack[-1]
        style_name = node.get('{%(text)s}style-name' % self.ns)
        style = self.styles.get(style_name)
        font_style = style.get('font-style') if style else None
        text_position = style.get('text-position') if style else None

        if font_style is None:
            font_style = last_font_style
        if text_position is None:
            text_position = last_text_position

        self._styles_stack.append((font_style, text_position))

        if node.text:
            visitor('text', node.text, font_style, text_position)

        for child in node.getchildren():
            self.handle_node(child, visitor)
            if child.tail:
                visitor('text', child.tail, font_style, text_position)

        self._styles_stack.pop()

    def get_node_kind(self, node):
        if node is None:
            return
        if node.tag == '{%(text)s}list-item' % self.ns and len(node) > 0:
            node = node[0]
        style_name = node.get('{%(text)s}style-name' % self.ns)
        style = self.styles[style_name]
        if style and style_name not in self.style_map \
                and style['parent-style-name'] in self.style_map:
            style_name = style['parent-style-name']
            style = self.styles[style_name]
        if style_name in self.style_map:
            kind = self.style_map[style_name]
        else:
            kind = 'p'
        return kind

    def get_image_properties(self, node):
        href = node.get('{%(xlink)s}href' % self.ns)
        if href is None:
            return None, None
        fname = href.split('/')[-1]
        if href.startswith('./'):
            href = href[2:]
        if href.startswith('../'):
            with self.dirname.joinpath(href[3:]).open('rb') as f:
                fcontent = f.read()
        else:
            fcontent = self.archive.read(href)
        return fname, fcontent

    def handle_node(self, node, visitor):
        if node.tag in ('{%(text)s}span' % self.ns, '{%(text)s}s' % self.ns):
            self.recurse_node(node, visitor)

        elif node.tag in ('{%(text)s}p' % self.ns, '{%(text)s}h' % self.ns):
            kind = self.get_node_kind(node)
            with visitor.wrapped_visit(kind):
                self.recurse_node(node, visitor)

        elif node.tag == '{%(draw)s}frame' % self.ns:
            children = node.getchildren()
            if len(children) == 1 and children[0].tag == '{%(draw)s}image' % self.ns:
                fname, fcontent = self.get_image_properties(children[0])
                if fname is None:
                    return
                width = node.get('{%(svg)s}width' % self.ns)
                height = node.get('{%(svg)s}height' % self.ns)
                visitor('image', fname, fcontent, width=width, height=height)
            else:
                self.recurse_node(node, visitor)

        elif node.tag == '{%(draw)s}image' % self.ns:
            fname, fcontent = self.get_image_properties(node)
            if fname is None:
                return
            visitor('image', fname, fcontent)

        elif node.tag == '{%(text)s}list' % self.ns:
            headings = node.findall('.//{%(text)s}h' % self.ns)
            if len(headings):
                for h in headings:
                    self.handle_node(h, visitor)
            else:
                level = visitor.list_level
                if level == 1:
                    style_name = node.get('{%(text)s}style-name' % self.ns)
                    self.current_list_styles = self.list_styles[style_name]
                kind = self.current_list_styles[level-1]['kind']
                with visitor.wrapped_visit('list', kind):
                    self.recurse_node(node, visitor)

        elif node.tag == '{%(text)s}list-item' % self.ns:
            with visitor.wrapped_visit('list_item'):
                self.recurse_node(node, visitor)

        elif node.tag == '{%(table)s}table' % self.ns:
            with visitor.wrapped_visit('table'):
                self.recurse_node(node, visitor)

        elif node.tag == '{%(table)s}table-column' % self.ns:
            repeat = int(node.get('{%(table)s}number-columns-repeated' % self.ns, 1))
            visitor('table_column', repeat=repeat)

        elif node.tag == '{%(table)s}table-header-rows' % self.ns:
            with visitor.wrapped_visit('table_header_rows'):
                self.recurse_node(node, visitor)

        elif node.tag == '{%(table)s}table-row' % self.ns:
            with visitor.wrapped_visit('table_row'):
                self.recurse_node(node, visitor)

        elif node.tag == '{%(table)s}table-cell' % self.ns:
            cspan = int(node.get('{%(table)s}number-columns-spanned' % self.ns, 1))
            rspan = int(node.get('{%(table)s}number-rows-spanned' % self.ns, 1))
            with visitor.wrapped_visit('table_cell', rspan, cspan):
                self.recurse_node(node, visitor)

        elif node.tag == '{%(table)s}covered-table-cell' % self.ns:
            visitor('covered_table_cell')

        elif node.tag == '{%(text)s}a' % self.ns:
            href = node.get('{%(xlink)s}href' % self.ns)
            with visitor.wrapped_visit('a', href):
                self.recurse_node(node, visitor)

        elif node.tag == '{%(text)s}tab' % self.ns:
            visitor('text', ' ')

        elif node.tag == '{%(text)s}line-break' % self.ns:
            visitor('line_break')

        elif node.tag == '{%(text)s}table-of-content' % self.ns:
            title = None
            depth = None
            for child in node.getchildren():
                if child.tag == '{%(text)s}table-of-content-source' % self.ns:
                    depth = int(child.get('{%(text)s}outline-level' % self.ns))
                    for nephew in child.getchildren():
                        if nephew.tag == '{%(text)s}index-title-template' % self.ns:
                            title = nephew.text
                            break
                    break
            if title is not None or depth is not None:
                visitor('table_of_content', title, depth)

        else:
            if self.debug:
                print("Unsupported node tag: %r" % node.tag, file=sys.stderr)

    def __call__(self, visitor):
        nodes = self.xml_content.findall(
            '{%(office)s}body/{%(office)s}text/*' % self.ns)

        for el in nodes:
            self.handle_node(el, visitor)
