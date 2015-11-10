import os

from PyQt5 import QtCore, QtGui, QtWidgets

from hackedit.app import settings
from hackedit.api.widgets import PreferencePage, FileIconProvider
from hackedit.app import boss_wrapper as boss
from hackedit.app.forms import settings_page_templates_ui
from hackedit.app.forms import dlg_add_boss_source_ui


class Templates(PreferencePage):
    """
    A page for configuring general editor settings (settings that apply
    to any editor independently from the target language).
    """
    can_reset = False
    can_restore_defaults = False
    can_apply = False

    def __init__(self):
        icon = QtGui.QIcon.fromTheme('folder-templates')
        super().__init__('Templates', icon=icon)
        self.ui = settings_page_templates_ui.Ui_Form()
        self.ui.setupUi(self)
        self.ui.lbl_boss_version.setText(
            '<i>Powered by <a href="https://github.com/datafolklabs/boss">'
            'BOSS</a> (v%s)</i>' % boss.version())
        font = self.ui.lbl_boss_version.font()
        font.setPointSize(8)
        self.ui.lbl_boss_version.setFont(font)
        self.ui.list_sources.currentItemChanged.connect(
            self.update_source_details)
        self.ui.bt_sync.clicked.connect(self.sync)
        self.ui.bt_rm_source.clicked.connect(self.rm_source)
        self.ui.bt_add_source.clicked.connect(self.add_source)
        self.update_sources()
        self.update_source_details(self.ui.list_sources.currentItem())

    def update_sources(self):
        row = self.ui.list_sources.currentRow()
        if row == -1:
            row = 0
        self.ui.list_sources.clear()
        sources = boss.sources()
        if not sources:
            return
        for src in sources:
            # if src['label'] == 'boss':
            #     # don't show boss templates, they miss the metadata tag
            #     continue
            item = QtWidgets.QListWidgetItem()
            item.setText(src['label'])
            if src['is_local']:
                item.setIcon(QtGui.QIcon.fromTheme('folder'))
            else:
                item.setIcon(QtGui.QIcon.fromTheme('folder-remote'))
            item.setData(QtCore.Qt.UserRole, src)
            self.ui.list_sources.addItem(item)
        self.ui.list_sources.setCurrentRow(row)

    def update_source_details(self, item):
        if item is None:
            self.ui.edit_source_label.clear()
            self.ui.edit_source_cache.clear()
            self.ui.edit_source_path.clear()
            self.ui.edit_sync_time.clear()
            self.ui.list_templates.clear()
            self.ui.group_details.setDisabled(True)
            self.ui.bt_rm_source.setDisabled(True)
        else:
            self.ui.group_details.setDisabled(False)
            self.ui.bt_rm_source.setDisabled(False)
            src = item.data(QtCore.Qt.UserRole)
            self.ui.edit_source_label.setText(src['label'])
            self.ui.edit_source_cache.setText(src['cache'])
            self.ui.edit_source_path.setText(src['path'])
            try:
                self.ui.edit_sync_time.setText(src['last_sync_time'].strftime(
                    "%Y-%m-%d %H:%M:%S"))
            except AttributeError:
                self.ui.edit_sync_time.setText(src['last_sync_time'])
            self.ui.list_templates.clear()
            for label, templ in boss.templates():
                if label == item.text():
                    titem = QtWidgets.QListWidgetItem()
                    titem.setText(templ)
                    icon = 'folder'
                    meta = boss.get_template_metadata(label, templ)
                    if meta:
                        try:
                            icon = meta['icon']
                        except KeyError:
                            pass
                    if icon.startswith(':') or os.path.exists(icon):
                        icon = QtGui.QIcon(icon)
                    elif icon.startswith('file.'):
                        icon = FileIconProvider().icon(icon)
                    else:
                        icon = QtGui.QIcon.fromTheme(icon)
                    titem.setIcon(icon)
                    self.ui.list_templates.addItem(titem)

    def sync(self):
        QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
        boss.sync()
        QtWidgets.qApp.restoreOverrideCursor()
        self.update_sources()

    def rm_source(self):
        source = self.ui.list_sources.currentItem().text()
        answer = QtWidgets.QMessageBox.question(
            self, 'Remove source', 'Are you sure you want to remove the '
            'source %r?' % source)
        if answer == QtWidgets.QMessageBox.Yes:
            QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
            boss.rm_source(source)
            QtWidgets.qApp.restoreOverrideCursor()
        self.update_sources()

    def add_source(self):
        label, url = DlgAddSource.add_source(self)
        if label and url:
            local = os.path.exists(url)
            boss.add_source(label, url, local=local)
        self.update_sources()

    def reset(self):
        self.ui.cb_auto_sync.setChecked(settings.auto_sync_templates())

    def restore_defaults(self):
        settings.set_auto_sync_templates(True)

    def save(self):
        settings.set_auto_sync_templates(self.ui.cb_auto_sync.isChecked())


class DlgAddSource(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = dlg_add_boss_source_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.edit_label.textChanged.connect(self.enable_ok)
        self.ui.edit_url.textChanged.connect(self.enable_ok)

    def enable_ok(self):
        bt = self.ui.buttonBox.button(self.ui.buttonBox.Ok)
        bt.setDisabled(
            not self.ui.edit_label.text() or not self.ui.edit_url.text())

    @classmethod
    def add_source(cls, parent):
        dlg = DlgAddSource(parent)
        if dlg.exec_() == dlg.Accepted:
            return dlg.ui.edit_label.text().strip(), \
                dlg.ui.edit_url.text().strip()
        return None, None
