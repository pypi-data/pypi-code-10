"""
This plugin show the project contents in a tree view.
"""
import logging
import mimetypes
import os
import shlex
import subprocess
import time
import webbrowser
from fnmatch import fnmatch

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqode.core.api import DelayJobRunner, TextHelper
from pyqode.core.widgets import FileSystemTreeView, FileSystemContextMenu, \
    FileSystemHelper

from hackedit import api
from hackedit.api import plugins, shortcuts, utils
from hackedit.api.project import load_user_config, save_user_config
from hackedit.api.widgets import FileIconProvider
from hackedit.app import settings, boss_wrapper as boss, common
from hackedit.app.dialogs.dlg_ignore import DlgIgnore
from hackedit.app.widgets.locator import LocatorWidget
from hackedit.app.workspaces import WorkspaceManager


try:
    # new scandir function in python 3.5
    from os import scandir as listdir
except ImportError:
    try:
        # new scandir function from scandir package on pypi
        from scandir import scandir as listdir
    except ImportError:
        # scandir package not found, use the slow listdir function
        from os import listdir


def _logger():
    return logging.getLogger(__name__)


def ignore_path(path, ignore_patterns=None):
    """
    Utility function that checks if a given path should be ignored.

    A path is ignored if it matches one of the ignored_patterns.

    :param path: the path to check
    :param ignore_patterns: The ignore patters to respect.
        If none, :func:hackedit.api.settings.ignore_patterns() is used instead.
    :returns: True if the path is in an directory that must be ignored
        or if the file name matches an ignore pattern, otherwise False.
    """
    if ignore_patterns is None:
        ignore_patterns = utils.get_ignored_patterns()

    def ignore(name):
        for ptrn in ignore_patterns:
            if fnmatch(name, ptrn):
                return True

    for part in os.path.normpath(path).split(os.path.sep):
        if part and ignore(part):
            return True
    return False


def scandir(directory, ignore_patterns):
    files = []
    print('scanning directory: %s' % directory)
    join = os.path.join
    isfile = os.path.isfile
    isdir = os.path.isdir
    append = files.append
    for path in listdir(directory):
        try:
            path = path.name
        except AttributeError:
            pass
        full_path = join(directory, path)
        ignored = ignore_path(full_path, ignore_patterns)
        if not ignored:
            if isfile(full_path):
                append(full_path)
            elif isdir(full_path):
                try:
                    files += scandir(full_path, ignore_patterns)
                except PermissionError:
                    pass
            time.sleep(0)
    return files


def scan_project_directories(_, directories, ignore_patterns):
    files = []
    for directory in directories:
        try:
            files += scandir(directory, ignore_patterns)
        except PermissionError:
            pass
    files = sorted(files)
    return files


