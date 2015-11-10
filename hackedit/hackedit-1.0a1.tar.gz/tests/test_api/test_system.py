import os

from hackedit.api import system


def test_which():
    pth = system.which('python')
    assert os.path.exists(pth)
    assert os.path.isfile(pth)
    pth = system.which('foobar')
    assert pth is None


def test_get_authenticiation_program():
    system.get_authentication_program()


def test_get_app_data_dir():
    path = system.get_app_data_directory()
    assert os.path.exists(path)
