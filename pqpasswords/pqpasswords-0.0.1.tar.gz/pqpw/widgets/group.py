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

from PyQt4 import QtCore
from PyQt4 import QtGui

from .record import VTWidgetRecordItem
from ..utils import icon_from_resources


class VTWidgetGroupItem(QtGui.QTreeWidgetItem):
    '''
    QTreeWidgetItem that contains the contents of a Group.
    '''
    def __init__(self, parent, group):
        super().__init__(parent, [group])
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        self.setIcon(0, icon_from_resources('folder'))

    def setData(self, column, role, value):
        '''
        Overrides the base classes method.
        '''
        if column == 0 and role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            value = value or '<Group>'
            if self.data(column, role) != value:  # update childs
                for child in map(self.child, range(self.childCount())):
                    if isinstance(child, VTWidgetRecordItem):
                        child.group = value
        return super().setData(column, role, value)
