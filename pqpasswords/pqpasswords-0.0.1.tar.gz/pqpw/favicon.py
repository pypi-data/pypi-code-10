# Copyright (C) 2015 Okami <okami@fuzetsu.info>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import os
import re
import time

from urllib.error import HTTPError
from urllib.request import Request, urlopen

from queue import Queue, Empty
from hashlib import md5

from html.parser import HTMLParser

from PyQt4 import QtGui
from PyQt4 import QtCore

from .config import config


class FaviconFinder(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.favicon_url = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'link' and 'href' in attributes and 'icon' in attributes.get('rel'):
            if not self.favicon_url:
                self.favicon_url = attributes['href']


class FaviconUpdater(QtCore.QThread):
    def __init__(self):
        super(FaviconUpdater, self).__init__()
        self.cache = config.get_cache_dir()
        self.queue = Queue()
        self.running = True
        self.faviconReady = QtCore.SIGNAL('faviconReady')

    def __del__(self):
        self.wait()

    def stop_me(self):
        self.running = False

    def _get(self, url):
        print(url)
        request = Request(url.toString(), headers={
            'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)',
        })
        return urlopen(request).read()

    def _parse_favicon(self, page):
        favicon_url = None
        #### HTMLParser method
        # finder = FaviconFinder()
        # finder.feed(page)
        # favicon_url = finder.favicon_url
        #### BeautifulSoup method
        # from BeautifulSoup import BeautifulSoup
        # soup = BeautifulSoup(page)
        # link = soup.html.head.find(
        #     lambda x: x.name == 'link' and 'icon' in x['rel'])
        # if link:
        #     favicon_url = link['href']
        #### RegExp method
        if not favicon_url:
            link = r'(?P<link><link[^>]+rel=[\'\"][\w ]*icon[\'\"][^>]*/?>)'
            href = r'href=[\'\"](?P<href>[^\'\"]+)[\'\"]'
            s = re.search(link, page)
            if s and s.group('link'):
                s = re.search(href, s.group('link'))
                if s and s.group('href'):
                    favicon_url = s.group('href')
        return favicon_url

    def _get_favicon(self, item):
        if item.icon:
            # got from cache
            self.emit(self.faviconReady, item)
        else:
            f = open(item.icon_path, 'wb+')
            try:
                page = self._get(QtCore.QUrl(item.url))
                favicon_url = self._parse_favicon(page.decode('utf8')) or '/favicon.ico'
                favicon = self._get(
                    QtCore.QUrl(item.url).resolved(QtCore.QUrl(favicon_url)))
                f.write(favicon)
            except HTTPError:
                f.write(b'0')
            finally:
                f.close()
                self.emit(self.faviconReady, item)

    def run(self):
        while self.running:
            try:
                item = self.queue.get_nowait()
                try:
                    self._get_favicon(item)
                except Exception as e:
                    print(e)
                self.queue.task_done()
            except Empty as e:
                time.sleep(0.05)

    def on_url_updated(self, item):
        self.queue.put_nowait(item)
