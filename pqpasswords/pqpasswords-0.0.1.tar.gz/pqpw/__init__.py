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


COLUMNS = ({
    'label': 'Title',
    'field': 'title',
}, {
    'label': 'Username',
    'field': 'user',
}, {
    'label': 'Group',
    'field': 'group',
}, {
    'label': 'Password',
    'field': 'passwd',
}, {
    'label': 'URL',
    'field': 'url',
}, {
    'label': 'Notes',
    'field': 'notes',
# }, {
#     'label': 'Last modified',
#     'field': 'last_mod',
# }, {
#     'label': 'UUID',
#     'field': 'uuid',
})

COLUMNS_BY_FIELD = dict(map(
    lambda i: (i[1]['field'], i[0]), enumerate(COLUMNS)))

VAULT_EXT = {
    'Password Safe v3 (*.psafe3)': '.psafe3',
}
ALL_EXT = {
    'All files (*.*)': '.*',
}
