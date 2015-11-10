"""
This module implements the wizard used to create new project/files
"""
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from hackedit.api.widgets import FileIconProvider
from hackedit.app import boss_wrapper as boss
from hackedit.app.forms import wizard_new_ui


class WizardNew(QtWidgets.QWizard):
    def __init__(self, parent, current_project):
        super().__init__(parent)
        self.home_path = os.path.expanduser('~')
        if not current_project:
            current_project = self.home_path
        self.current_project = current_project
        self.ui = wizard_new_ui.Ui_Wizard()
        self.ui.setupUi(self)
        self.ui.lbl_boss_version.setText(
            '<i>Powered by <a href="https://github.com/datafolklabs/boss">'
            'BOSS</a> (v%s)</i>' % boss.version())
        font = self.ui.lbl_boss_version.font()
        font.setPointSize(8)
        self.ui.lbl_boss_version.setFont(font)
        self.ui.list_sources.currentItemChanged.connect(self.update_templates)
        self.ui.tree_templates.currentItemChanged.connect(
            self.update_next_btn)
        self.ui.edit_prj_path.textChanged.connect(self.check_path)
        self.update_sources()

    def update_sources(self):
        row = self.ui.list_sources.currentRow()
        if row == -1:
            row = 0
        self.ui.list_sources.clear()
        for src in boss.sources():
            item = QtWidgets.QListWidgetItem()
            item.setText(src['label'])
            if src['is_local']:
                item.setIcon(QtGui.QIcon.fromTheme('folder'))
            else:
                item.setIcon(QtGui.QIcon.fromTheme('folder-remote'))
            item.setData(QtCore.Qt.UserRole, src)
            self.ui.list_sources.addItem(item)
        self.ui.list_sources.setCurrentRow(row)

    def validateCurrentPage(self):
        is_valid = self.is_valid
        if is_valid:
            if self.currentId() == 0:
                item = self.ui.tree_templates.currentItem()
                label, templ = item.data(0, QtCore.Qt.UserRole)
                meta = boss.get_template_metadata(label, templ)
                if meta and meta['category'] == 'File':
                    self.single_file = True
                    self.ui.edit_prj_path.setText(self.current_project)
                else:
                    self.single_file = False
                    self.ui.edit_prj_path.setText(self.home_path)
                self.label = label
                self.template = templ
            elif self.currentId() == 1:
                self.path = self.ui.edit_prj_path.text()
        return is_valid

    def update_templates(self, item):
        project_tree_node = self.ui.tree_templates.topLevelItem(0)
        files_tree_node = self.ui.tree_templates.topLevelItem(1)
        uncategorized_tree_node = self.ui.tree_templates.topLevelItem(2)

        for node in [project_tree_node, files_tree_node,
                     uncategorized_tree_node]:
            node.takeChildren()

        if item is None:
            self.ui.tree_templates.setEnabled(False)
        else:
            self.button(self.NextButton).setEnabled(True)
            self.ui.tree_templates.setEnabled(True)
            for label, templ in boss.templates():
                if label == item.text():
                    meta = boss.get_template_metadata(label, templ)
                    name = templ
                    description = ''
                    parent = uncategorized_tree_node
                    icon = 'folder'
                    if meta:
                        name = meta['name']
                        description = meta['name']
                        cat = meta['category']
                        try:
                            icon = meta['icon']
                        except KeyError:
                            pass
                        if cat == 'Project':
                            parent = project_tree_node
                        elif cat == 'File':
                            parent = files_tree_node
                            if icon == 'folder':
                                icon = 'document'
                    titem = QtWidgets.QTreeWidgetItem()
                    titem.setText(0, name)
                    titem.setToolTip(0, description)
                    if icon.startswith(':') or os.path.exists(icon):
                        icon = QtGui.QIcon(icon)
                    elif icon.startswith('file.'):
                        icon = FileIconProvider().icon(icon)
                    else:
                        icon = QtGui.QIcon.fromTheme(icon)
                    titem.setIcon(0, icon)
                    titem.setData(0, QtCore.Qt.UserRole, (label, templ))
                    parent.addChild(titem)
        flg_select = False
        for node in [project_tree_node, files_tree_node,
                     uncategorized_tree_node]:
            node.setExpanded(True)
            if not flg_select and node.childCount():
                self.ui.tree_templates.setCurrentItem(node.child(0))
                flg_select = True
            node.setHidden(not node.childCount())

    def update_next_btn(self, item):
        self.is_valid = item is not None and item.data(
            0, QtCore.Qt.UserRole) is not None
        self.button(self.NextButton).setEnabled(self.is_valid)

    def check_path(self, path):
        ok = False
        message = ''
        if os.path.isdir(path):
            if not self.single_file and os.listdir(path):
                message = 'Directory is not empty'
            else:
                ok = True
        elif os.path.exists(path):
            message = 'Path does is not a directory'
        else:
            ok = True
        self.ui.lbl_prj_location_error.setHidden(ok)
        self.ui.lbl_prj_location_error.setText(message)
        self.is_valid = ok

    @classmethod
    def get_parameters(cls, parent=None, current_project=None):
        wizard = WizardNew(parent, current_project)
        if wizard.exec_() == wizard.Accepted:
            return wizard.label, wizard.template, wizard.path, \
                wizard.single_file
        return None, None, None, None
