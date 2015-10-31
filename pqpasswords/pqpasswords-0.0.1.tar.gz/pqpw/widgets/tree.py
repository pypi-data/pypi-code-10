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
from .group import VTWidgetGroupItem

from .. import COLUMNS
from ..utils import icon_from_resources


class VaultTreeWidget(QtGui.QTreeWidget):
    '''
    QTreeWidget that contains the contents of a Vault.
    '''
    vault = None

    def __init__(self, *args, **kwargs):
        self.urlUpdated = QtCore.SIGNAL('urlUpdated')

        super().__init__(*args, **kwargs)
        self.setHeaderLabels(tuple(map(lambda x: x['label'], COLUMNS[:2])))
        self.setColumnWidth(0, 250)
        self.setSortingEnabled(True)
        self.sortItems(0, QtCore.Qt.AscendingOrder)

    def on_favicon_ready(self, item):
        if item.icon:
            item.setIcon(0, item.icon)

    def update_fields(self):
        self.clear()
        groups = {}
        for record in self.vault.records:
            if record.group and not record.group in groups:
                groups[record.group] = VTWidgetGroupItem(self, record.group)
            if record.group:
                parent = groups[record.group]
            else:
                parent = self
            item = VTWidgetRecordItem(parent, record)

    def set_vault(self, vault):
        '''
        Set the Vault this control should display.
        '''
        self.vault = vault
        self.update_fields()
        self.select_first()

    def deselect_all(self):
        '''
        De-selects all items
        '''
        for item in self.selectedItems():
            self.setItemSelected(item, False)

    def select_first(self):
        '''
        Selects and focuses the first item (if there is one)
        '''
        self.deselect_all()
        if self.topLevelItemCount() > 0:
            self.setItemSelected(self.topLevelItem(0), True)

    def groups(self):
        return map(lambda x: x.text(0),
            filter(lambda x: isinstance(x, VTWidgetGroupItem),
            map(self.topLevelItem, range(self.topLevelItemCount()))))

    def move_to_group(self, item):
        old_group = item.parent().text(0) if item.parent() else ''
        if item.group == old_group:
            return
        self.take_child_from_parent(item)
        if item.group:
            if item.group in self.groups():
                for i in map(self.topLevelItem, range(self.topLevelItemCount())):
                    if isinstance(i, VTWidgetGroupItem) and i.text(0) == item.group:
                        group = i
                        break
            else:
                group = VTWidgetGroupItem(self, item.group)
            group.addChild(item)
        else:
            self.addTopLevelItem(item)

    def take_child_from_parent(self, child):
        parent = child.parent()
        if parent:  # take from parent
            parent.takeChild(parent.indexOfChild(child))
        else:  # take from root
            self.takeTopLevelItem(self.indexOfTopLevelItem(child))
