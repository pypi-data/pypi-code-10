# -*- coding: utf-8 -*-

from contextlib import contextmanager


class Visitor(object):
    def __init__(self, writer, debug=False):
        self.writer = writer
        self.debug = debug
        self.list_level = 1

    def on_p_start(self):
        self.writer.p_start()

    def on_p_end(self):
        self.writer.p_end()

    def on_a_start(self, href):
        self.writer.a_start(href)

    def on_a_end(self):
        self.writer.a_end()

    def on_note_start(self):
        self.writer.hightlight_start('note')

    def on_note_end(self):
        self.writer.highlight_end()

    def on_warning_start(self):
        self.writer.highlight_start('warning')

    def on_warning_end(self):
        self.writer.highlight_end()

    def on_tip_start(self):
        self.writer.highlight_start('tip')

    def on_tip_end(self):
        self.writer.highlight_end()

    def on_title_start(self):
        self.writer.title_start()

    def on_title_end(self):
        self.writer.title_end()

    def on_subtitle_start(self):
        self.writer.subtitle_start()

    def on_subtitle_end(self):
        self.writer.subtitle_end()

    def on_h0_start(self):
        self.writer.h0_start()

    def on_h0_end(self):
        self.writer.h0_end()

    def on_h1_start(self):
        self.writer.h1_start()

    def on_h1_end(self):
        self.writer.h1_end()

    def on_h2_start(self):
        self.writer.h2_start()

    def on_h2_end(self):
        self.writer.h2_end()

    def on_h3_start(self):
        self.writer.h3_start()

    def on_h3_end(self):
        self.writer.h3_end()

    def on_h4_start(self):
        self.writer.h4_start()

    def on_h4_end(self):
        self.writer.h4_end()

    def on_h5_start(self):
        self.writer.h5_start()

    def on_h5_end(self):
        self.writer.h5_end()

    def on_h6_start(self):
        self.writer.h6_start()

    def on_h6_end(self):
        self.writer.h6_end()

    def on_list_start(self, kind):
        self.list_level += 1
        self.writer.list_start(kind)

    def on_list_end(self):
        self.writer.list_end()
        self.list_level -= 1

    def on_list_item_start(self):
        self.writer.list_item_start()

    def on_list_item_end(self):
        self.writer.list_item_end()

    def on_text(self, text, font_style=None, text_position=None):
        # Ignore spurious "\n   " chunks emitted by the ODT reader
        if not text.startswith('\n') or text.strip():
            self.writer.text(text, font_style, text_position)

    def on_line_break(self):
        from .rst import line_break
        self.writer.text(line_break)

    def on_image(self, fname, fcontent, width=None, height=None):
        if fname.find('.') == -1:
            fname += '.png'
        fname = fname.replace(' ', '_')
        self.writer.image(fname, fcontent, width=width, height=height)

    def on_table_start(self):
        self.writer.table_start()

    def on_table_end(self):
        self.writer.table_end()

    def on_table_column(self, repeat, width):
        self.writer.table_column(repeat, width)

    def on_table_header_rows_start(self):
        self.writer.table_header_start()

    def on_table_header_rows_end(self):
        self.writer.table_header_end()

    def on_table_row_start(self):
        self.writer.row_start()

    def on_table_row_end(self):
        self.writer.row_end()

    def on_table_cell_start(self, rows_span, columns_span):
        self.writer.cell_start(rows_span, columns_span)

    def on_table_cell_end(self):
        self.writer.cell_end()

    def on_covered_table_cell(self):
        pass

    def on_table_of_content(self, title, depth):
        self.writer.table_of_content(title, depth)

    def __call__(self, element, *args, **kw):
        handler = getattr(self, 'on_' + element, None)
        if handler is not None:
            handler(*args, **kw)

    @contextmanager
    def wrapped_visit(self, element, *args, **kwargs):
        self(element + '_start', *args, **kwargs)
        yield
        self(element + '_end')
