"""
This plugin show the list of open documents.
"""
import os
from hackedit import api

from PyQt5 import QtCore, QtWidgets


class OpenDocuments(api.plugins.WorkspacePlugin):
    """ This plugin show the list of open documents. """
    def activate(self):
        self.list = QtWidgets.QListWidget()
        api.window.add_dock_widget(
            self.list, 'Documents',
            icon=api.widgets.FileIconProvider.mimetype_icon('file.txt'),
            area=QtCore.Qt.LeftDockWidgetArea)
        api.signals.connect_slot(
            api.signals.CURRENT_EDITOR_CHANGED, self._update)
        self.list.itemActivated.connect(self._on_item_activated)
        self.list.itemClicked.connect(self._on_item_activated)
        self.icon_provider = api.widgets.FileIconProvider()

    def _update(self, *_):
        self.list.clear()
        names = []
        paths = []
        for path in api.editor.get_all_paths():
            paths.append(path)
            finfo = QtCore.QFileInfo(path)
            name = finfo.fileName()
            names.append(name)
        current_index = 0
        for n, p in zip(names, paths):
            if names.count(n) > 1:
                n = os.path.join(
                    QtCore.QFileInfo(os.path.dirname(p)).baseName(), n)
            itm = QtWidgets.QListWidgetItem(
                self.icon_provider.icon(QtCore.QFileInfo(n)), n)
            itm.setToolTip(p)
            if p == api.editor.get_current_path():
                current_index = self.list.count()
            self.list.addItem(itm)
        self.list.setCurrentRow(current_index)

    def _on_item_activated(self, item):
        path = item.toolTip()
        api.editor.open_file(path)
