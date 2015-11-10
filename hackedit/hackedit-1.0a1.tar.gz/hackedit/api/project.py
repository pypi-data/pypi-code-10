"""
This module contains the API for managing projects.
"""
import json
import os

from pyqode.core.share import Definition

from ._shared import _window


#: Default project folder name
FOLDER = '.hackedit'


def open_project(path, sender=None):
    """
    Opens a project in a new window (or in the current window depending on the
    user's choice).

    .. note:: if path is a file, then the dirname is used instead and the file
              is open in a new tab automatically.

    :param path: path to the project to open. If path is a file, dirname is
                 used instead.
    """
    _window()._app.open_path(path, sender=sender)


def add_project(path):
    """
    Adds a project to the list of open projects (a project is just a foler).

    :param path: path of the project. If path is a file, the dirname is used
                 instead (and the file will get open in a new tab).
    """
    _window().open_folder(path)


def get_projects():
    """
    Returns the list of project/paths open in the main window.
    """
    return _window().projects


def get_current_project():
    """
    Gets the current project/file path.

    .. note:: This function returns the path of the active project, if you
              would like to get the path of the current editor, just use
              :func:`hackedit.api.editor.get_current_path`
    """
    return _window().current_project


def get_root_project():
    """
    Gets the root project/file path.

    The root project is the first open project, which contains links to other
    projects if any.

    .. note:: This function returns the path of the active project, if you
              would like to get the path of the current editor, just use
              :func:`hackedit.api.editor.get_current_path`
    """
    try:
        return _window().projects[0]
    except IndexError:
        return None


def get_project_files():
    """
    Gets the list of relevant project files.

    The list is fildered according to the ignore patterns defined
    in ``Preferences > Mimetypes``.

    .. note:: The list of project files is initially contains only the list of
        open files int the main tab widget.
        Use the signal :attr:`hackedit.api.signals.PROJECT_FILES_AVAILABLE`
        to know when the list is available.
    """
    files = _window().project_files
    # make sure to include external files currently opened.
    from hackedit.api.editor import get_all_paths
    files += get_all_paths()
    return sorted(list(set(files)))


def get_project_symbols(project_path):
    """
    Returns a dict that contains all the project symbols.

    Each key in the dict is a file path. Each value is a list of
    :class:`pyqode.core.share.Definition` for the associated file path.
    """
    usd = load_user_cache(project_path)
    try:
        symbols = usd['project_symbols']
    except KeyError:
        symbols = {}
    symbols = [Definition.from_dict(d) for d in symbols]
    return symbols


def set_project_symbols(project_path, symbols):
    usd = load_user_cache(project_path)
    symbols = [d.to_dict() for d in symbols]
    usd['project_symbols'] = symbols
    save_user_cache(project_path, usd)


def load_user_config(project_path):
    """
    Loads project user config (.hackedit/config.usr)

    The user config is used to stored user specific configuration (such as the
    directories he wants to ignore, the list of linked projects,...).

    :param project_path: path of the project to read user data from.
    :return: dict
    """
    path = os.path.join(project_path, FOLDER, 'config.usr')
    try:
        with open(path, 'r') as f:
            return json.loads(f.read())
    except (OSError, ValueError):
        return {}


def save_user_config(project_path, data):
    """
    Saves the project user config to the specified path

    :param project_path: project path
    :param data: data to save
    """
    path = os.path.join(project_path, FOLDER, 'config.usr')
    try:
        os.makedirs(os.path.dirname(path))
    except FileExistsError:
        pass
    # write data
    try:
        with open(path, 'w') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4,
                               separators=(',', ': ')))
    except PermissionError:
        pass


def load_user_cache(project_path):
    """
    Loads project user cache (.hackedit/cache.usr).

    The cache is used to cache project data such as the project files list,
    the list of symbols,...

    :param project_path: path of the project to read user data from.
    :return: dict
    """
    path = os.path.join(project_path, FOLDER, 'cache.usr')
    try:
        with open(path, 'r') as f:
            return json.loads(f.read())
    except (OSError, ValueError):
        return {}


def save_user_cache(project_path, data):
    """
    Saves the project user cache to the specified path

    :param project_path: project path
    :param data: data to save
    """
    path = os.path.join(project_path, FOLDER, 'cache.usr')
    try:
        os.makedirs(os.path.dirname(path))
    except FileExistsError:
        pass
    # write data
    try:
        with open(path, 'w') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4,
                               separators=(',', ': ')))
    except PermissionError:
        pass


def load_workspace(path):
    """
    Load workspace from project user data

    :param path: project path
    """
    from hackedit.app.workspaces import WorkspaceManager
    data = load_user_config(path)
    try:
        return WorkspaceManager().workspace_by_name(data['workspace'])
    except KeyError:
        return None


def save_workspace(path, workspace_name):
    """
    Saves the current workspace in project user data.
    """
    data = load_user_config(path)
    data['workspace'] = workspace_name
    try:
        save_user_config(path, data)
    except PermissionError:
        pass
