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

import json
import os
import platform


class Config(object):
    '''
    Manages the configuration file
    '''
    def __init__(self):
        '''
        DEFAULT VALUES
        '''
        self._basescript = None
        self.recentvaults = []
        self.pwlength = 10
        self.reduction = False
        self.search_notes = False
        self.search_passwd = False
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_'
        self.favicon = False
        self.window_width = 800
        self.window_height = 480

        self._fname, self._cache = self.get_config_files()
        self._json = {}

        if os.path.exists(self._fname):
            f = open(self._fname, 'r')
            self._json = json.load(f)
            f.close()

        if 'recentvaults' in self._json:
            self.recentvaults = self._json['recentvaults']
        if 'alphabet' in self._json:
            self.alphabet = self._json['alphabet']
        if 'pwlength' in self._json:
            self.pwlength = int(self._json['pwlength'])
        if 'alphabetreduction' in self._json:
            self.reduction = self._json['alphabetreduction'] == True
        if 'search_notes' in self._json:
            self.search_notes = self._json['search_notes'] == True
        if 'search_passwd' in self._json:
            self.search_passwd = self._json['search_passwd'] == True
        if 'favicon' in self._json:
            self.favicon = self._json['favicon'] == True
        if 'window_width' in self._json:
            self.window_width = int(self._json['window_width'])
        if 'window_height' in self._json:
            self.window_height = int(self._json['window_height'])

        if not os.path.exists(self._fname):
            self.save()

    def set_basescript(self, basescript):
        self._basescript = basescript

    def get_basescript(self):
        return self._basescript

    def save(self):
        if not os.path.exists(os.path.dirname(self._fname)):
            os.mkdir(os.path.dirname(self._fname))

        self._json = {}

        # remove duplicates and trim to 10 items
        _saved_recentvaults = []
        for item in self.recentvaults:
            if not item in _saved_recentvaults:
                _saved_recentvaults.append(item)

        self._json['recentvaults'] = _saved_recentvaults
        self._json['pwlength'] = self.pwlength
        self._json['alphabetreduction'] = self.reduction
        self._json['search_notes'] = self.search_notes
        self._json['search_passwd'] = self.search_passwd
        self._json['favicon'] = self.favicon
        self._json['window_width'] = self.window_width
        self._json['window_height'] = self.window_height

        f = open(self._fname, 'w+')
        json.dump(self._json, f)
        f.close()

    def get_cache_dir(self):
        if not os.path.exists(self._cache):
            os.mkdir(self._cache)
        return self._cache

    @staticmethod
    def get_config_files():
        '''
        Returns the full filename of the config file
        and fill path to cache directory
        '''
        base_fname = 'pqpasswords'
        base_cache = 'cache'

        # Default configuration path is ~/.config/foo/
        base_path = os.path.join(os.path.expanduser('~'), '.config')
        if os.path.isdir(base_path):
            fname = os.path.join(base_path, base_fname, base_fname + '.json')
        else:
            # ~/.foo/
            fname = os.path.join(os.path.expanduser('~'), '.' + base_fname + '.json')

        # ~/.cache/foo/
        base_path = os.path.join(os.path.expanduser('~'), '.cache')
        if os.path.isdir(base_path):
            cache = os.path.join(base_path, base_fname)
        else:
            # ~/.foo/cache/
            cache = os.path.join(os.path.expanduser('~'), '.' + base_fname, base_cache)

        # On Mac OS X, config files go to ~/Library/Application Support/foo/
        if platform.system() == 'Darwin':
            base_path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support')
            if os.path.isdir(base_path):
                fname = os.path.join(base_path, base_fname, base_fname + '.json')
                cache = os.path.join(base_path, base_fname, base_cache)

        # On Microsoft Windows, config files go to $APPDATA/foo/
        if platform.system() in ('Windows', 'Microsoft'):
            if ('APPDATA' in os.environ):
                base_path = os.environ['APPDATA']
                if os.path.isdir(base_path):
                    fname = os.path.join(base_path, base_fname, base_fname + '.json')
                    cache = os.path.join(base_path, base_fname, base_cache)

        # Allow config directory override as per freedesktop.org XDG Base Directory Specification
        if ('XDG_CONFIG_HOME' in os.environ):
            base_path = os.environ['XDG_CONFIG_HOME']
            if os.path.isdir(base_path):
                fname = os.path.join(base_path, base_fname, base_fname + '.json')
                cache = os.path.join(base_path, base_fname, base_cache)

        return fname, cache

config = Config()
