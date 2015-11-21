# -*- coding: utf-8 -*-
# :Project:   metapensiero.odt2sphinx
# :Created:   gio 19 nov 2015 08:19:22 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   Python Software Foundation License
# :Copyright: Copyright (C) 2015 Lele Gaifax
#

import itertools
import re
import sys


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


class NewlineFilter(object):
    "Output stream wrapper that strips excessive newlines."

    def __init__(self, output):
        self.output = output
        self.newlines = 0
        self.bofs = True

    def close(self):
        self.output.write('\n')
        if self.output is not sys.stdout:
            self.output.close()

    def write(self, chunk):
        newlines = self.newlines
        if chunk.startswith('\n'):
            for c in chunk:
                if c != '\n':
                    break
                newlines += 1
            chunk = chunk.lstrip('\n')

        if chunk:
            if newlines and not self.bofs:
                self.output.write('\n' * min(newlines, 2))
                newlines = 0

            if chunk.endswith('\n'):
                while chunk[-newlines - 1] == '\n':
                    newlines += 1
                chunk = chunk.rstrip('\n')
            self.output.write(chunk)
            self.bofs = False

        self.newlines = newlines


class Emitter(object):
    def __init__(self, elements, output=None):
        self.elements = elements
        self.output = NewlineFilter(output or sys.stdout)
        self.current_heading = None

    def change_heading(self, heading):
        item = None
        if self.current_heading is None:
            # Emit initial elements footer content
            footer_items = self.elements.footer_items
        else:
            # Emit previous section elements footer content
            footer_items = self.current_heading.footer_items

        for item in footer_items:
            # Ignore aggregated items
            if item.has_footer_content:
                item.footer_emit(self.output)

        if item is not None:
            self.output.write('\n')

        self.current_heading = heading

    def __call__(self):
        from .rst import Heading, aggregate

        for element in aggregate(self.elements):
            if isinstance(element, Heading):
                self.change_heading(element)
            element.emit(self.output)
        self.change_heading(None)
        self.output.close()


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
        from .rst import Directive

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
        from .rst import Directive

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
