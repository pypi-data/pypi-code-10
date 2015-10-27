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

import re

from creole import creole2html
from creole.shared import example_macros

from dooku.conf import Conf
from holocron.ext import abc


class Creole(abc.Converter):
    """
    A creole converter.

    This class is a converter extension that is designed to convert some
    input creole text into HTML, extracting some useful meta information.
    See the :class:`~holocron.ext.Converter` class for interface details.

    The converter supports some settings that could be turned on/off
    in the following option:

        ext:
           creole: { ... }

    The class is actually both extension and converter in terms of Holocron
    at one time. It means that this class will be discovered by Holocron as
    extension, and this class register its instance as converter in the
    application.

    :param app: an application instance for which we're creating extension
    """

    extensions = ['.creole']

    _default_conf = {
        'syntax_highlight': True,
    }

    def __init__(self, app):
        self._conf = Conf(self._default_conf, app.conf.get('ext.creole', {}))
        self._re_title = re.compile('<h1>(.*?)</h1>(.*)', re.M | re.S)

        self._macros = {}
        if self._conf['syntax_highlight']:
            self._macros['code'] = example_macros.code

        app.add_converter(self)

    def to_html(self, text):
        html = creole2html(text, macros=self._macros)
        return self._extract_meta(html)

    def _extract_meta(self, html):
        """
        Extracts some meta information from a given HTML.

        We need to cut document's title from the HTML, because we want to
        use it in different places and show it in own way. Please note that
        the method *cut* the title, and there will be no title in the HTML
        anymore.

        :param html: extracts information from the HTML
        :returns: a tuple of (meta, html)
        """
        meta = {}

        match = self._re_title.match(html)
        if match:
            meta['title'], html = match.groups()

        return meta, html.strip()
