"""
This module contains an API for easily integrating a new interpreter in
hackedit. The API has been made to integrate the python interpreter but it
could **theorically** be used for Ruby, Perl,...

To integrate a new interpreter into hackedit, you just need to:

    - implement an InterpreterManager (especially _detect_system_interpreters)
    - create a plugin which inherits from ScriptRunnerPlugin and use your
      new InterpreterManager.

See :mod:`hackedit_python.run` for a concrete example.

"""
import json
import os
import shlex

from PyQt5 import QtGui, QtCore, QtWidgets

from . import (editor, events, plugins, project, shortcuts, widgets, window,
               signals, special_icons, utils)
from hackedit.app import mime_types
from hackedit.app.forms import dlg_script_run_config_ui


class InterpreterManager:
    """
    Base class that manages a collection of interpreter (e.g. python2, python3,
    local interpreters).
    """
    @property
    def extensions(self):
        return mime_types.get_extensions(self.mimetype)

    def __init__(self, name, default_interpreter=None, mimetype=None):
        """
        :param name: Name of the interpreter (e.g. python, ruby,...)
        :param default_interpreter: Default interpreter value (e.g.
            sys.executable)
        """
        self.name = name
        self.mimetype = mimetype
        self._default_interpreter = default_interpreter

    @property
    def default_interpreter(self):
        """
        Gets the default interpreter.

        :return: Default interpreter path.
        """
        default = self._default_interpreter
        if default is None or not os.path.exists(default):
            default = self.all_interpreters[0]
        return QtCore.QSettings().value(
            '%s/default' % self.name, default)

    @default_interpreter.setter
    def default_interpreter(self, interpreter):
        """
        Sets the default interpreter.

        :param interpreter: Default interpreter.
        """
        QtCore.QSettings().setValue('%s/default' % self.name, interpreter)

    @property
    def all_interpreters(self):
        """
        Gets all interpreters.
        :return: list of interpreter paths
        """
        return sorted(set(self._detect_system_interpreters() +
                          self._get_locals()))

    def add_interpreter(self, path):
        """
        Adds an interpreter path to the list of known interpreters.

        :param path: interpreter path to add.
        """
        l = self._get_locals()
        l.append(path)
        self._set_locals(l)

    def remove_interpreter(self, path):
        """
        Removes the given interpreter from the list of known interpreters

        :param path: interpreter path to remove.
        """
        locals = self._get_locals()
        try:
            locals.remove(path)
        except ValueError:
            pass
        else:
            self._set_locals(locals)

    def get_project_interpreter(self, project_path):
        """
        Gets the project interprerter.

        The interpreter path is stored into .hackedit/config.usr

        :param project_path: project path

        :return: path to the project interpreter or None if the list
                 of known interpreter is empty and no interpreter has been
                 defined for the project.
        """
        try:
            return project.load_user_config(project_path)['interpreter']
        except KeyError:
            # use the first interpreter available
            return self.default_interpreter

    def set_project_interpreter(self, project_path, interpreter):
        """
        Sets the project interpreter.

        :param project_path: project path
        :param interpreter: interpreter to use for project_path
        """
        usd = project.load_user_config(project_path)
        usd['interpreter'] = interpreter
        project.save_user_config(project_path, usd)

    def _detect_system_interpreters(self):
        """
        Detects system interpreters. This method does not do anything, it's up
        to you to implement it
        """
        return []

    def _get_locals(self):
        """
        Gets the local interpreters, added by users.
        """
        ret_val = []
        lst = QtCore.QSettings().value('%s/local_interpreters' % self.name, [])
        if lst:
            for pth in lst:
                if os.path.exists(pth):
                    ret_val.append(pth)
        else:
            ret_val = []
        return ret_val

    def _set_locals(self, interpreters):
        """
        Sets the local interpreters, added by users.
        """
        QtCore.QSettings().setValue(
            '%s/local_interpreters' % self.name, list(set(interpreters)))

    def get_interpreter_icon(self):
        """
        Returns the icon used for the interpreter.

        Subclass may want to override this icon to provide an icon for the
        interpreter. This icon will show up in the run config dialog.

        The default implementation returns an empty icon.
        """
        return QtGui.QIcon()


