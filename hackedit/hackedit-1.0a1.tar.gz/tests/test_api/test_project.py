import os
import shutil

from PyQt5 import QtTest

from .test_window import win, PATH2
from hackedit.api import project
from hackedit.app import settings


PATH = os.path.join(os.getcwd(), 'tests', 'data', 'FooBarProj')
PATH3 = os.path.join(os.getcwd(), 'tests', 'data', 'SpamEggsProj2')
PATH4 = os.path.join(os.getcwd(), 'tests', 'data', 'SpamEggsProj3')


def test_open_proj_current_window(qtbot):
    w = win(qtbot)
    settings.set_open_mode(settings.OpenMode.CurrentWindow)
    assert len(project.get_projects()) == 1
    project.open_project(PATH2, sender=w)
    assert len(project.get_projects()) == 2
    QtTest.QTest.qWait(1000)


def test_add_project(qtbot):
    win(qtbot)
    assert len(project.get_projects()) == 2
    project.add_project(PATH3)
    assert len(project.get_projects()) == 3


def test_open_proj_new_window(qtbot):
    w = win(qtbot)
    settings.set_open_mode(settings.OpenMode.NewWindow)
    assert len(project.get_projects()) == 3
    project.open_project(PATH4, sender=w)
    assert len(w._app._editor_windows) == 2
    assert len(project.get_projects()) == 1


def setup():
    try:
        shutil.rmtree(os.path.join(PATH, project.FOLDER))
    except OSError:
        pass


def test_user_config():
    data = project.load_user_config(PATH)
    assert data == {}
    data = {'Foo': 'bar', 'Spam': 4, 'Eggs': [1, 2, 3]}
    project.save_user_config(PATH, data)
    usd = project.load_user_config(PATH)
    assert data == usd
    usd['Foo'] = 'BAR'
    project.save_user_config(PATH, usd)
