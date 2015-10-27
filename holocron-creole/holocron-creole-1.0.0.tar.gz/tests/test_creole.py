# coding: utf-8

# Copyright (C) 2015  Igor Kalnitsky
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import textwrap
import unittest

from holocron.app import Holocron
from holocron_creole.converter import Creole


class TestCreoleConverter(unittest.TestCase):
    """
    Test Creole converter.
    """

    def setUp(self):
        self.conv = Creole(Holocron(conf={
            'ext': {
                'enabled': ['creole'],
            },
        }))

    def test_simple_post(self):
        """
        Creole converter has to fucking work.
        """
        meta, html = self.conv.to_html(textwrap.dedent('''\
            = some title =

            some text with **bold**
        '''))

        self.assertEqual(meta['title'], 'some title')
        self.assertEqual(html, '<p>some text with <strong>bold</strong></p>')

    def test_post_with_sections(self):
        """
        Title must be gone, section must be converted into <h2>.
        """
        meta, html = self.conv.to_html(textwrap.dedent('''\
            = some title =

            == some section 1 ==

            xxx

            == some section 2 ==

            yyy
        '''))

        self.assertEqual(meta['title'], 'some title')
        self.assertRegexpMatches(html, (
            '^<h2>some section 1</h2>\s*'
            '<p>xxx</p>\s*'
            '<h2>some section 2</h2>\s*'
            '<p>yyy</p>$'))

    def test_two_titles(self):
        """
        Only first <h1> should be considered as title, other <h1> should
        be kept as is.
        """
        meta, html = self.conv.to_html(textwrap.dedent('''\
            = some title =

            = other title =

            xxx
        '''))

        self.assertEqual(meta['title'], 'some title')
        self.assertRegexpMatches(html, (
            '^<h1>other title</h1>\s*'
            '<p>xxx</p>$'))

    def test_no_title_in_the_middle(self):
        """
        Only <h1> on the beginning should be considered as title, <h1> in
        the middle of content should be kept as is.
        """
        meta, html = self.conv.to_html(textwrap.dedent('''\
            xxx

            = some title =

            yyy
        '''))

        self.assertNotIn('title', meta)
        self.assertRegexpMatches(html, (
            '^<p>xxx</p>\s*'
            '<h1>some title</h1>\s*'
            '<p>yyy</p>$'))

    def test_post_without_title(self):
        """
        Converter has to work even if there's no title in the document.
        """
        meta, html = self.conv.to_html(
            'some text with **bold** and //italic//\n')

        self.assertEqual(meta, {})
        self.assertEqual(html, (
            '<p>some text with <strong>bold</strong> and <i>italic</i></p>'))

    def test_code_macros_is_enabled(self):
        """
        Converter has to use Pygments to highlight code blocks.
        """
        self.conv = Creole(Holocron(conf={
            'ext': {
                'enabled': ['creole'],
                'creole': {
                    'syntax_highlight': True,
                }
            }}))

        _, html = self.conv.to_html(textwrap.dedent('''\
            <<code ext=".py">>
                lambda x: pass
            <</code>>
        '''))

        self.assertRegexpMatches(html, '.*pygments.*<pre>[\s\S]+</pre>.*')

    def test_code_macros_is_disabled(self):
        """
        Converter shouldn't support code macros if syntax highlighting is
        turned off.
        """
        self.conv = Creole(Holocron(conf={
            'ext': {
                'enabled': ['creole'],
                'creole': {
                    'syntax_highlight': False,
                }
            }}))

        _, html = self.conv.to_html(textwrap.dedent('''\
            <<code ext=".py">>
                lambda x: pass
            <</code>>
        '''))

        self.assertEqual(html, "[Error: Macro 'code' doesn't exist]")

    def test_post_with_inline_code(self):
        """
        Converter has to use <code> for inline code.
        """
        _, html = self.conv.to_html('test {{{code}}}\n')

        self.assertEqual(html, '<p>test <tt>code</tt></p>')