class ScriptRunnerPlugin(plugins.WorkspacePlugin):
    """
    Base class for adding the ability to run script within hackedit.

    This plugin will add a combo box with the project run configuration, an
    action to change/edit run configurations and an action to run the active
    config.

    To add support for a new interpreter, subclass this plugin and pass
    it you own custom interpreter manager and, optionally, the run console
    widget to use for running the program.
    """
    #: Signal emitted when the list of configs has been refreshed.
    #: Parameter specifies whether there is an active config or not.
    config_refreshed = QtCore.pyqtSignal(bool)

    def __init__(self, _window, interpreter_manager, run_console=None):
        super().__init__(_window)
        self.run_console = run_console
        self.interpreter_manager = interpreter_manager
        self._loading_configs = False
        signals.connect_slot(signals.CURRENT_PROJECT_CHANGED, self.refresh)
        signals.connect_slot(signals.PROJECT_ADDED, self.refresh)
        self._dock_run = None
        self._run_widget = None
        self._setup_menu()
        self._setup_combo_box()
        self._setup_toolbar()
        if not self.interpreter_manager.all_interpreters:
            # todo: interpreter missing event with a fixme action
            # that open the application preferences to the interpreters
            # tab.
            name = self.interpreter_manager.name
            ev = events.Event(
                'No interpreter found',
                '%s: no interpreter found' % name.capitalize(),
                level=events.WARNING)
            events.post(ev)

    def enable_run(self):
        """
        Updates run action state (will get enabled/disabled dependending on
        whether there is an active run config or not)
        """
        enabled = self.get_active_config() is not None
        self.config_refreshed.emit(enabled)
        self._action_run.setEnabled(enabled)

    def enable_mnu_configs(self):
        """
        Enables/Disables configs menu depending on its content.
        """
        self._mnu_configs.setEnabled(len(self._mnu_configs.actions()))

    def run(self):
        """
        Runs the active configuration
        """
        editor.save_all_editors()
        cfg = self.get_active_config()
        for prj in project.get_projects():
            if not os.path.relpath(cfg['working_dir'], prj).startswith('..'):
                base_path = prj
                break
        else:
            # not in a project, use active project interpreter.
            base_path = project.get_current_project()
        script = os.path.abspath(os.path.join(base_path, cfg['script']))
        cwd = os.path.abspath(os.path.join(base_path, cfg['working_dir']))
        args = []
        if len(cfg['interpreter_options']):
            args += cfg['interpreter_options']
        args += [script]
        if len(cfg['script_parameters']):
            args += cfg['script_parameters']
        interpreter = self.interpreter_manager.get_project_interpreter(
            base_path)

        try:
            external_terminal = cfg['run_in_external_terminal']
        except KeyError:
            external_terminal = False

        if not external_terminal:
            if self._dock_run is None:
                self._create_dock()
            console = self._run_widget.run_program(
                interpreter, args=args, cwd=cwd, env=cfg['environment'],
                name=cfg['name'], klass=self.run_console)
            try:
                console.open_file_requested.connect(
                    self._on_open_file_requested,
                    type=QtCore.Qt.UniqueConnection)
            except TypeError:
                pass
        else:
            # todo run in external terminal.
            cmd = ' '.join([interpreter] + args)
            cmd = utils.get_cmd_run_command_in_terminal() % cmd
            tokens = shlex.split(cmd, posix=False)
            pgm, args = tokens[0], tokens[1:]
            QtCore.QProcess.startDetached(pgm, args, cwd)
            events.post(
                events.Event('Program running in external terminal', cmd),
                force_show=True)

    def configure(self):
        """
        Edit configuration of the current editor.
        """
        try:
            active = self._configs_combo_box.currentText()
        except AttributeError:
            active = ''
        _DlgScriptRunConfiguration.edit_configurations(
            self._window, self.interpreter_manager, active)
        self.refresh()
        self._mnu_configs.setEnabled(len(self._mnu_configs.actions()))
        enabled = self.get_active_config() is not None
        self.config_refreshed.emit(enabled)
        self._action_run.setEnabled(enabled)

    def get_active_config(self):
        configs = []
        for pth in project.get_projects():
            configs += load_configs(pth)
        if len(configs):
            config_name = self._configs_group.checkedAction(
                ).text().replace('&', '')
            for config in configs:
                if config['name'] == config_name:
                    return config
            return configs[0]
        else:
            return None

    def refresh(self):
        try:
            self._loading_configs = True
        except AttributeError:
            return
        self._mnu_configs.clear()
        self._configs_combo_box.clear()
        actions = self._configs_group.actions()
        for a in actions:
            self._configs_group.removeAction(a)
        configs = []
        for pth in reversed(project.get_projects()):
            configs += load_configs(pth)
            active = get_active_config_name(pth, configs)
        for config in sorted(configs, key=lambda x: x['name']):
            action = self._mnu_configs.addAction(config['name'])
            action.setCheckable(True)
            action.setMenuRole(action.NoRole)
            icon = widgets.FileIconProvider().icon(
                self.interpreter_manager.extensions[0].replace('*', ''))
            action.setIcon(icon)
            self._configs_group.addAction(action)
            action.setChecked(config['name'] == active)
            index = self._configs_combo_box.count()
            self._configs_combo_box.addItem(config['name'])
            self._configs_combo_box.setItemData(index, action)
            self._configs_combo_box.setItemIcon(index, icon)
        self._configs_combo_box.adjustSize()
        self._mnu_configs.setEnabled(True)
        if self._configs_group.checkedAction() is None:
            actions = self._configs_group.actions()
            if len(actions):
                actions[0].setChecked(True)
            else:
                self._mnu_configs.setEnabled(False)
        for i in range(self._configs_combo_box.count()):
            if self._configs_combo_box.itemData(i) == \
                    self._configs_group.checkedAction():
                self._configs_combo_box.setCurrentIndex(i)
        enabled = self.get_active_config() is not None
        self.config_refreshed.emit(enabled)
        self._action_run.setEnabled(enabled)
        self._loading_configs = False

    def _setup_menu(self):
        name = self.interpreter_manager.name.capitalize()
        name = name[0] + '&' + name[1:]
        self._mnu = window.get_menu(name)
        self._action_run = self._mnu.addAction('Run')
        window.get_main_window().addAction(self._action_run)
        self._action_run.triggered.connect(self.run)
        self._action_run.setShortcut(shortcuts.get('Run', 'F9'))
        self._action_run.setIcon(special_icons.run_icon())
        self._action_configure = self._mnu.addAction('Configure')
        self._action_configure.setMenuRole(self._action_configure.NoRole)
        self._action_configure.triggered.connect(self.configure)
        window.get_main_window().addAction(self._action_configure)
        self._action_configure.setIcon(special_icons.configure_icon())
        self._separator = self._mnu.addSeparator()

    def apply_preferences(self):
        self._action_run.setShortcut(shortcuts.get('Run', 'F9'))

    def _setup_combo_box(self):
        # add a combo box to choose the run configuration to use
        # in project mode.
        self._mnu_configs = QtWidgets.QMenu('Configurations', self._mnu)
        self._mnu.insertMenu(self._separator, self._mnu_configs)
        self._mnu_configs.menuAction().setMenuRole(QtWidgets.QAction.NoRole)
        self._configs_group = QtWidgets.QActionGroup(self._mnu_configs)
        self._configs_group.triggered.connect(
            self._on_config_action_triggered)
        self._configs_combo_box = QtWidgets.QComboBox()
        self._configs_combo_box.currentIndexChanged.connect(
            self._on_current_config_changed)
        self._configs_combo_box.setSizeAdjustPolicy(
            self._configs_combo_box.AdjustToContents)
        self.refresh()
        self._mnu_configs.setEnabled(len(self._mnu_configs.actions()) != 0)

    def _setup_toolbar(self):
        name = self.interpreter_manager.name
        toolbar = window.get_toolbar('%sToolBar' % name,
                                     '%sToolBar' % name.capitalize())
        self._configs_combo_box.show()
        toolbar.addWidget(self._configs_combo_box)
        toolbar.addAction(self._action_configure)
        toolbar.addAction(self._action_run)

    def _on_config_action_triggered(self, action):
        if self._loading_configs:
            return
        name = action.text().replace('&', '')
        # save active config in the root project settings
        save_active_config(project.get_projects()[0], name)
        for i in range(self._configs_combo_box.count()):
            a = self._configs_combo_box.itemData(i)
            if a == action:
                self._configs_combo_box.setCurrentIndex(i)
                break

    def _on_open_file_requested(self, path, line):
        # open file from traceback
        editor.open_file(path, line=line)

    def _create_dock(self):
        self._run_widget = widgets.RunWidget(self._window)
        self._dock_run = window.add_dock_widget(
            self._run_widget, 'Run', special_icons.run_icon(),
            QtCore.Qt.BottomDockWidgetArea)
        self._run_widget.last_tab_closed.connect(self._remove_dock)

    def _remove_dock(self):
        window.remove_dock_widget(self._dock_run)
        self._dock_run = None
        self._run_widget = None

    def _on_current_config_changed(self, index):
        if self._loading_configs:
            return
        action = self._configs_combo_box.itemData(index)
        action.setChecked(True)
        self._on_config_action_triggered(action)


