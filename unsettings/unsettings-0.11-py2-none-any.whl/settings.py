#!/usr/bin/env python
#
#-*- coding: utf-8-*-
#
# Unsettings - a configuration frontend for the Unity desktop environment
#
# Copyright (C) 2012 Florian Diesch <devel@florian-diesch.de>
#
# Homepage: http://www.florian-diesch.de/software/unsettings/
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
#

import os, os.path, subprocess, sys
import xdg, xdg.BaseDirectory
from gettext import gettext as _

import _meta, dialogs

APP_NAME = _meta.TITLE
APP_VERSION = _meta.VERSION
APP_DESC = _meta.DESC
APP_AUTHOR = _meta.AUTHOR_NAME
APP_AUTHOR_EMAIL = _meta.AUTHOR_EMAIL
APP_TIMESTAMP = _meta.TIMESTAMP
APP_YEAR = 2013


__version__ = APP_VERSION
app_name = APP_NAME.lower()
GETTEXT_DOMAIN=app_name 



def get_unity_version():
    cmd = ['unity', '--version']
    try:
        versionstr = subprocess.check_output(cmd)
    except OSError as e:
        dialogs.error(_('Error running %s:\n%s') % (' '.join(cmd), 
                                                    str(e)))
        sys.exit(1)
    version = versionstr.split()[1]
    major = int(version.split('.')[0])
    try:
        minor = int(version.split('.')[1])
    except IndexError:
        minor = 0
    try:
        revision = int(version.split('.')[2])
    except IndexError:
        revision = 0
    return major, minor, revision, version


FLAG_NEEDS_LOGIN=1

global_flags = {}



DUMPFILE_EXT = '.unsettings'
DUMPFILE_FORMAT = 2

SLEEP_TIME = 1



USER_CONFIG_DIR = os.path.join(os.path.expanduser('~/.config'), 'unsettings')
try:
    os.makedirs(USER_CONFIG_DIR)
except OSError:
    pass

X_ENV_FILE = os.path.join(USER_CONFIG_DIR, 'xenv')

XDG_DATA_HOME = xdg.BaseDirectory.xdg_data_home
THUMBS_CACHE_PATH = os.path.expanduser(os.path.join('~/.cache', 'thumbnails'))
GVFS_METADATA_PATH = os.path.join(XDG_DATA_HOME, 'gvfs-metadata')
LIBDVDCSS_KEYS_PATH = os.path.expanduser(os.path.join('~', '.dvdcss'))


DATA_DIR = '/usr/share/unsettings'
UI_DIR = os.path.join(DATA_DIR, 'ui')
ICON_DIR = os.path.join(DATA_DIR, 'icons')


LOCALE_DIR='/usr/share/locale'

(UNITY_MAJOR_VERSION, UNITY_MINOR_VERSION, UNITY_REVISION_NUMBER,
 UNITY_VERSION) = get_unity_version()


WEB_URL = 'http://www.florian-diesch.de/software/%s/' % app_name
LOCAL_DOCS_URL = 'man:unsettings'
PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DJCGEPS4746PU'
FLATTR_URL = 'http://flattr.com/thing/634745/Unsettings'

TRANSLATIONS_URL = 'https://translations.launchpad.net/%s' % app_name

BUGREPORT_URL = 'https://bugs.launchpad.net/%s/+filebug' % app_name

