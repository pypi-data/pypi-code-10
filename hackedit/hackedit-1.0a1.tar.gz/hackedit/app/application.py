"""
This module contains the Application class.
"""
import logging
import os
import sys
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqode.core.widgets import RecentFilesManager, FileSystemContextMenu
from qdarkstyle import load_stylesheet_pyqt5

from hackedit import api
from hackedit.api import system, shortcuts, _shared
from hackedit.api.project import load_user_config, load_workspace, \
    save_workspace
from hackedit.app import common, environ, mime_types, icons, boss_wrapper, \
    settings
from hackedit.app.dialogs.open_path import DlgOpen
from hackedit.app.dialogs.workspace import DlgSelectWorkspace
from hackedit.app.main_window import MainWindow
from hackedit.app.plugin_manager import PluginManager
from hackedit.app.welcome_window import WelcomeWindow
from hackedit.app.workspaces import WorkspaceManager


def _logger():
    return logging.getLogger(__name__)


class Application(QtCore.QObject):
    """
    Runs the QApplication and manages the list of editor windows.
    """

    #: signal emitted when an unhandled exception occurred (for internal use)
    _report_exception_requested = QtCore.pyqtSignal(object, str)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------
    @property
    def window_count(self):
        return len(self._editor_windows)

    def __init__(self, qapp, splash, args):
        def show_msg_on_splash(msg):
            if msg:
                _logger().info(msg)
                if splash is not None:
                    splash.showMessage(
                        msg, QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter,
                        QtCore.Qt.white)
                    qapp.processEvents()
        self._args = args
        self._qapp = qapp
        self._splash = splash
        super().__init__()
        _shared._APP = self
        environ.apply()
        shortcuts.load()
        show_msg_on_splash('Setting up log file...')
        show_msg_on_splash('Setting up except hook...')
        self._report_exception_requested.connect(self._report_exception)
        self._old_except_hook = sys.excepthook
        sys.excepthook = self._except_hook
        self._editor_windows = []

        show_msg_on_splash('Loading fonts...')
        QtGui.QFontDatabase.addApplicationFont(
            ':/fonts/Hack-Bold.ttf')
        QtGui.QFontDatabase.addApplicationFont(
            ':/fonts/Hack-BoldItalic.ttf')
        QtGui.QFontDatabase.addApplicationFont(
            ':/fonts/Hack-Italic.ttf')
        QtGui.QFontDatabase.addApplicationFont(
            ':/fonts/Hack-Regular.ttf')

        show_msg_on_splash('Setting up mimetypes...')
        mime_types.load()

        show_msg_on_splash('Setting up user interface...')
        self._qapp.setWindowIcon(QtGui.QIcon(':/icons/hackedit_128.png'))
        self._qapp.lastWindowClosed.connect(self.quit)
        self._qapp.focusWindowChanged.connect(self._on_current_window_changed)
        self._setup_tray_icon()
        self.apply_preferences()

        show_msg_on_splash('Loading plugins...')
        self.plugin_manager = PluginManager()

        show_msg_on_splash('Setting up templates...')
        self.setup_templates()

        show_msg_on_splash('Loading recent files...')
        self._recents = RecentFilesManager(
            qapp.organizationName(), qapp.applicationName())

        show_msg_on_splash('Setting up welcome window...')
        self._welcome_window = WelcomeWindow(self)

        show_msg_on_splash('')

    def setup_templates(self):
        force_sync = False
        for template_provider in self.plugin_manager.template_providers:
            try:
                url = template_provider.get_remote_url()
                label = template_provider.get_label()
            except TypeError:
                pass
            else:
                if url and label:
                    exists = False
                    sources = boss_wrapper.sources()
                    if not sources:
                        exists = False
                    else:
                        for src in sources:
                            if src['label'] == label:
                                exists = True
                    if not exists:
                        boss_wrapper.add_source(label, url)
                        force_sync = True

        if (force_sync or settings.auto_sync_templates() or
                not settings.has_sync_templates_once()):
            try:
                boss_wrapper.sync()
            except Exception:
                pass
            else:
                settings.set_has_sync_templates_once(True)

    def check_for_update(self):
        common.check_for_update(
            self._qapp.activeWindow(), show_up_to_date_msg=False)

    def restart(self):
        """
        Restarts the IDE.
        """
        QtCore.QProcess.startDetached(sys.executable, sys.argv)
        self.quit(force=True)

    def open_path(self, path, sender=None, force=False):
        """
        Open a new window with `path`.

        :param path: folder or file to open
        """
        path = os.path.normpath(path.strip())
        if path.endswith(('/', '\\')):
            path = path[:-1]
        ret = self._open(path, sender, force)
        shortcuts.save()
        return ret

    def get_recent_files_manager(self):
        """
        Gets the recent files manager
        """
        return self._recents

    def get_open_windows(self):
        """
        Gets the list of open windows.
        """
        ret_val = []
        for w in self._editor_windows:
            ret_val.append(w)
        return ret_val

    def quit(self, force=False):
        """
        Quits the application.

        :param force: True to force exit, bypassing the exit question.
        """
        self._qapp.closeAllWindows()
        if not self.window_count:
            self.tray_icon.hide()
            self._qapp.exit(0)

    def set_active_window(self, window):
        """
        Sets `window` as the active window.

        :param window: Window to activate.
        """
        self._set_active_window(window)

    def get_workspaces(self):
        """
        Returns the list of available workspaces names.

        :return: list of str
        """
        WorkspaceManager().get_names()

    def run(self):
        """
        Runs the application'main loop.
        """
        if self._splash is not None:
            self._splash.close()
            self._splash = None
            delattr(self, '_splash')

        _logger().debug('running')
        nb_window = 0
        for path in self._args.paths:
            if self.open_path(path):
                nb_window += 1
        if settings.restore_last_window():
            try:
                path = self.get_recent_files_manager().get_recent_files()[0]
            except IndexError:
                pass
            else:
                if self.open_path(path):
                    nb_window += 1
        if nb_window == 0:
            self._welcome_window.show()
        if self._args.autoquit:
            QtCore.QTimer.singleShot(5000, self.quit)
        if settings.automatically_check_for_updates():
            QtCore.QTimer.singleShot(2000, self.check_for_update)
        self._qapp.exec_()

    def apply_preferences(self):
        """
        Apply preferences on all open windows
        """
        if settings.dark_theme():
            self._qapp.setStyleSheet(load_stylesheet_pyqt5())
        else:
            self._qapp.setStyleSheet('')
        try:
            if self._args.dev:
                self._qapp.setStyleSheet(
                    self._qapp.styleSheet() +
                    '\nQToolBar{background-color: #80AA80;color: white;}')
        except AttributeError:
            pass
        self.tray_icon.setVisible(settings.show_tray_icon())
        mime_types.load()
        icons.init()
        FileSystemContextMenu.set_file_explorer_command(
            settings.file_manager_cmd())
        for w in self._editor_windows:
            w.apply_preferences()

    # -------------------------------------------------------------------------
    # Private API (+ overridden methods)
    # -------------------------------------------------------------------------
    def _setup_tray_icon(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self._qapp)
        self.tray_icon.setIcon(self._qapp.windowIcon())
        self.tray_icon.messageClicked.connect(self._restore_last_msg_window)
        self.tray_icon.activated.connect(self._restore_last_active_window)
        tray_icon_menu = QtWidgets.QMenu(None)
        self.tray_icon_menu_windows = tray_icon_menu.addMenu('Restore window')
        self.tray_icon_menu_windows.setEnabled(False)
        self.tray_icon_menu_windows.setIcon(QtGui.QIcon.fromTheme(
            'view-restore'))
        tray_icon_menu.addSeparator()
        if not system.PLASMA_DESKTOP:
            # plasma desktop already adds a "quit" action automatically
            action = tray_icon_menu.addAction('Quit')
            action.setIcon(QtGui.QIcon.fromTheme('application-exit'))
            action.triggered.connect(self.quit)
        self.tray_icon.setContextMenu(tray_icon_menu)

    def _on_current_window_changed(self, _):
        w = self._qapp.activeWindow()
        if isinstance(w, MainWindow):
            self._last_window = w

    def _restore_last_msg_window(self):
        try:
            api.window.restore(self.tray_icon.last_window)
        except AttributeError:
            self._restore_last_active_window()

    def _restore_last_active_window(self):
        api.window.restore(self._last_window)

    def _setup_workspace_plugins(self, win, workspace):
        self.plugin_manager.load_workspace_plugins(win=win)
        _logger().debug('setting up workspace plugins: %r -> %r',
                        workspace, win)
        win.workspace = workspace
        for plugin in workspace['plugins']:
            _logger().debug(
                    'adding plugin to window: %r -> %r', plugin, win)
            try:
                plugin_class = self.plugin_manager.workspace_plugins[plugin]
                plugin = plugin_class(win)
                plugin.activate()
            except Exception as e:
                _logger().exception('Plugin activattion failed')
                event = api.events.ExceptionEvent(
                    '%r plugin activation failed' % plugin,
                    'Failed to active plugin: %r. '
                    'Either the plugin is missing or the plugin failed to '
                    'load...' % plugin, e)
                event.level = api.events.WARNING
                win.notifications.add(event, force_show=True)
            else:
                _logger().debug(
                    'plugin added to window: %r -> %r', plugin, win)
                win.plugins.append(plugin)

    def _update_windows(self):
        for w in self._editor_windows:
            w.update_title()
        enable = len(self._editor_windows) > 0
        self.tray_icon_menu_windows.setEnabled(enable)
        self.tray_icon_menu_windows.clear()
        for w in self._editor_windows:
            w.update_mnu_view()
            w.update_mnu_recents()
            title = ' + '.join([os.path.split(p)[1] for p in w.projects])
            a = self.tray_icon_menu_windows.addAction(title)
            a.triggered.connect(self._restore_window_from_tray)

    def _restore_window_from_tray(self):
        action = self.sender()
        for w in self._editor_windows:
            title = ' + '.join([os.path.split(p)[1] for p in w.projects])
            if title == action.text():
                api.window.restore(w)
                break

    def _has_multiple_projects(self, path):
        data = load_user_config(path)
        try:
            return len(data['linked_paths'])
        except KeyError:
            return False

    def _open(self, path, sender, force):
        _logger().info('opening path: %s', path)
        if os.path.isfile(path):
            # open a new window on parent directory and open file in a new tab
            tab_to_open = path
            # todo find project root dir, fallback to dirname if not root
            # project dir could be found
            path = os.path.dirname(path)
            _logger().info('file project root dir: %s', path)
        else:
            tab_to_open = None

        # check if the path is not already open in an existing window
        window = None
        if not force:
            for w in self._editor_windows:
                if path in w.projects:
                    # already open
                    window = w
                    self._set_active_window(w)
                    if tab_to_open:
                        w.open_file(tab_to_open)
                    break

        if window is None:
            if sender is None or self._has_multiple_projects(path):
                # from homepage or when project has multiple projects
                open_mode = settings.OpenMode.NewWindow
            else:
                open_mode = self._ask_open_mode(path)
                if open_mode is None:
                    # user canceled dialog
                    return False

            # open folder in new/current window
            if open_mode == settings.OpenMode.NewWindow:
                workspace = load_workspace(path)
                if workspace is None:
                    # ask the user to choose a workspace
                    workspace = self._ask_for_workspace()
                    if workspace is None:
                        # dialog canceled by user, cancel the whole operation
                        self._qapp.restoreOverrideCursor()
                        return False
                self._welcome_window.setEnabled(False)
                self._qapp.setOverrideCursor(QtCore.Qt.WaitCursor)
                self._qapp.processEvents()
                # Open in new window
                window = self._add_new_window(path, workspace)
                # remember workspace for next open
                window._workspace = workspace
                # save workspace
                save_workspace(path, workspace['name'])
            else:
                self._welcome_window.setEnabled(False)
                self._qapp.setOverrideCursor(QtCore.Qt.WaitCursor)
                self._qapp.processEvents()
                window = sender
                _logger().debug('opening project in existing window: %r',
                                window)
                window.open_folder(path)

        _logger().debug('project opened: %r' % window)

        # update recent files
        if tab_to_open:
            window.open_file(tab_to_open)
        else:
            self._recents.open_file(window.projects[0])

        # show window
        self._show_window(window)

        # update the windows menu of all opened editor windows
        self._update_windows()

        self._qapp.restoreOverrideCursor()

        # hide welcome window
        self._welcome_window.hide()

        return True

    def _show_window(self, window):
        window.raise_()
        window.show()
        self._qapp.setActiveWindow(window)

    def _add_new_window(self, path, workspace):
        _logger().debug('creating new window')
        window = MainWindow(self, path=path, workspace=workspace)
        window._setup = True
        self._editor_windows.append(window)
        _logger().debug('setting up workspaces plugins')
        self._setup_workspace_plugins(window, workspace)
        _logger().debug('restoring state')
        if not window.restore_state(path):
            # show maximised the first time a window is created,
            # afterwards, restore_state will take care of restoring
            # the correct window size/show mode.
            window.showMaximized()
        _logger().debug('applying user preferences')
        window.apply_preferences()
        window.closed.connect(self._on_window_closed)
        window.current_project_changed.connect(self._update_windows)
        window.current_tab_changed.connect(self._update_windows)
        window.setup_status_bar()
        window._setup = False
        return window

    def _ask_open_mode(self, path):
        return DlgOpen.get_open_mode(self._qapp.activeWindow(), path)

    def _ask_for_workspace(self):
        workspaces = WorkspaceManager()
        names = workspaces.get_names()
        lnames = len(names)
        if lnames == 0 or 'HACKEDIT_CORE_TEST_SUITE' in os.environ:
            from hackedit.plugins.workspaces import GenericWorkspace
            workspace = GenericWorkspace().get_data()
        else:
            if lnames == 1:
                name = names[0]
            else:
                name = DlgSelectWorkspace.get_workspace(
                    self._welcome_window, self)
                if name is None:
                    return None
                # reload workspaces, user might have edited the workspaces
                workspaces = WorkspaceManager()
            workspace = workspaces.workspace_by_name(name)
        return workspace

    def _on_window_closed(self, window):
        self._editor_windows.remove(window)
        _logger().debug('window closed: %r' % window)
        self._update_windows()
        if self._editor_windows:
            self._last_window = self._editor_windows[0]

    def _set_active_window(self, window):
        _logger().debug('active window set to %r' % window)
        self._qapp.setActiveWindow(window)
        for w in self._editor_windows:
            if w != window:
                w.update_mnu_view()

    def _except_hook(self, exc_type, exc_val, tb):
        from cement.core.exc import CaughtSignal
        import signal
        if isinstance(exc_val, CaughtSignal) and exc_val.signum in [
                signal.SIGKILL, signal.SIGTERM]:
            os._exit(1)

        tb = '\n'.join([''.join(traceback.format_tb(tb)),
                        '{0}: {1}'.format(exc_type.__name__, exc_val)])
        # exception might come from another thread, use a signal
        # so that we can be sure we will show the bug report dialog from
        # the main gui thread.
        self._report_exception_requested.emit(exc_val, tb)

    def _report_exception(self, exc, tb):
        try:
            _logger().critical('unhandled exception:\n%s', tb)
            try:
                w = self._last_window
            except AttributeError:
                pass
            else:
                action = QtWidgets.QAction(None)
                action.setText('Restart HackEdit')
                action.triggered.connect(self.restart)
                ev = api.events.ExceptionEvent(
                    '[Unhandled exception]  %s: %s' % (
                        exc.__class__.__name__, str(exc)),
                    'An unhandled exception has occured: %r\n\n'
                    'Please report!' % exc, exc, tb=tb,
                    custom_actions=[action])
                w.notifications.add(ev, False, True)
        except Exception:
            _logger().exception('exception in excepthook')


# monkeypatch needed to use our pygments style plugins when pygments has
# been embedded in a zip.
from pygments import styles  # noqa

_get_style_by_name = styles.get_style_by_name


def get_style_by_name(name):
    try:
        style = _get_style_by_name(name)
    except Exception as e:
        if name == 'qt':
            from pyqode.core.styles import QtStyle
            style = QtStyle
        elif name == 'darcula':
            from pyqode.core.styles import DarculaStyle
            style = DarculaStyle
        else:
            raise e
    finally:
        return style


styles.get_style_by_name = get_style_by_name