class _DlgScriptRunConfiguration(QtWidgets.QDialog):
    """
    This dialog let the users configure how they want their script to be run.
    """
    @classmethod
    def edit_configurations(cls, window, interpreter_manager,
                            active_config_name):
        """
        Edits the list of configuration for the given project/file.
        :param window: Project window instance
        :param interpreter_manager: the interpreter manager used by the dialog
                (:class:`hackedit.api.interpreters.InterpreterManager`).
        :return: The updated list of configurations.
        """
        dlg = cls(window, interpreter_manager, active_config_name)
        ret_val = None
        if dlg.exec_() == dlg.Accepted:
            dlg._update_current_config()
            for path in dlg._configs.keys():
                save_configs(path, dlg._configs[path])
            if dlg._current_config:
                # save active config in current project
                save_active_config(
                    window.projects[0], dlg._current_config['name'])

        return ret_val

    def __init__(self, window, interpreter_manager, active_config_name):
        super().__init__(window)
        self.interpreter_manager = interpreter_manager
        self._active_config_name = active_config_name
        self._window = window
        self._current_project = None
        self._current_config = None
        self._configs = {}
        self._setup_ui()
        self._load_interpreters()
        self._load_configs()
        self._connect_slots()
        for path in self._configs.keys():
            for i, cfg in enumerate(self._configs[path]):
                if cfg['name'] == self._active_config_name:
                    self._show_project_configs(path)
                    self._on_config_changed(i)
        if self._current_project is None:
            self._current_project = window.current_project

    def _update_prj_interpreter(self, index):
        self.interpreter_manager.set_project_interpreter(
            self._current_project,
            self._ui.combo_prj_interpreter.itemText(index))

    def _connect_slots(self):
        self._ui.bt_add_env_var.clicked.connect(self._add_row)
        self._ui.table_env_vars.currentCellChanged.connect(
            self._table_env_var_sel_changed)
        self._ui.bt_rm_env_var.clicked.connect(self._rm_current_row)
        self._ui.edit_name.textChanged.connect(self._update_name_in_list)
        self._ui.bt_add_cfg.clicked.connect(self._add_cfg)
        self._ui.bt_rm_cfg.clicked.connect(self._rm_cfg)
        self._ui.bt_pick_script.clicked.connect(self._pick_script)
        self._ui.bt_pick_working_dir.clicked.connect(self._pick_working_dir)
        self._ui.list_configs.currentRowChanged.connect(
            self._on_config_changed)
        self._ui.cb_project.currentTextChanged.connect(
            self._show_project_configs)
        self._ui.combo_prj_interpreter.currentIndexChanged.connect(
            self._update_prj_interpreter)

    def _setup_ui(self):
        self._ui = dlg_script_run_config_ui.Ui_Dialog()
        self._ui.setupUi(self)
        self.setWindowTitle('Setup project run configurations')

    def _show_project_configs(self, path):
        if self._current_project:
            self._update_current_config()
        self._ui.list_configs.clear()
        self._current_project = path
        active = get_active_config_name(path, self._configs[path])
        # find active config row
        active_row = 0
        for i, cfg in enumerate(self._configs[path]):
            icon = widgets.FileIconProvider().icon(
                self.interpreter_manager.extensions[0].replace('*', ''))
            self._ui.list_configs.addItem(cfg['name'])
            self._ui.list_configs.item(i).setIcon(icon)
            if cfg['name'] == active:
                active_row = i
        if len(self._configs[path]):
            self._ui.list_configs.setCurrentRow(active_row)
            self._ui.group_settings.setDisabled(False)
        else:
            # empty list of configs, cannot edit settings -> disable
            self._ui.group_settings.setDisabled(True)
        self._ui.combo_prj_interpreter.setCurrentText(
            self.interpreter_manager.get_project_interpreter(
                self._current_project))

    def _load_interpreters(self):
        for i, interpreter in enumerate(
                self.interpreter_manager.all_interpreters):
            self._ui.combo_prj_interpreter.addItem(interpreter)
            self._ui.combo_prj_interpreter.setItemIcon(
                i, self.interpreter_manager.get_interpreter_icon())
        combo = self._ui.combo_prj_interpreter
        interpreter = self.interpreter_manager.get_project_interpreter(
            project.get_current_project())
        combo.setCurrentText(interpreter)

    def _load_configs(self):
        # load configs of each project
        current_index = 0
        for i, npath in enumerate(project.get_projects()):
            self._ui.cb_project.addItem(npath)
            self._ui.cb_project.setItemIcon(
                i, QtGui.QIcon.fromTheme('folder'))
            self._configs[npath] = load_configs(npath)
            for cfg in self._configs[npath]:
                if cfg['name'] == self._active_config_name:
                    current_index = self._ui.cb_project.count() - 1
        self._ui.cb_project.setCurrentIndex(current_index)

    def _rm_current_row(self):
        self._ui.table_env_vars.removeRow(self._ui.table_env_vars.currentRow())

    def _table_env_var_sel_changed(self, current_row, _, prev_row, *args):
        if current_row != prev_row:
            self._ui.bt_rm_env_var.setEnabled(current_row != -1)

    def _add_row(self):
        self._ui.table_env_vars.insertRow(
            self._ui.table_env_vars.rowCount())

    def _get_env_vars(self):
        env_vars = {}
        for i in range(self._ui.table_env_vars.rowCount()):
            name_item = self._ui.table_env_vars.item(i, 0)
            val_item = self._ui.table_env_vars.item(i, 1)
            if name_item and val_item:
                env_vars[name_item.text()] = val_item.text()
        return env_vars

    def _on_config_changed(self, row):
        self._change_config(self._configs[self._current_project][row])

    def _update_name_in_list(self, new_name):
        for i in range(self._ui.list_configs.count()):
            if self._ui.list_configs.item(i).text() == \
                    self._current_config['name']:
                self._current_config['name'] = new_name
                self._ui.list_configs.item(i).setText(new_name)

    def _rm_cfg(self):
        cfg = self._current_config
        self._current_config = None
        for i in range(self._ui.list_configs.count()):
            if self._ui.list_configs.item(i).text() == cfg['name']:
                self._ui.list_configs.takeItem(i)
                break
        try:
            self._configs[self._current_project].remove(cfg)
        except ValueError:
            pass
        self._ui.group_settings.setDisabled(
            len(self._configs[self._current_project]) == 0)

    def _add_cfg(self):
        cpt = 0
        for config in self._configs[self._current_project]:
            if 'Unnamed' in config['name']:
                cpt += 1
        config = create_default_config(self._current_project)
        if cpt:
            config['name'] = 'Unnamed (%d)' % cpt
        self._ui.list_configs.addItem(config['name'])
        self._configs[self._current_project].append(config)
        self._change_config(config)
        self._ui.group_settings.setDisabled(len(
            self._configs[self._current_project]) == 0)

    def _pick_script(self):
        current_path = self._current_project
        folder = self._ui.edit_script.text()
        if not folder or not os.path.exists(folder):
            folder = current_path
        path, ffilter = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Choose %s script' % self.interpreter_manager.name,
            folder, '%s files (%s)' % (
                self.interpreter_manager.name.capitalize(),
                ' '.join(self.interpreter_manager.extensions)))
        if path:
            self._ui.edit_script.setText(os.path.normpath(path))
            self._ui.edit_name.setText(QtCore.QFileInfo(path).baseName())
            self._ui.edit_working_dir.setText(os.path.dirname(path))

    def _pick_working_dir(self):
        current_path = self._current_project
        folder = self._ui.edit_script.text()
        if not folder or not os.path.exists(folder):
            folder = current_path
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Choose the working directory', folder)
        if path:
            self._ui.edit_working_dir.setText(os.path.normpath(path))

    def _display_config(self, config):
        self._ui.edit_name.setText(config['name'])
        self._ui.edit_intepreter_options.setText(' '.join(
            config['interpreter_options']))
        if config['script']:
            self._ui.edit_script.setText(config['script'])
        else:
            self._ui.edit_script.setText('')
        self._ui.edit_script_args.setText(
            ' '.join(config['script_parameters']))
        if config['working_dir']:
            self._ui.edit_working_dir.setText(config['working_dir'])
        else:
            self._ui.edit_working_dir.setText('')

        # interpreter combo box
        combo = self._ui.combo_prj_interpreter
        interpreter = self.interpreter_manager.get_project_interpreter(
            self._current_project)
        combo.blockSignals(True)
        combo.setCurrentText(interpreter)
        combo.blockSignals(False)

        # environment variables
        self._ui.table_env_vars.clear()
        self._ui.table_env_vars.setHorizontalHeaderLabels(['Name', 'Value'])
        self._ui.table_env_vars.setRowCount(0)
        for key, value in config['environment'].items():
            index = self._ui.table_env_vars.rowCount()
            self._ui.table_env_vars.insertRow(index)
            self._ui.table_env_vars.setItem(
                index, 0, QtWidgets.QTableWidgetItem(key))
            self._ui.table_env_vars.setItem(
                index, 1, QtWidgets.QTableWidgetItem(value))

        try:
            checked = config['run_in_external_terminal']
        except KeyError:
            checked = False
        finally:
            self._ui.cb_run_in_external_terminal.setChecked(checked)

        # select active config in list
        for i in range(self._ui.list_configs.count()):
            self._ui.list_configs.clearSelection()
            if self._ui.list_configs.item(i).text() == config['name']:
                self._ui.list_configs.item(i).setSelected(True)
                break

    def _change_config(self, config):
        if self._current_config is not None:
            self._update_current_config()
        self._current_config = config
        self._display_config(config)

    def _update_current_config(self):
        if self._current_config is None:
            # no config added yet
            return
        self._current_config['name'] = self._ui.edit_name.text()
        opts = self._ui.edit_intepreter_options.text().strip()
        if not opts:
            opts = []
        else:
            opts = shlex.split(opts, posix=False)
        self._current_config['interpreter_options'] = opts
        self._current_config['script'] = self._ui.edit_script.text()
        args = self._ui.edit_script_args.text().strip()
        if not args:
            args = []
        else:
            args = shlex.split(args, posix=False)
        self._current_config['script_parameters'] = args
        self._current_config['working_dir'] = self._ui.edit_working_dir.text()
        self._current_config['environment'] = self._get_env_vars()
        self._current_config['run_in_external_terminal'] = \
            self._ui.cb_run_in_external_terminal.isChecked()


