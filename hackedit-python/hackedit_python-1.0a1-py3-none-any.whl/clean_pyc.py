import logging
import os
import shutil

from PyQt5 import QtGui
from hackedit import api


class CleanPycFiles(api.plugins.WorkspacePlugin):
    """
    Cleans python bytecode (*.pyc/__pycache__)
    """
    def activate(self):
        menu = api.window.get_menu('&Python')
        menu.addSeparator()
        self.action_clean = menu.addAction('Clean *.pyc files')
        self.action_clean.setIcon(QtGui.QIcon.fromTheme('edit-clear'))
        self.action_clean.setToolTip(
            'Removes *.pyc/__pycache__ for the active project')
        self.action_clean.triggered.connect(self._clean_pyc_files)

    def _clean_pyc_files(self):
        api.tasks.start('Cleaning *.pyc files', clean_pyc_files, None,
                        args=(api.project.get_projects(),))


def clean_directory(path):
    for filename in os.listdir(path):
        fpath = os.path.join(path, filename)
        if os.path.splitext(filename)[1] == '.pyc':
            try:
                os.remove(fpath)
            except OSError:
                _logger().debug('failed to delete file %s', fpath)
            else:
                _logger().debug('- %s removed', fpath)
        elif os.path.isdir(fpath):
            if filename == '__pycache__':
                shutil.rmtree(fpath, ignore_errors=True)
                _logger().debug('- %s removed', fpath)
            else:
                clean_directory(fpath)


def clean_pyc_files(_, project_paths):
    for i, path in enumerate(project_paths):
        clean_directory(path)


def _logger():
    return logging.getLogger(__name__)
