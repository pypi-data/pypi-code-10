from PyQt5 import QtGui, QtWidgets

from hackedit.api import shortcuts
from hackedit.api.widgets import PreferencePage
from hackedit.app.forms import settings_page_shortcuts_ui


class Shortcuts(PreferencePage):
    def __init__(self):
        super().__init__(
            'Shortcuts', icon=QtGui.QIcon.fromTheme(
                'preferences-desktop-keyboard'), category='Environment')
        self._ui = settings_page_shortcuts_ui.Ui_Form()
        self._ui.setupUi(self)
        self._ui.edit_filter.prompt_text = 'Filter by name or by shortcut'
        self._ui.edit_filter.textChanged.connect(self._filter)
        header_view = self._ui.table.horizontalHeader()
        header_view.setSectionResizeMode(0, header_view.Stretch)
        header_view.setSectionResizeMode(1, header_view.Interactive)

    def _filter(self, filter_text):
        filter_text = filter_text.lower()
        for i in range(self._ui.table.rowCount()):
            name = self._ui.table.item(i, 0).text().lower()
            sequence = QtGui.QKeySequence(filter_text).toString().lower()
            shortcut = self._ui.table.cellWidget(
                i, 1).keySequence().toString().lower()
            if not filter_text or filter_text in name or \
                    (sequence and sequence == shortcut):
                self._ui.table.showRow(i)
            else:
                self._ui.table.hideRow(i)

    def reset(self):
        # force refresh
        shortcuts.load()
        actions = shortcuts.get_all_names()
        self._ui.table.clearContents()
        self._ui.table.setRowCount(len(actions))
        for row, action in enumerate(actions):
            name_item = QtWidgets.QTableWidgetItem()
            name_item.setText(action)
            self._ui.table.setItem(row, 0, name_item)
            edit = QtWidgets.QKeySequenceEdit()
            edit.setKeySequence(QtGui.QKeySequence(
                shortcuts.get(action, None)))
            edit.keySequenceChanged.connect(self.check_for_conflicts)
            edit.setObjectName(action)
            self._ui.table.setCellWidget(row, 1, edit)

    def check_for_conflicts(self, new_sequence):
        if not new_sequence.toString():
            return
        shortcuts = []
        names = []
        for i in range(self._ui.table.rowCount()):
            name = self._ui.table.item(i, 0).text()
            shortcut = self._ui.table.cellWidget(i, 1).keySequence().toString()
            if shortcut in shortcuts:
                existing = names[shortcuts.index(shortcut)]
                if existing != self.sender().objectName():
                    QtWidgets.QMessageBox.warning(
                        self, 'Shortcuts conflict',
                        'The shortcut %s is already used by action %r.\n'
                        'You will need to fix it otherwise both '
                        "shortcus won't work..." % (shortcut, existing))
                break
            else:
                shortcuts.append(shortcut)
                names.append(name)

    def restore_defaults(self):
        shortcuts.restore_defaults()

    def save(self):
        for i in range(self._ui.table.rowCount()):
            action = self._ui.table.item(i, 0).text()
            shortcut = self._ui.table.cellWidget(i, 1).keySequence().toString()
            shortcuts.update(action, shortcut)
        shortcuts.save()