def get_active_config_name(path, configs):
    """
    Loads the active configuration name for a given path.

    :param path: Project path
    :param configs: The list of available configs.

    :return: Name of the active config (should be in ``configs``)
    """
    data = project.load_user_config(path)
    try:
        return data['run_config']
    except KeyError:
        try:
            return configs[0]['name']
        except IndexError:
            return None


def save_active_config(path, config_name):
    """
    Saves the active project configuration to a file.

    :param path: Project path
    :param config_name: Name of the active config.
    """
    data = project.load_user_config(path)
    data['run_config'] = config_name
    project.save_user_config(path, data)


def load_configs(path):
    """
    Loads the list of project configurations.

    :param path: Project path
    :return: The list of project configurations.
    """
    # add a menu with the existing configurations.
    base_path = path
    path = os.path.join(base_path, project.FOLDER, 'run.json')
    try:
        with open(path) as f:
            configs = json.load(f)
    except OSError:
        configs = []
    else:
        configs = sorted(configs, key=lambda cfg: cfg['name'])
        for cfg in configs:
            cfg['script'] = os.path.abspath(
                os.path.join(base_path, cfg['script']))
            cfg['working_dir'] = os.path.abspath(
                os.path.join(base_path, cfg['working_dir']))
    return configs


def save_configs(path, configs):
    """
    Saves the list of project configurations to json.

    :param path: Project path
    :param configs: The list of configs to save.
    """
    base_path = path
    # normalise paths; relative paths will work cross-platform
    try:
        for cfg in configs:
            cfg['script'] = os.path.relpath(cfg['script'], base_path)
            cfg['working_dir'] = os.path.relpath(cfg['working_dir'], base_path)
    except ValueError:
        # invalid config
        pass
    path = os.path.join(base_path, project.FOLDER, 'run.json')
    with open(path, 'w') as f:
        json.dump(configs, f, indent=4, sort_keys=True)


def create_default_config(path):
    """
    Creates a default configuration for the given path.
    :param path: Path for which the default config must be created.
    :return: the default config.
    """
    if os.path.isfile(path):
        return {
                'name': QtCore.QFileInfo(path).baseName(),
                'script': path,
                'script_parameters': [],
                'working_dir': os.path.dirname(path),
                'interpreter_options': [],
                'environment': {}
        }
    else:
        return {
            'name': 'Unnamed',
            'script': '',
            'script_parameters': [],
            'working_dir': path,
            'interpreter_options': [],
            'environment': {}
        }
