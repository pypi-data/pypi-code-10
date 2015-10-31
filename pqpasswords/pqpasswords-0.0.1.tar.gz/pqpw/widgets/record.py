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
from hashlib import md5

from PyQt4 import QtCore
from PyQt4 import QtGui

from .. import COLUMNS, COLUMNS_BY_FIELD
from ..config import config
from ..utils import icon_from_resources


class VTWidgetRecordItem(QtGui.QTreeWidgetItem):
    ''' QTreeWidgetItem that contains the contents of a Record. '''

    _record = None

    def __init__(self, parent, record):
        super().__init__(parent, type=QtGui.QTreeWidgetItem.Type)
        for i, column in enumerate(map(lambda c: getattr(record, c['field']), COLUMNS)):
            self.setData(i, QtCore.Qt.EditRole, column)
        self._record = record

        # set default icon
        self.setIcon(0, self.icon or icon_from_resources('text-x-generic'))

        # retrieve icon if not exists
        if not self.icon and self.url:
            tree = self.treeWidget()
            tree.emit(tree.urlUpdated, self)

    record = property(lambda self: self._record)

    def _set_title(self, value):
        self._record.title = value
        self.setData(COLUMNS_BY_FIELD['title'], QtCore.Qt.EditRole, value)

    def _set_user(self, value):
        self._record.user = value
        self.setData(COLUMNS_BY_FIELD['user'], QtCore.Qt.EditRole, value)

    def _set_passwd(self, value):
        self._record.passwd = value
        self.setData(COLUMNS_BY_FIELD['passwd'], QtCore.Qt.EditRole, value)

    def _set_notes(self, value):
        self._record.notes = value
        self.setData(COLUMNS_BY_FIELD['notes'], QtCore.Qt.EditRole, value)

    def _set_url(self, value):
        old_url = self._record.url
        self._record.url = value
        self.setData(COLUMNS_BY_FIELD['url'], QtCore.Qt.EditRole, value)
        if value and value != old_url:
            tree = self.treeWidget()
            tree.emit(tree.urlUpdated, self)

    def _set_group(self, value):
        self._record.group = value
        self.setData(COLUMNS_BY_FIELD['group'], QtCore.Qt.EditRole, value)

    title = property(lambda self: self._record.title, _set_title)
    user = property(lambda self: self._record.user, _set_user)
    passwd = property(lambda self: self._record.passwd, _set_passwd)
    notes = property(lambda self: self._record.notes, _set_notes)
    url = property(lambda self: self._record.url, _set_url)
    group = property(lambda self: self._record.group, _set_group)

    # def setData(self, column, role, value):
    #     ''' Overrides the base classes method. '''
    #     super().setData(column, role, value)
    #     if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
    #         if self._record:
    #             field = COLUMNS[column]['field']
    #             old_value = getattr(self._record, field)
    #             # value = value.toString()
    #             setattr(self._record, field, value)
    #             if old_value != value and field == 'url':
    #                 tree = self.treeWidget()
    #                 tree.emit(tree.urlUpdated, self)

    @property
    def icon_path(self):
        ''' returns unique path to icon '''
        return os.path.join(
            config.get_cache_dir(),
            md5(self.url.encode('utf8')).hexdigest())

    @property
    def icon(self):
        ''' returns icon or None '''
        try:
            size = os.path.getsize(self.icon_path)
            if size <= 1:
                # return fallback icon if empty
                return icon_from_resources('text-x-generic')

            f = open(self.icon_path, 'rb')
            data = f.read()
            f.close()
            image = QtGui.QImage()
            image.loadFromData(data)
            icon = QtGui.QIcon(QtGui.QPixmap(image))
            if not icon.isNull():
                return icon
        except:
            pass
