"""
This module contains the file indexor.

The file index is in charge of indexing the symbols found in every
project files. It does that for each file whenever the project files list
has been updated and whenever a file has been saved.

The indexor make use of the registered FileSymbolParserPlugin to get as much
symbols as possible (even if the project mix several programming languages).
"""
import logging
import mimetypes
import os

import pkg_resources

from hackedit import api
from hackedit.app import mime_types


def _logger():
    return logging.getLogger(__name__)


def index_project_files(th, prj, project_files, indexor_plugins):
    # load user defined mimetypes (we are in a background process!)
    mime_types.load()
    all_symbols = []
    path_exists = os.path.exists
    path_split = os.path.split
    count = len(project_files)
    for i, file in enumerate(project_files):
        if not path_exists(file):
            continue
        th.report_progress(
            'indexing %s' % path_split(file)[1], i/count*100)
        path, symbols = parse_document(prj, file, indexor_plugins)
        all_symbols += symbols
    api.project.set_project_symbols(prj, all_symbols)
    return


def parse_document(prj, path, indexor_plugins):
    mime = mimetypes.guess_type(path)[0]
    for plugin in indexor_plugins:
        if mime in plugin.mimetypes:
            try:
                symbols = plugin.parse(path)
            except Exception as e:
                print(path, e)
            else:
                break
    else:
        symbols = []

    return path, symbols


def index_document(th, prj, path, indexor_plugins):
    mime_types.load()
    path, symbols = parse_document(prj, path, indexor_plugins)
    all_symbols = api.project.get_project_symbols(prj)
    # remove all symbols for the specified path
    to_remove = []
    for symbol in all_symbols:
        if symbol.file_path == path:
            to_remove.append(symbol)
    for symbol in to_remove:
        all_symbols.remove(symbol)
    # update symbols
    all_symbols += symbols
    api.project.set_project_symbols(prj, all_symbols)


class FileIndexor:
    def __init__(self, window):
        self._window = window   # this let us use the hackedit.api functions.
        self._plugins = []
        self._load_plugins()
        self._pending_task = None
        api.signals.connect_slot(
            api.signals.PROJECT_FILES_AVAILABLE, self._index_all)
        api.signals.connect_slot(
            api.signals.DOCUMENT_SAVED, self._index_document)

    def _load_plugins(self):
        _logger().debug('loading symbol indexors plugins')
        for entrypoint in pkg_resources.iter_entry_points(
                api.plugins.SymbolIndexorPlugin.ENTRYPOINT):
            _logger().debug('  - loading plugin: %s', entrypoint)
            try:
                plugin = entrypoint.load()()
            except ImportError:
                _logger().exception('failed to load plugin')
            else:
                self._plugins.append(plugin)
                _logger().debug('  - plugin loaded: %s', entrypoint)
        _logger().debug('indexor plugins: %r', self._plugins)

    def force_stop(self):
        if self._pending_task:
            self._pending_task.cancel()
            self._pending_task = None

    def _index_all(self, project_files):
        """
        Indexates symbols found in all project files.

        When the task has finished, the list of project symbols will be
        updated.
        """
        if self._pending_task is None:
            self._task_running = True
            self._pending_task = api.tasks.start(
                'Indexing project symbols', index_project_files,
                self._on_task_finished, args=(
                    api.project.get_root_project(), project_files,
                    self._plugins), cancellable=False)

    def _index_document(self, path, _):
        """
        Indexates symbols found in a given document.
        """
        if self._pending_task is None:
            self._task_running = True
            self._pending_task = api.tasks.start(
                'Indexing file symbols',
                index_document, self._on_task_finished,
                args=(api.project.get_root_project(), path, self._plugins),
                cancellable=False)

    def _on_task_finished(self, *_):
        self._pending_task = None
