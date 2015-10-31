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
import pkgutil

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from .config import config


class Settings(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)

        self._sc_length = QtGui.QSpinBox(self)
        self._sc_length.setRange(4, 128)

        self._cb_reduction = QtGui.QCheckBox(
            'Avoid easy to mistake chars', self)

        self._tc_alphabet = QtGui.QLineEdit(config.alphabet, self)

        self._favicon = QtGui.QCheckBox(
            'Download website icons for the records', self)

        self._bt_ok = QtGui.QPushButton('OK', self)
        self._bt_ok.clicked.connect(self._on_ok)
        self._bt_cancel = QtGui.QPushButton('Cancel', self)
        self._bt_cancel.clicked.connect(self._on_cancel)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QtGui.QLabel(
            'Generated Password Length', self), 3, 0)
        grid.addWidget(self._sc_length, 3, 1, 1, 3)
        grid.addWidget(QtGui.QLabel('Alphabet', self), 4, 0)
        grid.addWidget(self._tc_alphabet, 4, 1, 1, 3)
        grid.addWidget(self._cb_reduction, 5, 0, 1, 4)
        grid.addWidget(self._favicon, 6, 0, 1, 4)

        grid.addWidget(self._bt_ok, 7, 2)
        grid.addWidget(self._bt_cancel, 7, 3)

        self.setWindowTitle('PQPasswords - Settings')
        self.setLayout(grid)

        self.set_initial_focus()
        self.update_fields()

    def update_fields(self):
        '''
        Update fields from source
        '''
        self._sc_length.setValue(config.pwlength)
        self._tc_alphabet.setText(config.alphabet)
        self._cb_reduction.setChecked(config.reduction)
        # self._search_notes.setChecked(config.search_notes)
        # self._search_passwd.setChecked(config.search_passwd)
        self._favicon.setChecked(config.favicon)

    def _apply_changes(self):
        '''
        Update source from fields
        '''
        config.pwlength = self._sc_length.value()
        config.reduction = self._cb_reduction.isChecked()
        # config.search_notes = self._search_notes.isChecked()
        # config.search_passwd = self._search_passwd.isChecked()
        config.alphabet = self._tc_alphabet.text()
        config.favicon = self._favicon.isChecked()
        config.save()

    def _on_cancel(self, dummy):
        '''
        Event handler: Fires when user chooses this button.
        '''
        self.reject()

    def _on_ok(self, evt):
        '''
        Event handler: Fires when user chooses this button.
        '''
        self._apply_changes()
        self.accept()

    def set_initial_focus(self):
        self._sc_length.setFocus()
