import time

from PyQt5 import QtCore, QtWidgets

from .test_window import win, FILE1, FILE2
from hackedit.api import editor


def test_open_file(qtbot):
    win(qtbot)
    assert len(editor.get_all_paths()) == 0
    editor.open_file(FILE1)
    assert len(editor.get_all_paths()) == 1
    editor.open_file(FILE2)
    assert len(editor.get_all_paths()) == 2


def test_get_current_editor(qtbot):
    win(qtbot)
    assert editor.get_current_editor() is None
    editor.open_file(FILE1)
    assert editor.get_current_editor() is not None


def test_get_current_path(qtbot):
    win(qtbot)
    assert editor.get_current_path() is None
    editor.open_file(FILE1)
    assert editor.get_current_path() == FILE1


def test_get_all_paths(qtbot):
    win(qtbot)
    editor.open_file(FILE1)
    editor.open_file(FILE2)
    assert len(editor.get_all_editors()) == 2
    assert editor.get_all_paths() == [FILE1, FILE2]


def test_save_current_editor(qtbot):
    win(qtbot)
    editor.open_file(FILE1)
    editor.save_current_editor()


def test_save_all_editors(qtbot):
    win(qtbot)
    editor.open_file(FILE1)
    editor.open_file(FILE2)
    editor.save_all_editors()
