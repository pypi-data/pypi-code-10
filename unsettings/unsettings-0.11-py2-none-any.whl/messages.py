#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Indicator-Privacy - Unity appindicator to switch privacy settings
#                     http://www.florian-diesch.de/software/indicator-privacy/
#
# Copyright (C) 2013 Florian Diesch <devel@florian-diesch.de>
#
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

from gettext import gettext as _

import settings


clear_recent_activate_msg = _("""\
Do you really want to remove <b>all items</b> from the recently used files list?\
""")

clear_recent_activate_explanation = _("""\
Some programs store information about recently used files and folders so you can access them easier next time.

If you remove this list this information will be lost.\
""")

clear_altf2_history_msg = _("""\
Do you really want to remove <b>all items</b> from the Alt+F2 history?

<i>You need to log out before using Alt+F2 again for this to work.</i>\
""")

clear_altf2_history_explanation = _("""\
The Alt+F2 command runner saves a list of previous used commands and uses them as search results in the "History" section.

If you clear the Alt+F2 history this information will be lost.

<b>Note:</b> After clearing the command history you need to log out before you use the Alt+F2 command runner again. Otherwise the history will not be cleared.\
""")

clear_zeitgeist_msg = _("""\
Do you really want to remove <b>all items</b> from the Zeitgeist log?\
""")

clear_zeitgeist_explanation = _("""\
Zeitgeist is used by some programs to store information about files and URLs you access, applications you start, or similar activities.
Other programs, like the Unity Dash, use this information to let you quickly access this files, URLs or applications.

If you clear the Zeitgeist log this information will be lost.\
""")



clear_thumbs_cache_msg = _("""\
Do you really want to remove <b>all cached thumbnails</b>?\
""")

clear_thumbs_cache_explanation = _("""\
This will remove the folder <i>%s</i>. Some programs, like Nautilus, use this folder to store thumbnails for pictures, videos and similar files.

If you clear the thumbnail cache the thumbnails need to be created again next time they are displayed.
Depending on your hardware this may take some time.\
""") % settings.THUMBS_CACHE_PATH

clear_thumbs_cache_error = _("""\
Error while removing cached thumbnails:

%s\
""")



clear_gvfs_meta_msg = _("""\
Do you really want to remove <b>all GVFS metadata</b>?\
""")

clear_gvfs_meta_explanation = _("""\
This will remove the folder <i>%s</i>. 

GVFS metadata is used by some programs to store file specific data. For example Nautilus uses this to store the positions of your desktop icons, and Evince uses this to store information about documents, like the last page your viewed.

If you remove the GVFS metadata all this information will be lost.\
""") % settings.GVFS_METADATA_PATH

clear_gvfs_meta_error = _("""\
Error while removing GVFS metadata:

%s\
""")


clear_dvdcss_keys_msg = _("""\
Do you really want to remove <b>all cached libdvdcss keys</b>?\
""")

clear_dvdcss_keys_explanation = _("""\
This will remove the folder <i>%s</i> that contains the libdvdcss key cache.

Video players like VLC use this folder to store encryption keys if you play commercial video DVDs.

If you remove the cache the keys need to be created again next time you play the DVD. Depending on your hardware this may take some time.\
""") % settings.LIBDVDCSS_KEYS_PATH

clear_dvdcss_keys_error = _("""\
Error while removing cached libdvdcss keys:

%s\
""")
