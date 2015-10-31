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

import re
import os

from PyQt4 import QtCore
from PyQt4 import QtGui

from . import COLUMNS_BY_FIELD, VAULT_EXT, ALL_EXT
from .config import config
from .favicon import FaviconUpdater
from .loadframe import LoadFrame
from .recordframe import RecordFrame
from .settings import Settings
from .utils import icon_from_resources
from .vault import Vault
from .widgets.group import VTWidgetGroupItem
from .widgets.record import VTWidgetRecordItem
from .widgets.tree import VaultTreeWidget


class VaultFrame(QtGui.QMainWindow):
    '''
    Displays (and lets the user edit) the Vault.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resize(config.window_width, config.window_height)
        self.list_ = VaultTreeWidget()
        self.list_.itemDoubleClicked.connect(self._on_list_item_activated)

        self.updater = None
        if config.favicon:
            self.updater = FaviconUpdater()
            # signal: Updater(Thread) -> Widget(GUI)
            QtCore.QObject.connect(self.updater, self.updater.faviconReady,
                self.list_.on_favicon_ready)
            QtCore.QObject.connect(self.updater, self.updater.faviconReady,
                self.on_favicon_ready)
            # signal: Widget(GUI) -> Updater(Thread)
            QtCore.QObject.connect(self.list_, self.list_.urlUpdated,
                self.updater.on_url_updated)
            self.updater.start()

        self.statusBar()

        # Set up menus
        new = QtGui.QAction(icon_from_resources('document-new'),
            '&New', self)
        new.setShortcut('Ctrl+N')
        new.triggered.connect(self._on_new)

        open_ = QtGui.QAction(icon_from_resources('document-open'),
            '&Open', self)
        open_.setShortcut('Ctrl+O')
        open_.triggered.connect(self._on_open)

        self.save = QtGui.QAction(icon_from_resources('document-save'),
            '&Save', self)
        self.save.setEnabled(False)
        self.save.setShortcut('Ctrl+S')
        self.save.triggered.connect(self._on_save)

        self.save_as = QtGui.QAction(icon_from_resources('document-save-as'),
            'Save as' + '...', self)
        self.save_as.setEnabled(False)
        self.save_as.setShortcut('Ctrl+Shift+S')
        self.save_as.triggered.connect(self._on_save_as)

        self.change_password = QtGui.QAction(
            'Change &Password' + '...', self)
        self.change_password.setEnabled(False)
        self.change_password.triggered.connect(self._on_change_password)

        open_settings = QtGui.QAction('&Settings', self)
        open_settings.setShortcut('Ctrl+Shift+P')
        open_settings.triggered.connect(self._on_settings)

        # exit_ = QtGui.QAction(icon_from_resources('exit'),
        exit_ = QtGui.QAction(
            'E&xit', self)
        exit_.setShortcut('Ctrl+Q')
        exit_.triggered.connect(self.close)

        self.add_group = QtGui.QAction(icon_from_resources('folder-new'),
            'Add &group', self)
        self.add_group.setEnabled(False)
        self.add_group.setShortcut('Ctrl+G')
        self.add_group.triggered.connect(self._on_group_add)

        self.add_record = QtGui.QAction(icon_from_resources('contact-new'),
            '&Add record', self)
        self.add_record.setEnabled(False)
        self.add_record.setShortcut('Ctrl+A')
        self.add_record.triggered.connect(self._on_add)

        self.edit_record = QtGui.QAction(icon_from_resources('document-properties'),
            '&Edit', self)
        self.edit_record.setEnabled(False)
        self.edit_record.setShortcut('Ctrl+E')
        self.edit_record.triggered.connect(self._on_edit)

        self.remove_record = QtGui.QAction(icon_from_resources('edit-delete'),
            '&Delete', self)
        self.remove_record.setEnabled(False)
        self.remove_record.setShortcut('Ctrl+Backspace')
        self.remove_record.triggered.connect(self._on_delete)

        self.copy_username = QtGui.QAction(icon_from_resources('edit-copy'),
            'Copy &Username', self)
        self.copy_username.setEnabled(False)
        self.copy_username.setShortcut('Ctrl+U')
        self.copy_username.triggered.connect(self._on_copy_username)

        self.copy_password = QtGui.QAction(icon_from_resources('edit-copy'),
            'Copy &Password', self)
        self.copy_password.setEnabled(False)
        self.copy_password.setShortcut('Ctrl+P')
        self.copy_password.triggered.connect(self._on_copy_password)

        self.open_url = QtGui.QAction(icon_from_resources('internet-web-browser'),
            'Open UR&L', self)
        self.open_url.setEnabled(False)
        self.open_url.setShortcut('Ctrl+L')
        self.open_url.triggered.connect(self._on_open_url)

        menubar = self.menuBar()

        file_ = menubar.addMenu('&File')
        file_.addAction(new)
        file_.addAction(open_)
        file_.addAction(self.save)
        file_.addAction(self.save_as)
        file_.addSeparator()
        file_.addAction(self.change_password)
        file_.addSeparator()
        file_.addAction(open_settings)
        file_.addSeparator()
        file_.addAction(exit_)

        edit = menubar.addMenu('&Edit')
        edit.addAction(self.add_group)
        edit.addAction(self.add_record)
        edit.addAction(self.remove_record)
        edit.addSeparator()
        edit.addAction(self.edit_record)
        edit.addSeparator()
        edit.addAction(self.copy_username)
        edit.addAction(self.copy_password)
        edit.addAction(self.open_url)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(new)
        toolbar.addAction(open_)
        toolbar.addAction(self.save)
        toolbar.addSeparator()
        toolbar.addAction(self.add_group)
        toolbar.addAction(self.add_record)
        toolbar.addAction(self.remove_record)
        toolbar.addAction(self.edit_record)
        toolbar.addSeparator()
        # toolbar.addAction(copy_username)
        toolbar.addAction(self.copy_password)
        toolbar.addAction(self.open_url)

        self.setWindowTitle('PQPasswords')

        self.setCentralWidget(self.list_)

        self.vault_file_name = None
        self.vault_password = None
        self.vault = None
        self.mark_modified(is_modified=False)

    def mark_modified(self, item=None, i=0, is_modified=True):
        self._is_modified = is_modified
        self.save.setEnabled(is_modified)

    def preload(self, filename):
        loadframe = LoadFrame(self, is_new=False)
        loadframe.add_vault(filename)
        loadframe.exec_()
        self._modal_size = loadframe.size()

    def open_vault(self, filename=None, password=''):
        '''
        Set the Vault that this frame should display.
        '''
        self.vault_file_name = None
        self.vault_password = None
        self.vault = Vault(password, filename=filename)
        self.list_.set_vault(self.vault)
        self.vault_file_name = filename
        self.vault_password = password
        self.mark_modified(is_modified=False)
        self.statusBar().showMessage('Read Vault contents from disk')

        self.change_password.setEnabled(True)
        self.save_as.setEnabled(True)
        self.add_group.setEnabled(True)
        self.add_record.setEnabled(True)
        self.edit_record.setEnabled(True)
        self.remove_record.setEnabled(True)
        self.copy_username.setEnabled(True)
        self.copy_password.setEnabled(True)
        self.open_url.setEnabled(True)

    def save_vault(self, filename, password):
        '''
        Write Vault contents to disk.
        '''
        try:
            self.vault_file_name = filename
            self.vault_password = password
            self.vault.write_to_file(filename, password)
            # self.statusBar().showMessage('Wrote Vault contents to disk')
            self.mark_modified(is_modified=False)
        except RuntimeError:
            QtGui.QMessageBox.critical(self, 'Error writing to disk',
                'Could not write Vault contents to disk',
                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                QtGui.QMessageBox.NoButton)

    def _clear_clipboard(self, match_text=None):
        clipboard = QtGui.QApplication.clipboard()
        if match_text:
            if clipboard.text() != match_text:
                return
        clipboard.clear()
        self.statusBar().showMessage('Cleared clipboard')

    def _copy_to_clipboard(self, text, duration=None):
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(text)
        if duration:
            QtCore.QTimer().singleShot(duration * 1000,
                lambda: self._clear_clipboard(text))

    def _on_list_item_activated(self, item, column):
        '''
        Event handler: Fires when user double-clicks a list entry.
        '''
        # if item.type_() == 'record':
        if isinstance(item, VTWidgetRecordItem):
            # self.list_.editItem(item, column)
            self.list_.deselect_all()
            self.list_.setItemSelected(item, True)
            self._on_edit()
        # elif item.type_() == 'group':
        if isinstance(item, VTWidgetGroupItem):
            self.list_.editItem(item, 0)
            # if column == 0:
            #     self.list_.editItem(item, 0)
            # else:
            #     item.setExpanded(item.isExpanded())

    def _on_settings(self):
        '''
        Event handler: Fires when user chooses this menu item.
        '''
        settings = Settings(self)
        # settings.resize(self._modal_size.width(), settings.size().height())
        settings.exec_()

    def _on_change_password(self):
        if not self.vault:
            return
        value, ok = QtGui.QInputDialog.getText(self, 'Change Vault Password',
            'New password', mode=QtGui.QLineEdit.Password)
        if not ok:
            return
        password_new = unicode(value).encode('latin1', 'replace')
        value, ok = QtGui.QInputDialog.getText(self, 'Change Vault Password',
            'Re-enter new password', mode=QtGui.QLineEdit.Password)
        if not ok:
            return
        password_new_confirm = unicode(value).encode('latin1', 'replace')
        if password_new_confirm != password_new:
            QtGui.QMessageBox.critical(self, 'Bad Password',
                'The given passwords do not match',
                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                QtGui.QMessageBox.NoButton)
            return
        self.vault_password = password_new
        self.statusBar().showMessage('Changed Vault password')
        self.mark_modified(is_modified=True)

    def _on_new(self):
        loadframe = LoadFrame(self, is_new=True)
        loadframe.exec_()
        self._modal_size = loadframe.size()

    def _on_open(self):
        loadframe = LoadFrame(self, is_new=False)
        loadframe.exec_()
        self._modal_size = loadframe.size()

    def _on_save(self):
        if not self.vault:
            return
        if not self.vault_file_name:
            self._on_save_as()
        else:
            self.save_vault(self.vault_file_name, self.vault_password)

    def _on_save_as(self):
        if not self.vault:
            return
        home = os.path.expanduser("~")
        wildcard = ';;'.join(tuple(VAULT_EXT.keys()) + tuple(ALL_EXT.keys()))
        filename, filter_ = QtGui.QFileDialog.getSaveFileNameAndFilter(self,
            caption='Save new Vault as...', directory=home, filter=wildcard)
        if filename:
            if filter_ in VAULT_EXT:
                ext = VAULT_EXT[filter_]
            if not filename.endswith(ext):
                filename += ext
            if filename not in config.recentvaults:
                config.recentvaults.insert(0, filename)
                config.save()
            self.save_vault(filename, self.vault_password)

    def closeEvent(self, event):
        '''
        Event handler: Fires when user chooses this menu item.
        '''
        # TODO: ask before closing
        if self.updater:
            self.updater.stop_me()
        if (config.window_width != self.size().width()
                or config.window_height != self.size().height()):
            config.window_width = self.size().width()
            config.window_height = self.size().height()
            config.save()
        super(VaultFrame, self).closeEvent(event)

    def _on_group_add(self):
        if not self.vault:
            return
        item = VTWidgetGroupItem(self.list_, 'New Group')
        self.list_.editItem(item)
        self.mark_modified(is_modified=True)

    def _on_edit(self):
        '''
        Event handler: Fires when user chooses this menu item.
        '''
        item = self.list_.currentItem()
        if self.vault and item:
            if isinstance(item, VTWidgetRecordItem):
                # save group
                old_group = item.group
                # edit
                recordframe = RecordFrame(self)
                recordframe.record_item = item
                recordframe.resize(self._modal_size.width(),
                    recordframe.size().height())
                if recordframe.exec_() == QtGui.QDialog.Accepted:
                    self.mark_modified(is_modified=True)
                # compare groups
                if item.group != old_group:
                    self.list_.move_to_group(item)
            if isinstance(item, VTWidgetGroupItem):
                self.list_.editItem(item)

    def _on_add(self):
        '''
        Event handler: Fires when user chooses this menu item.
        '''
        if not self.vault:
            return

        recordframe = RecordFrame(self)
        if recordframe.exec_() == QtGui.QDialog.Accepted:
            item = recordframe.record_item
            self.vault.records.append(item.record)
            self.list_.move_to_group(item)
            self.mark_modified(is_modified=True)

    def _on_delete(self):
        '''
        Event handler: Fires when user chooses this menu item.
        '''
        item = self.list_.currentItem()
        if self.vault and item:
            if isinstance(item, VTWidgetRecordItem):
                if item.user or item.passwd:
                    reply = QtGui.QMessageBox.question(self,
                        'Really delete record?',
                        ('Are you sure you want to delete this record? '
                        'It contains a username or password and there is '
                        'no way to undo this action.'),
                        QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply != QtGui.QMessageBox.Yes:
                        return
                self.vault.records.remove(item.record)
            elif isinstance(item, VTWidgetGroupItem):
                # move everyone in this group to root
                children = map(item.child, range(item.childCount()))
                for child in children:
                    child.group = ''
                    self.list_.take_child_from_parent(child)
                self.list_.addTopLevelItems(children)
            self.list_.take_child_from_parent(item)

    def _on_copy_username(self):
        '''
        Event handler: Fires when user chooses this menu item.
        '''
        item = self.list_.currentItem()
        if self.vault and item and isinstance(item, VTWidgetRecordItem):
            self._copy_to_clipboard(item.user)
            self.statusBar().showMessage(
                'Copied username of "%s" to clipboard' % item.title)

    def _on_copy_password(self):
        '''
        Event handler: Fires when user chooses this menu item.
        '''
        item = self.list_.currentItem()
        if self.vault and item and isinstance(item, VTWidgetRecordItem):
            self._copy_to_clipboard(item.passwd, duration=10)
            self.statusBar().showMessage(
                'Copied password of "%s" to clipboard' % item.title)

    def _on_open_url(self):
        '''
        Event handler: Fires when user chooses this menu item.
        '''
        item = self.list_.currentItem()
        if self.vault and item and isinstance(item, VTWidgetRecordItem):
            try:
                import webbrowser
                webbrowser.open(item.url)
            except ImportError:
                self.statusBar().showMessage(
                    'Could not load python module '
                    '"webbrowser" needed to open "%s"' % item.url)

    def on_favicon_ready(self, item):
        self.statusBar().showMessage('Icon retrieved for "%s"' % item.title)
