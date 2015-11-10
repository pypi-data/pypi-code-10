"""
Base class for the file/project manager
"""
import shutil
import logging
import os
import shlex

from PyQt5 import QtCore, QtGui, QtWidgets
from hackedit import api
from pyqode.core.modes import CheckerMessage, CheckerMessages
from pyqode.core.widgets import ErrorsTable

from hackedit_cobol.lib.compiler import GnuCOBOLCompiler, EXECUTABLE, \
    get_compiler_config


class CobolManagerPluginBase(api.plugins.WorkspacePlugin):
    configuration_changed = QtCore.pyqtSignal()

    def setup_ui(self):
        self.build_output_dock = None
        self.build_output = None
        self.issues_dock = None
        self.issues_table = None
        self.run_dock = None
        self.run_widget = None

        # toolbar and menu
        cob_menu = api.window.get_menu('C&OBOL')
        cob_toolbar = api.window.get_toolbar('cobolToolBar', 'COBOLToolBar')

        # configure
        self.a_configure = cob_menu.addAction('Configure')
        self.a_configure.setIcon(api.special_icons.configure_icon(build=True))
        self.a_configure.setShortcut(api.shortcuts.get('Configure', 'F8'))
        self.a_configure.setToolTip('Configure')
        self.a_configure.setMenuRole(self.a_configure.NoRole)
        cob_toolbar.addAction(self.a_configure)

        # build
        self.a_build = cob_menu.addAction('Build')
        self.a_build.setIcon(api.special_icons.run_build())
        self.a_build.setToolTip('Build')
        self.a_build.setShortcut(api.shortcuts.get('Build', 'Ctrl+B'))
        cob_toolbar.addAction(self.a_build)

        # clean
        self.a_clean = cob_menu.addAction('Clean')
        self.a_clean.setIcon(api.special_icons.build_clean())
        self.a_clean.setToolTip('Clean')
        self.a_clean.setShortcut(api.shortcuts.get('Clean', 'Ctrl+Alt+C'))
        self.a_clean.setShortcutContext(QtCore.Qt.WindowShortcut)
        self._window.addAction(self.a_clean)
        cob_toolbar.addAction(self.a_clean)

        self.a_rebuild = cob_menu.addAction('Rebuild')
        self.a_rebuild.setIcon(QtGui.QIcon.fromTheme('view-refresh'))
        self.a_rebuild.setToolTip('Rebuild')
        self.a_rebuild.setShortcut(api.shortcuts.get(
            'Rebuild', 'Ctrl+Alt+B'))
        self.a_clean.setShortcutContext(QtCore.Qt.WindowShortcut)
        self._window.addAction(self.a_rebuild)
        cob_toolbar.addAction(self.a_rebuild)

        cob_toolbar.addSeparator()

        # run
        self.a_run = cob_menu.addAction('Run')
        self.a_run.setIcon(api.special_icons.run_icon())
        self.a_run.setShortcut(api.shortcuts.get('Run', 'F9'))
        self.a_run.setToolTip('Run')
        cob_toolbar.addAction(self.a_run)

    def _setup_run_dock(self):
        self.run_widget = api.widgets.RunWidget(self._window)
        self.run_widget.last_tab_closed.connect(self._remove_run_dock)
        self.run_dock = api.window.add_dock_widget(
            self.run_widget, 'Run', api.special_icons.run_icon())

    def _remove_run_dock(self):
        api.window.remove_dock_widget(self.run_dock)
        self.run_widget = None
        self.run_dock = None

    def _on_command_finished(self, command, input_file_path, status, output):
        working_directory = os.path.dirname(input_file_path)
        if self.build_output_dock is None:
            self._setup_build_output_dock()
        self.build_output.setTextColor(self.command_color)
        self.build_output.append(command)
        if output:
            self.build_output.setTextColor(self.text_color)
            self.build_output.append(output)
        if not self.issues_dock:
            self._setup_issues_dock()

        if status != 0:
            # parse output and add some issues
            msgs = GnuCOBOLCompiler.parse_output(output, working_directory)
            if msgs:
                for msg in msgs:
                    self.issues_table.add_message(msg)
            else:
                self.issues_table.add_message(
                    CheckerMessage(
                        'Command failed: see the "Compile output" pane for the'
                        ' full output...',
                        CheckerMessages.ERROR, -1, path=input_file_path))
        else:
            # add an entry to indicate that the compilation was successfull
            if output.strip() != '' or len(output) == 0:
                output = 'Compilation succeeded'
            self.issues_table.add_message(
                CheckerMessage(output, CheckerMessages.INFO, -1,
                               path=input_file_path))

        self.build_output_dock.show()

    def _setup_build_output_dock(self):
        self.build_output = QtWidgets.QTextEdit()
        self.build_output.setReadOnly(True)
        self.build_output_dock = api.window.add_dock_widget(
            self.build_output, 'Compile output',
            icon=api.special_icons.run_build())
        self.text_color = self.build_output.palette().text().color()
        self.command_color = QtCore.Qt.blue if not api.utils.is_dark_theme() \
            else self.build_output.palette().highlight().color()

    def _setup_issues_dock(self):
        self.issues_table = ErrorsTable()
        self.issues_table.msg_activated.connect(self._on_issue_clicked)
        self.issues_dock = api.window.add_dock_widget(
            self.issues_table, 'Issues',
            icon=QtGui.QIcon.fromTheme('dialog-error'))

    def _on_issue_clicked(self, issue):
        api.editor.open_file(issue.path, line=issue.line)

    def _on_build_errored(self, path, exception, tb):
        if self.build_output_dock is None:
            self._setup_build_output_dock()
        if self.issues_dock is None:
            self._setup_issues_dock()
        color = self.build_output.textColor()
        self.build_output.setTextColor(QtCore.Qt.red)
        self.build_output.append('Exception while compiling file: %r \n'
                                 'Error=%r' % (path, str(exception)))
        self.build_output.setTextColor(color)
        self.issues_table.add_message(CheckerMessage(
            'Exception while compiling: %r' % str(exception),
            CheckerMessages.ERROR, -1, path=path))
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText('Exception while compiling')
        msg_box.setInformativeText(
            'An exception occured while compiling %s\nError=%s' %
            (path, str(exception)))
        msg_box.setIcon(msg_box.Warning)
        msg_box.setDetailedText(tb)
        msg_box.exec_()

    def _on_config_message(self, msg):
        if self.build_output_dock is None:
            self._setup_build_output_dock()
        color = self.build_output.textColor()
        self.build_output.setTextColor(QtCore.Qt.darkGreen)
        self.build_output.append(msg)
        self.build_output.setTextColor(color)

    def _on_config_skipped(self, msg):
        if self.build_output_dock is None:
            self._setup_build_output_dock()
        color = self.build_output.textColor()
        self.build_output.setTextColor(QtCore.Qt.darkYellow)
        self.build_output.append(msg)
        self.build_output.setTextColor(color)

    def _on_build_finished(self, success):
        self.a_build.setIcon(api.special_icons.run_build())
        self.a_build.setText('Compile')
        self.a_build.setToolTip('Compile current editor')
        self.enable_build_actions()
        if self.build_thread.abort:
            if self.build_output_dock is None:
                self._setup_build_output_dock()
            self.build_output.setTextColor(QtCore.Qt.red)
            self.build_output.append('Aborted')
        else:
            self.build_output.setTextColor(QtCore.Qt.darkGreen)
            ev = api.events.Event(
                'Build finished',
                'Compilation finished with success.' if success else
                'Compilation finished with errors',
                level=api.events.INFO if success else api.events.WARNING)
            api.events.post(ev, show_balloon=not self.build_output.isVisible())
            self.issues_dock.show()
        self.build_thread = None
        if self._flg_run:
            self._run()

    def _remove_path(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                try:
                    os.remove(path)
                except OSError as e:
                    ev = api.events.Event(
                        'Clean: failed to remove file',
                        'Failed to remove %r\nError: %s' % (path, e),
                        level=api.events.WARNING)
                    api.events.post(ev)
                else:
                    return path
            else:
                try:
                    shutil.rmtree(path)
                except OSError as e:
                    ev = api.events.Event(
                        'Clean: failed to remove directory',
                        'Failed to remove %r\nError: %s' % (path, e),
                        level=api.events.WARNING)
                    api.events.post(ev)
                else:
                    return path
        return None

    def rebuild(self):
        self.clean()
        self.build()

    def run(self):
        self._flg_run = True
        self.build()

    def run_in_external_terminal(self, path, cfg, cfg_name):
        wd = os.path.dirname(path)
        executable = cfg['filetype'] == EXECUTABLE
        compiler_cfg = get_compiler_config(cfg_name)
        if not executable:
            program = compiler_cfg['cobcrun']
            arguments = [QtCore.QFileInfo(path).baseName()] + \
                cfg['run']['arguments']
            number_of_params = 3
        else:
            number_of_params = 2
            program = path
            arguments = cfg['run']['arguments']

        cmd = ' '.join([program] + arguments)
        cmd = api.utils.get_cmd_run_command_in_terminal() % cmd
        tokens = shlex.split(cmd, posix=False)

        if api.system.LINUX:
            tokens = tokens[:2] + [' '.join(tokens[-number_of_params:])]

        pgm, args = tokens[0], tokens[1:]
        env = os.environ.copy()
        for k, v in cfg['run']['environment-variables']:
            os.environ[k] = v
        os.environ['path'] = GnuCOBOLCompiler(
            compiler_cfg).setup_environment().value('PATH')
        QtCore.QProcess.startDetached(pgm, args, wd)
        api.events.post(
            api.events.Event('Program running in external terminal', cmd),
            force_show=True)
        os.environ = env

    def run_embedded(self, pgm, args, file_cfg, compiler_cfg, path):
        cwd = os.path.dirname(path)
        _logger().info('running program in embedded console')
        _logger().info('command: %s' % ' '.join([pgm] + args))
        _logger().info('working_directory: %s' % cwd)
        env = file_cfg['run']['environment-variables']
        env['path'] = GnuCOBOLCompiler(
            compiler_cfg).setup_environment().value('PATH')
        self.run_widget.run_program(pgm, args, cwd, env=env)


def _logger():
    return logging.getLogger(__name__)