class ProjectExplorer(QtCore.QObject):
    """
    Displays project content in a treeview, manage the list of open projects
    and provides the list of project files to other plugins.

    This is a central plugin that all workspace should include!
    """
    project_only = True
    preferred_position = 0

    def __init__(self, window):
        super().__init__()
        self._window = window
        self._locator = LocatorWidget(self._window)
        self._locator.activated.connect(self._on_locator_activated)
        self._locator.cancelled.connect(self._on_locator_cancelled)
        self._widget = QtWidgets.QWidget(self._window)
        self._job_runner = DelayJobRunner()
        self._cached_files = []
        self._task_running = False
        self._widget.installEventFilter(self)
        self._setup_filesystem_treeview()
        self._setup_prj_selector_widget(self._window)
        self._setup_dock_widget()
        self._setup_tab_bar_context_menu(self._window)
        self._setup_locator()
        self._setup_project_menu()
        api.signals.connect_slot(api.signals.CURRENT_EDITOR_CHANGED,
                                 self._on_current_editor_changed)

    def _get_ignored_patterns(self):
        patterns = utils.get_ignored_patterns()
        prj_path = api.project.get_root_project()
        # project specific ignore patterns
        usd = api.project.load_user_config(prj_path)
        try:
            patterns += usd['ignored_patterns']
        except KeyError:
            pass
        return patterns

    def _run_update_projects_model_thread(self):
        if not self._task_running:
            self._task_running = True
            pth = api.project.get_root_project()
            usd = api.project.load_user_cache(pth)
            try:
                files = usd['project_files']
            except KeyError:
                files = []
            if files:
                self._window.project_files = files
            directories = api.project.get_projects()
            api.tasks.start('Indexing project files',
                            scan_project_directories,
                            self._on_file_list_available,
                            args=(directories, self._get_ignored_patterns()),
                            cancellable=False)

    def get_files(self):
        """
        Returns the filtered list of files for all open projects.
        """
        return self._window.project_files

    def close(self):
        # save active project in first open project
        paths = api.project.get_projects()
        data = load_user_config(paths[0])
        data['active_project'] = self._combo_projects.currentData()
        try:
            save_user_config(paths[0], data)
        except PermissionError:
            pass
        self._window = None
        self._locator._window = None
        self._locator = None

    def apply_preferences(self):
        new_patterns = ';'.join(utils.get_ignored_patterns())
        if self._last_ignore_patterns != new_patterns:
            self._last_ignore_patterns = new_patterns
            self._fs.clear_ignore_patterns()
            self._fs.add_ignore_patterns(self._get_ignored_patterns())
            self._fs.set_root_path(api.project.get_current_project())
        self._run_update_projects_model_thread()
        self._fs.context_menu.update_show_in_explorer_action()
        self._tab_bar_action_show_in_explorer.setText(
            'Show in %s' % FileSystemContextMenu.get_file_explorer_name())
        self._update_workspaces_menu()
        self.action_goto_anything.setShortcut(shortcuts.get(
            'Goto anything', 'Ctrl+P'))
        self.action_goto_symbol.setShortcut(shortcuts.get(
            'Goto symbol', 'Ctrl+R'))
        self.action_goto_symbol_in_project.setShortcut(shortcuts.get(
            'Goto symbol in project', 'Ctrl+Shift+R'))
        self.action_goto_line.setShortcut(shortcuts.get(
            'Goto line', 'Ctrl+G'))

    def _on_file_list_available(self, files):
        if files is None:
            return
        self._task_running = False
        if files != self._cached_files:
            self._window.project_files = files
            self._window.project_files_available.emit(
                api.project.get_project_files())
            self._cached_files = files
            pth = api.project.get_root_project()
            cache = api.project.load_user_cache(pth)
            cache['project_files'] = files
            api.project.save_user_cache(pth, cache)
            _logger().debug('project model updated')

    def _setup_tab_bar_context_menu(self, window):
        text = 'Show in %s' % FileSystemContextMenu.get_file_explorer_name()
        action = QtWidgets.QAction(text, window)
        action.setToolTip(text)
        action.setIcon(QtGui.QIcon.fromTheme('system-file-manager'))
        action.triggered.connect(self._on_show_in_explorer_triggered)
        api.window.add_tab_widget_context_menu_action(action)
        self._tab_bar_action_show_in_explorer = action

    def _setup_dock_widget(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._widget_active_projects)
        layout.addWidget(self._fs)
        layout.setContentsMargins(3, 3, 3, 3)
        self._widget.setLayout(layout)
        dock = api.window.add_dock_widget(
            self._widget, 'Project', QtGui.QIcon.fromTheme('folder'),
            QtCore.Qt.LeftDockWidgetArea)
        dock.show()

    def _setup_project_menu(self):
        menu = api.window.get_menu('&View')
        self.workspaces_menu = menu.addMenu('Workspace')
        menu.addSeparator()

    def _update_workspaces_menu(self):
        if QtGui.QIcon.hasThemeIcon('preferences-system-windows'):
            icon = QtGui.QIcon.fromTheme('preferences-system-windows')
        else:
            icon = QtGui.QIcon.fromTheme('applications-interfacedesign')
        self.workspaces_menu.clear()
        ag = QtWidgets.QActionGroup(self.workspaces_menu)
        for w in WorkspaceManager().get_names():
            a = QtWidgets.QAction(w, self.workspaces_menu)
            a.setCheckable(True)
            a.setChecked(w == self._window.workspace['name'])
            a.setIcon(icon)
            ag.addAction(a)
            self.workspaces_menu.addAction(a)
        ag.triggered.connect(self._on_workspace_action_clicked)

    @QtCore.pyqtSlot(QtWidgets.QAction)
    def _on_workspace_action_clicked(self, action):
        prj = api.project.get_root_project()
        open_path = self._window._app.open_path
        api.project.save_workspace(prj, action.text().replace('&', ''))
        self._window._save_state(*self._window._get_session_info())
        window = self._window
        open_path(prj, force=True)
        window.close()

    def _setup_locator(self):
        menu = api.window.get_menu('&Goto')
        self.action_goto_anything = menu.addAction('Goto anything...')
        self.action_goto_anything.setShortcut(shortcuts.get(
            'Goto anything', 'Ctrl+P'))
        self._window.addAction(self.action_goto_anything)
        self.action_goto_anything.triggered.connect(self._goto_anything)

        menu.addSeparator()

        self.action_goto_symbol = menu.addAction('Goto symbol...')
        self.action_goto_symbol.setShortcut(shortcuts.get(
            'Goto symbol', 'Ctrl+R'))
        self._window.addAction(self.action_goto_symbol)
        self.action_goto_symbol.triggered.connect(self._goto_symbol)

        self.action_goto_symbol_in_project = menu.addAction(
            'Goto symbol in project...')
        self.action_goto_symbol_in_project.setShortcut(shortcuts.get(
            'Goto symbol in project', 'Ctrl+Shift+R'))
        self._window.addAction(self.action_goto_symbol_in_project)
        self.action_goto_symbol_in_project.triggered.connect(
            self._goto_symbol_in_project)

        menu.addSeparator()

        self.action_goto_line = menu.addAction('Goto line')
        self.action_goto_line.setShortcut(shortcuts.get(
            'Goto line', 'Ctrl+G'))
        self._window.addAction(self.action_goto_line)
        self.action_goto_line.triggered.connect(self._goto_line)

    def _goto_anything(self):
        self._locator.mode = self._locator.MODE_GOTO_ANYTHING
        self._show_locator()

    def _goto_symbol(self):
        self._cached_cursor_position = TextHelper(
            api.editor.get_current_editor()).cursor_position()
        self._locator.mode = self._locator.MODE_GOTO_SYMBOL
        self._show_locator()

    def _goto_symbol_in_project(self):
        self._locator.mode = self._locator.MODE_GOTO_SYMBOL_IN_PROJECT
        self._show_locator()

    def _goto_line(self):
        self._cached_cursor_position = TextHelper(
            api.editor.get_current_editor()).cursor_position()
        self._locator.mode = self._locator.MODE_GOTO_LINE
        self._show_locator()

    def _show_locator(self):
        widget = api.editor.get_current_editor()
        if widget is None:
            widget = self._window._ui.stackedWidget
        parent_pos = widget.pos()
        parent_size = widget.size()
        w = parent_size.width() * 0.8
        self._locator.setMinimumWidth(parent_size.width() * 0.8)
        x, y = parent_pos.x(), parent_pos.y()
        pw = parent_size.width()
        x += pw / 2 - w / 2
        self._locator.move(widget.mapToGlobal(QtCore.QPoint(x, y)))
        self._locator.show()

    def _setup_prj_selector_widget(self, window):
        self._widget_active_projects = QtWidgets.QWidget(window)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._combo_projects = QtWidgets.QComboBox()
        layout.addWidget(self._combo_projects)
        self.load_project_combo()
        api.signals.connect_slot(api.signals.PROJECT_ADDED,
                                 self._on_path_added)
        api.signals.connect_slot(api.signals.CURRENT_PROJECT_CHANGED,
                                 self._on_current_proj_changed)
        self._set_active_project()
        self._combo_projects.currentIndexChanged.connect(
            self._on_current_index_changed)
        bt_refresh = QtWidgets.QToolButton()
        bt_refresh.setIcon(QtGui.QIcon.fromTheme('view-refresh'))
        bt_refresh.setToolTip('Refresh tree view and run project indexation')
        bt_refresh.clicked.connect(self._refresh)
        layout.addWidget(bt_refresh)

        bt_remove_project = QtWidgets.QToolButton()
        bt_remove_project.setIcon(QtGui.QIcon.fromTheme('list-remove'))
        bt_remove_project.setToolTip('Remove project from view')
        bt_remove_project.clicked.connect(self._remove_current_project)
        layout.addWidget(bt_remove_project)
        self._widget_active_projects.setLayout(layout)
        if self._combo_projects.count() == 1:
            self._widget_active_projects.hide()

    def load_project_combo(self, current_index=None):
        if current_index is None:
            current_index = self._combo_projects.currentIndex()
        project_paths = api.project.get_projects()
        self._combo_projects.blockSignals(True)
        self._combo_projects.clear()
        for pth in project_paths:
            index = self._combo_projects.count()
            if os.path.ismount(pth):
                if api.system.WINDOWS and not pth.endswith('\\'):
                    pth += '\\'
                name = pth
            else:
                name = os.path.split(pth)[1]
            self._combo_projects.addItem(name)
            self._combo_projects.setItemIcon(index, FileIconProvider().icon(
                QtCore.QFileInfo(pth)))
            self._combo_projects.setItemData(index, pth)
        self._combo_projects.blockSignals(False)
        self._combo_projects.setCurrentIndex(current_index)

    def _setup_filesystem_treeview(self):
        self._fs = FileSystemTreeView(self._widget)
        self._fs.setMinimumWidth(200)
        self._last_ignore_patterns = ';'.join(utils.get_ignored_patterns())
        self._fs.add_ignore_patterns(self._get_ignored_patterns())
        self._fs.file_created.connect(self._on_file_created)
        self._fs.file_deleted.connect(self._on_file_deleted)
        self._fs.file_renamed.connect(self._on_file_renamed)
        self._fs.set_icon_provider(FileIconProvider())
        context_menu = FileSystemContextMenu()
        self._fs.set_context_menu(context_menu)
        self.templates_menu = context_menu.menu_new.addSeparator()
        self.templates_menu = context_menu.menu_new.addMenu('Templates')
        self.templates_menu.menuAction().setIcon(QtGui.QIcon.fromTheme(
            'folder-templates'))
        sources = {}
        for src in boss.sources():
            lbl = src['label']
            icon = QtGui.QIcon.fromTheme(
                'folder' if src['is_local'] else 'folder-remote')
            menu = self.templates_menu.addMenu(icon, lbl)
            sources[lbl] = menu
        for lbl, template, meta in boss.file_templates(include_meta=True):
            icon = meta['icon']
            if icon.startswith(':') or os.path.exists(icon):
                icon = QtGui.QIcon(icon)
            elif icon.startswith('file.'):
                icon = FileIconProvider().icon(icon)
            else:
                icon = QtGui.QIcon.fromTheme(icon)
            a = sources[lbl].addAction(icon, meta['name'])
            a.setData((lbl, template))
            a.triggered.connect(self._add_file_from_template)
        for menu in sources.values():
            menu.menuAction().setVisible(len(menu.actions()) > 0)
        self._fs.activated.connect(self._on_file_activated)

        self.action_mark_as_ignored = QtWidgets.QAction(
            'Mark as ignored', self._fs)
        self.action_mark_as_ignored.triggered.connect(
            self._on_mark_as_ignored)
        self.action_mark_as_ignored.setIcon(QtGui.QIcon.fromTheme(
            'emblem-unreadable'))
        self._fs.context_menu.insertAction(
            self._fs.context_menu.action_show_in_explorer,
            self.action_mark_as_ignored)
        self._fs.context_menu.insertSeparator(
            self._fs.context_menu.action_show_in_explorer)

        self.action_show_in_terminal = QtWidgets.QAction(
            QtGui.QIcon.fromTheme('utilities-terminal'), 'Open in terminal',
            self._fs)
        self.action_show_in_terminal.triggered.connect(
            self._on_show_in_terminal_triggered)
        self._fs.context_menu.addAction(self.action_show_in_terminal)

        self.action_open_in_browser = QtWidgets.QAction(
            QtGui.QIcon.fromTheme('applications-internet'),
            'Open in web browser', self._fs)
        self.action_open_in_browser.triggered.connect(
            self._on_action_open_in_browser_triggered)
        self._fs.context_menu.addAction(self.action_open_in_browser)

        self._fs.about_to_show_context_menu.connect(
            self._on_about_to_show_context_menu)

    def _on_mark_as_ignored(self):
        path = FileSystemHelper(self._fs).get_current_path()
        prj = api.project.get_root_project()
        usd = api.project.load_user_config(prj)
        try:
            patterns = usd['ignored_patterns']
        except KeyError:
            patterns = []
        finally:
            name = os.path.split(path)[1]
            pattern = DlgIgnore.get_ignore_pattern(self._window, name)
            if pattern:
                patterns.append(pattern)
                usd['ignored_patterns'] = patterns
                api.project.save_user_config(prj, usd)
                self._fs.clear_ignore_patterns()
                self._fs.add_ignore_patterns(self._get_ignored_patterns())
                # force reload
                self._fs.set_root_path(api.project.get_current_project())
                # update the list of project files, this should trigger an
                # indexation.
                self._run_update_projects_model_thread()
                self._window.indexor.force_stop()

    def _on_about_to_show_context_menu(self, path):
        is_html = mimetypes.guess_type(path)[0] == 'text/html'
        self.action_open_in_browser.setVisible(is_html)

    def _on_action_open_in_browser_triggered(self):
        path = FileSystemHelper(self._fs).get_current_path()
        if settings.use_default_browser():
            webbrowser.open_new_tab(path)
        else:
            cmd = utils.get_custom_browser_command() % path
            subprocess.Popen(cmd)

    def _on_show_in_terminal_triggered(self):
        path = FileSystemHelper(self._fs).get_current_path()
        if os.path.isfile(path):
            path = os.path.dirname(path)
        cmd = utils.get_cmd_open_folder_in_terminal() % path
        if api.system.WINDOWS:
            subprocess.Popen(cmd,
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(shlex.split(cmd, posix=False))

    def _add_file_from_template(self):
        source, template = self.sender().data()
        path = FileSystemHelper(self._fs).get_current_path()
        if os.path.isfile(path):
            path = os.path.dirname(path)
        common.create_new_from_template(source, template, path, True,
                                        self._window, self._window._app)

    def _on_show_in_explorer_triggered(self):
        path = api.window.get_tab_under_context_menu().file.path
        FileSystemContextMenu.show_in_explorer(
            path, api.window.get_main_window())

    def _on_file_activated(self, index):
        path = self._fs.filePath(index)
        if path and os.path.isfile(path):
            _logger().debug('showing editor for %r', path)
            api.editor.open_file(path)

    def _on_current_editor_changed(self, tab):
        if tab is not None:
            self._fs.select_path(tab.file.path)
        self.action_goto_line.setEnabled(tab is not None)
        self.action_goto_symbol.setEnabled(tab is not None)

    def _on_current_proj_changed(self, new_path):
        if api.project.get_current_project() != new_path:
            self._window._current_folder = new_path
            self._fs.set_root_path(new_path)

    def _set_active_project(self):
        paths = api.project.get_projects()
        try:
            data = load_user_config(paths[0])
        except IndexError:
            return
        try:
            active_path = data['active_project']
            if active_path is None:
                raise KeyError('active_project')
        except KeyError:
            active_path = paths[0]
        for i in range(self._combo_projects.count()):
            if self._combo_projects.itemData(i) == active_path:
                self._combo_projects.setCurrentIndex(i)
                self._fs.set_root_path(active_path)
                break
        else:
            self._fs.set_root_path(active_path)
        self._window._current_folder = active_path

    def _on_path_added(self, path):
        if os.path.isfile(path):
            return
        index = self._combo_projects.count()
        self.load_project_combo(current_index=index)
        self._on_current_index_changed(index)
        self._widget_active_projects.setVisible(
            self._combo_projects.count() > 1)
        data = load_user_config(api.project.get_projects()[0])
        data['active_project'] = path
        self._run_update_projects_model_thread()

    def _on_current_index_changed(self, index):
        new_path = self._combo_projects.itemData(index)
        if new_path:
            self._window.current_project_changed.emit(new_path)

    def _refresh(self):
        self._fs.set_root_path('/')
        self._fs.set_root_path(api.project.get_current_project())
        self._run_update_projects_model_thread()

    def _remove_current_project(self):
        path = self._combo_projects.itemData(
            self._combo_projects.currentIndex())
        self._combo_projects.removeItem(self._combo_projects.currentIndex())
        self._window._folders.remove(path)
        initial_path = api.project.get_projects()[0]
        data = load_user_config(initial_path)
        try:
            linked_paths = data['linked_paths']
        except KeyError:
            linked_paths = []
        try:
            linked_paths.remove(path)
        except ValueError:
            pass
        finally:
            data['linked_paths'] = linked_paths
            save_user_config(initial_path, data)
            self._run_update_projects_model_thread()

    def _on_file_created(self, path):
        api.editor.open_file(path)
        self._run_update_projects_model_thread()

    def _on_file_renamed(self, old_path, new_path):
        self._window.tab_widget.rename_document(old_path, new_path)
        self._run_update_projects_model_thread()

    def _on_file_deleted(self, path):
        self._window.tab_widget.close_document(path)
        self._job_runner.request_job(self._run_update_projects_model_thread)

    def _on_locator_activated(self, path, line):
        if line == -1:
            line = None
        else:
            line = line - 1  # 0 based
        api.editor.open_file(path, line=line)

    def _on_locator_cancelled(self):
        if self._locator.mode in [
                self._locator.MODE_GOTO_LINE, self._locator.MODE_GOTO_SYMBOL]:
            line, col = self._cached_cursor_position
            TextHelper(api.editor.get_current_editor()).goto_line(line, col)
