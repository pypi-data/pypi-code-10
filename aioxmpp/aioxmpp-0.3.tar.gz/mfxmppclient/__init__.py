import asyncio
import numbers
import sys

from datetime import timedelta

import urwid
import urwid.canvas
import urwid.raw_display
import urwid.text_layout

import asyncio_xmpp.node

palette = [
    ("status-bar", "white", "light blue", None, "#ddd", "#79A")
]

def input_filter(keys, raw):
    if len(keys) > 1:
        keys = [
            key if key != 'enter' else 'meta enter'
            for key in keys]
    # print(keys, raw, file=sys.stderr)
    # sys.stderr.flush()
    return keys

def rebase_layout(layout, base_offset):
    for row in layout:
        for i, segment in enumerate(row):
            if len(segment) == 2:
                nspc, offset = segment
                if offset is not None:
                    row[i] = nspc, offset+base_offset
            else:
                v1, offset1, offset2 = segment
                if isinstance(offset2, numbers.Number):
                    offset2 += base_offset
                offset1 += base_offset
                row[i] = v1, offset1, offset2

class ScrollableTextBox(urwid.Widget):
    _sizing = urwid.BOX
    _selectable = False

    def __init__(self):
        super().__init__()
        self._lines = ["foo", "bar", "baz"]
        self._top_offset = 0
        self._cached_layout = None
        self._cached_width = None
        self._cached_height = None
        self._cached_text = None
        self._layouter = urwid.text_layout.StandardTextLayout()

    def append_lines(self, lines, auto_scroll=True):
        self._lines.extend(lines)
        if self._cached_layout is not None:
            partial_layout = self._layouter.layout(
                "\n".join(lines),
                self._cached_width,
                'left',
                'space')
            rebase_offset = len(self._cached_text)
            if rebase_offset > 0:
                # a \n will be inserted!
                rebase_offset += 1
            rebase_layout(partial_layout, rebase_offset)
            self._cached_text = "\n".join([self._cached_text] + lines)
            self._cached_layout.extend(partial_layout)
        self._invalidate()

        if auto_scroll:
            self._top_offset = None

    def _relayout(self, maxrow, maxcol):
        self._cached_width = maxcol
        self._cached_height = maxrow
        self._cached_text = "\n".join(self._lines)
        self._cached_layout = self._layouter.layout(
            self._cached_text,
            maxcol,
            'left',
            'space')

    def _get_first_layout_line(self, maxrow):
        target_row = None

        if self._top_offset is not None:
            for i, row in enumerate(self._cached_layout):
                for segment in row:
                    try:
                        _, offset, end_offset = segment
                    except ValueError:
                        continue
                    if isinstance(end_offset, str):
                        continue
                    if offset <= self._top_offset <= end_offset:
                        target_row = i
                        break
                else:
                    continue
                break

        if target_row is None:
            target_row = len(self._cached_layout) - 1

        return max(0,
                   min(target_row,
                       len(self._cached_layout) - maxrow))

    def invalidate_layout(self):
        self._cached_layout = None
        self._cached_text = None
        self._invalidate()

    def scroll(self, offset):
        if self._top_offset is None:
            self._top_offset = self._get_first_layout_line(self._cached_height)
        self._top_offset += offset
        self._invalidate()

    def render(self, size, focus=False):
        maxcol, maxrow = size

        if self._cached_layout is not None:
            if self._cached_width != maxcol:
                self._relayout(maxrow, maxcol)
        else:
            self._relayout(maxrow, maxcol)

        first_row_index = self._get_first_layout_line(maxrow)

        rows = self._cached_layout[first_row_index:first_row_index+maxrow]
        if len(rows) < maxrow:
            rows.extend([[(0, None)]]*(maxrow-len(rows)))

        text_canvas = urwid.canvas.apply_text_layout(
            self._cached_text,
            [],
            rows,
            maxcol)
        # composite = urwid.canvas.CompositeCanvas(
        #     urwid.canvas.BlankCanvas())
        # composite.overlay(text_canvas, 0, 0)
        return text_canvas

class StatusBar(urwid.AttrMap):
    def __init__(self):
        super().__init__(urwid.Text("bar"), "status-bar")

class TitleBar(urwid.AttrMap):
    def __init__(self):
        super().__init__(urwid.Text("bar"), "status-bar")

class Window(urwid.Frame):
    _selectable = False

    def __init__(self):
        super().__init__(
            ScrollableTextBox(),
            TitleBar(),
            StatusBar())

class MetaEnterEdit(urwid.Edit):
    def keypress(self, size, key):
        # print(size, key, file=sys.stderr)
        if key == 'enter':
            return key
        elif key == 'meta enter':
            key = 'enter'
        return super().keypress(size, key)

class Client:
    def __init__(self, *, loop=None):
        self._loop = loop or asyncio.get_event_loop()

        self._edit = MetaEnterEdit(
            "[(status)] ",
            multiline=True
        )
        self._window = Window()

        self._urwid_root = urwid.Pile([
                ('weight', 1, self._window),
                ('pack', self._edit)
            ])
        self._urwid_root.focus_position = 1
        self._urwid_screen = urwid.raw_display.Screen()
        self._urwid_screen.register_palette(palette)
        self._urwid_screen.set_terminal_properties(colors=256)
        self._urwid_loop = urwid.MainLoop(
            self._urwid_root,
            screen=self._urwid_screen,
            event_loop=urwid.AsyncioEventLoop(loop=self._loop),
            input_filter=input_filter,
            handle_mouse=False,
            unhandled_input=self._unhandled_input)

        self._unhandled_queue = asyncio.Queue(loop=self._loop)

    def _unhandled_input(self, key):
        self._unhandled_queue.put_nowait(key)

    @asyncio.coroutine
    def _main(self):
        self._window.body.append_lines(
            ["foo bar baz {}".format(i)
             for i in range(20000)]
        )
        while True:
            ev = yield from self._unhandled_queue.get()
            if ev == 'enter':
                text = self._edit.get_edit_text().strip()
                if text:
                    self._window.body.append_lines(text.split("\n"))
                self._edit.set_edit_text("")
            elif ev == "page up":
                self._window.body.scroll(-20)
            elif ev == "page down":
                self._window.body.scroll(20)
            self._urwid_loop.draw_screen()

    def run(self):
        with self._urwid_loop.start():
            self._loop.run_until_complete(self._main())
