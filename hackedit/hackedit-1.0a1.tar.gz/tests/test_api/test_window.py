import os
import shutil
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqode.core.widgets import FileSystemTreeView

from hackedit.api import editor, project, window
from hackedit.app import settings


DATA_FILES_PATH = os.path.join(os.getcwd(), 'tests', 'data')
PROJ_PATH = os.path.join(DATA_FILES_PATH, 'FooBarProj')
FILE1 = os.path.join(PROJ_PATH, 'module.py')
FILE2 = os.path.join(PROJ_PATH, 'setup.py')
PATH2 = os.path.join(DATA_FILES_PATH, 'SpamEggsProj')
APP = None
WINDOW = None


def win(qtbot):
    """
    This fixture creates a brand new editor window for use in test functions
    """
    try:
        shutil.rmtree(os.path.join(PROJ_PATH, project.FOLDER))
    except OSError:
        pass
    from hackedit.app.application import Application
    from hackedit.app import argparser
    global APP, WINDOW
    if APP is None:
        sys.argv = [sys.argv[0]]
        APP = Application(QtWidgets.qApp, None, args=argparser.parse_args())
    QtCore.QSettings().clear()
    settings.set_confirm_app_exit(False)
    if WINDOW is None:
        APP.open_path(PROJ_PATH)
        WINDOW = APP._editor_windows[-1]
    WINDOW.tab_widget.close_all()
    QtWidgets.qApp.setActiveWindow(WINDOW)
    return WINDOW


def test_add_tab_widget_context_menu_action(qtbot):
    w = win(qtbot)
    window.add_tab_widget_context_menu_action(QtWidgets.QAction('Test', w))


def test_get_tab_under_context_menu(qtbot):
    win(qtbot)
    editor.open_file(FILE1)
    assert window.get_tab_under_context_menu() is None


def test_add_dock_widget(qtbot):
    win(qtbot)
    editor.open_file(FILE1)
    dw = window.add_dock_widget(
        QtWidgets.QPushButton(), 'FooDock',
        QtGui.QIcon.fromTheme('document-save'),
        QtCore.Qt.BottomDockWidgetArea)
    assert dw is not None
    assert isinstance(dw, QtWidgets.QDockWidget)


def test_remove_dock_widget(qtbot):
    win(qtbot)
    editor.open_file(FILE1)
    dw = window.add_dock_widget(
        QtWidgets.QPushButton(), 'FooDock2',
        QtGui.QIcon.fromTheme('document-save'),
        QtCore.Qt.BottomDockWidgetArea)
    window.remove_dock_widget(dw)


def test_get_dock_widget(qtbot):
    win(qtbot)
    editor.open_file(FILE1)
    ret_val = window.get_dock_widget('FooDock')
    assert ret_val is not None


def test_get_main_window(qtbot):
    assert win(qtbot) == window.get_main_window()


def test_get_toolbar(qtbot):
    win(qtbot)
    tb = window.get_toolbar('toolBarFile', 'FileToolBar')
    assert isinstance(tb, QtWidgets.QToolBar)


def test_add__action(qtbot):
    w = win(qtbot)
    window.add_action(QtWidgets.QAction('Test', w))


def test_get_menu(qtbot):
    win(qtbot)
    mnu = window.get_menu('Edit')
    assert mnu is not None
    assert isinstance(mnu, QtWidgets.QMenu)


def test_get_project_treeview(qtbot):
    win(qtbot)
    assert isinstance(window.get_project_treeview(), FileSystemTreeView)


def test_add_statusbar_widget(qtbot):
    win(qtbot)
    lbl = QtWidgets.QLabel()
    window.add_statusbar_widget(lbl)
