import shlex

from PyQt5 import QtCore, QtWidgets

from hackedit import api

from hackedit_cobol.forms import dlg_configure_project_ui, \
    dlg_secondary_compilers_ui
from hackedit_cobol.lib.compiler import EXECUTABLE, MODULE, get_compiler_config
from hackedit_cobol.lib.preparsers import get_preparser_for_file
from hackedit_cobol.lib.compiler import get_compiler_config_names


class DlgConfigureBase(QtWidgets.QDialog):
    """
    Base class for dlg configure project and dlg configure file.

    """
    #: Default executable configuration (override build options disabled)
    DEFAULT_EXECUTABLE_CFG = {
        'path': '',
        'filetype': EXECUTABLE,
        'free-format': False,
        'standard': 'default',
        'run': {
            'arguments': [],
            'external-terminal': False,
            'environment-variables': {}
        }
    }

    #: Default module config (override and run disabled by default).
    DEFAULT_MODULE_CFG = {
        'path': '',
        'filetype': MODULE,
        'free-format': False,
        'standard': 'default',
    }

    def get_compiler(self):
        return self.ui.combo_compilers.currentText()

    def __init__(self, parent, title='Configure project'):
        super().__init__(parent)
        self.ui = dlg_configure_project_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.bt_add_var.clicked.connect(self._add_var)
        self.ui.bt_add_var.clicked.connect(self._rm_var)
        self.ui.bt_secondary_compilers.clicked.connect(
            self._select_secondary_compilers)
        self.secondary_compilers = []  # should be set by the concrete impl
        self.ui.combo_compilers.addItems(get_compiler_config_names())
        for i in range(self.ui.combo_compilers.count()):
            self.ui.combo_compilers.setItemIcon(
                i, api.special_icons.run_build())
        self.ui.bt_secondary_compilers.setEnabled(
            self.ui.combo_compilers.count() > 1)

    def _udpate_overrides(self, checked):
        if not checked:
            ccfg = get_compiler_config(self.ui.combo_compilers.currentText())
            self.ui.cb_static.setChecked(ccfg['-static'])
            self.ui.cb_debug.setChecked(ccfg['-debug'])
            self.ui.cb_g.setChecked(ccfg['-g'])
            self.ui.cb_ftrace.setChecked(ccfg['-ftrace'])
            self.ui.cb_ftraceall.setChecked(ccfg['-ftraceall'])
            self.ui.cb_debugging_line.setChecked(ccfg['-fdebugging-line'])
            self.ui.edit_extra_flags.setText(
                ';'.join(ccfg['extra-compiler-flags']))
            self.ui.list_copy_paths.addItems(ccfg['copybook-paths'])
            self.ui.list_lib_paths.addItems(ccfg['library-paths'])
            self.ui.edit_libs.setText(' '.join(ccfg['libraries']))

    def display_file_config(self, cfg, fpath):
        preparser = get_preparser_for_file(fpath)
        if preparser:
            enable_build = not preparser.only_preparser
            self.ui.lbl_preparser_name.setText(preparser.config['name'])
        else:
            enable_build = True
            self.ui.lbl_preparser_name.setText('None')
        self.ui.tabWidget.setEnabled(enable_build)
        ftype = cfg['filetype']
        self.ui.combo_type.setCurrentIndex(ftype if ftype is not None else 0)
        self.ui.cb_free_format.setChecked(cfg['free-format'])
        self.ui.combo_standard.setCurrentText(cfg['standard'])
        # Override build options
        try:
            ocfg = cfg['override']
        except KeyError:
            # use default settings
            self.ui.group_override_build_options.setChecked(False)
            ccfg = get_compiler_config(self.ui.combo_compilers.currentText())
            self.ui.cb_static.setChecked(ccfg['-static'])
            self.ui.cb_debug.setChecked(ccfg['-debug'])
            self.ui.cb_g.setChecked(ccfg['-g'])
            self.ui.cb_ftrace.setChecked(ccfg['-ftrace'])
            self.ui.cb_ftraceall.setChecked(ccfg['-ftraceall'])
            self.ui.cb_debugging_line.setChecked(ccfg['-fdebugging-line'])
            self.ui.edit_extra_flags.setText(
                ';'.join(ccfg['extra-compiler-flags']))
            self.ui.list_copy_paths.addItems(ccfg['copybook-paths'])
            self.ui.list_lib_paths.addItems(ccfg['library-paths'])
            self.ui.edit_libs.setText(' '.join(ccfg['libraries']))
        else:
            # override default settings
            self.ui.group_override_build_options.setChecked(True)
            self.ui.cb_static.setChecked(ocfg['-static'])
            self.ui.cb_debug.setChecked(ocfg['-debug'])
            self.ui.cb_g.setChecked(ocfg['-g'])
            self.ui.cb_ftrace.setChecked(ocfg['-ftrace'])
            self.ui.cb_ftraceall.setChecked(ocfg['-ftraceall'])
            self.ui.cb_debugging_line.setChecked(ocfg['-fdebugging-line'])
            self.ui.edit_extra_flags.setText(
                ';'.join(ocfg['extra-compiler-flags']))
            self.ui.list_copy_paths.addItems(ocfg['copybook-paths'])
            self.ui.list_lib_paths.addItems(ocfg['library-paths'])
            self.ui.edit_libs.setText(' '.join(ocfg['libraries']))
        # Run options
        try:
            run_cfg = cfg['run']
        except KeyError:
            self.ui.group_run.setChecked(False)
            self.ui.edit_args.setText('')
            self.ui.cb_external_term.setChecked(False)
            self.ui.table_vars.clearContents()
        else:
            self.ui.group_run.setChecked(True)
            self.ui.edit_args.setText(' '.join(run_cfg['arguments']))
            self.ui.cb_external_term.setChecked(
                run_cfg['external-terminal'])
            try:
                env = run_cfg['environment-variables']
            except KeyError:
                self.ui.table_vars.setRowCount(0)
            else:
                self.ui.table_vars.setRowCount(len(env.items()))
                for i, (k, v) in enumerate(env.items()):
                    kitem = QtWidgets.QTableWidgetItem()
                    kitem.setText(k)
                    self.ui.table_vars.setItem(i, 0, kitem)
                    vitem = QtWidgets.QTableWidgetItem()
                    vitem.setText(v)
                    self.ui.table_vars.setItem(i, 1, vitem)
        try:
            self.ui.cb_compile_submodules.setChecked(cfg['compile-submodules'])
        except KeyError:
            pass

    def get_current_config(self, path):
        cfg = {
            'filetype': self.ui.combo_type.currentIndex(),
            'standard': self.ui.combo_standard.currentText(),
            'free-format': self.ui.cb_free_format.isChecked()
        }
        if path:
            cfg['path'] = path
        # override build options, if any...
        if self.ui.group_override_build_options.isChecked():
            flags = [t for t in self.ui.edit_extra_flags.text().split(';')
                     if t]
            ocfg = {
                '-static': self.ui.cb_static.isChecked(),
                '-debug': self.ui.cb_debug.isChecked(),
                '-g': self.ui.cb_g.isChecked(),
                '-ftrace': self.ui.cb_ftrace.isChecked(),
                '-ftraceall': self.ui.cb_ftraceall.isChecked(),
                '-fdebugging-line': self.ui.cb_debugging_line.isChecked(),
                'extra-compiler-flags': flags,
                'libraries': shlex.split(self.ui.edit_libs.text(),
                                         posix=False),
                'library-paths':
                    [self.ui.list_lib_paths.item(i).text() for i in range(
                        self.ui.list_lib_paths.count())],
                'copybook-paths':
                    [self.ui.list_copy_paths.item(i).text() for i in range(
                        self.ui.list_copy_paths.count())]
            }
            cfg['override'] = ocfg
        # run options, if any...
        if self.ui.group_run.isChecked():
            args = shlex.split(self.ui.edit_args.text(), posix=False)
            rcfg = {
                'arguments': args,
                'external-terminal': self.ui.cb_external_term.isChecked()
            }
            env = {}
            for i in range(self.ui.table_vars.rowCount()):
                key = self.ui.table_vars.item(i, 0).text()
                value = self.ui.table_vars.item(i, 1).text()
                env[key] = value
            rcfg['environment-variables'] = env
            cfg['run'] = rcfg
        if self.ui.cb_compile_submodules.isEnabled():
            cfg['compile-submodules'] = \
                self.ui.cb_compile_submodules.isChecked()
        return cfg

    def _add_var(self):
        index = self.ui.table_vars.rowCount()
        self.ui.table_vars.insertRow(index)
        focus_item = QtWidgets.QTableWidgetItem()
        self.ui.table_vars.setItem(index, 0, focus_item)
        self.ui.table_vars.setItem(index, 1, QtWidgets.QTableWidgetItem())
        self.ui.table_vars.scrollToItem(focus_item)
        self.ui.table_vars.editItem(focus_item)

    def _rm_var(self):
        self.ui.table_vars.removeRow(self.ui.table_vars.currentRow())

    def _select_secondary_compilers(self):
        all_compilers = get_compiler_config_names()
        main_compiler = self.ui.combo_compilers.currentText()
        values = DlgSecondaryCompilers.select_secondary_compilers(
            main_compiler, self.secondary_compilers, all_compilers, self)
        if values:
            self.secondary_compilers = values


class DlgSecondaryCompilers(QtWidgets.QDialog):
    def __init__(self, all_compilers, main_compiler, secondary_compilers,
                 parent):
        super().__init__(parent)
        self.ui = dlg_secondary_compilers_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Select secondary compilers')
        all_compilers.remove(main_compiler)
        for name in all_compilers:
            item = QtWidgets.QListWidgetItem(
                api.special_icons.run_build(), name)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(
                QtCore.Qt.Checked if name in secondary_compilers else
                QtCore.Qt.Unchecked)
            self.ui.listWidget.addItem(item)

    def get_checked_compilers(self):
        ret_val = []
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                ret_val.append(item.text())
        return ret_val

    @classmethod
    def select_secondary_compilers(
            cls, main_compiler, secondary_compilers, all_compilers,
            parent):
        dlg = DlgSecondaryCompilers(all_compilers, main_compiler,
                                    secondary_compilers, parent)
        if dlg.exec_():
            return dlg.get_checked_compilers()
