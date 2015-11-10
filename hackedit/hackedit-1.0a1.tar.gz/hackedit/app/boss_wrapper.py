"""
A small procedural API that wraps the main features of the boss
cli application (https://github.com/datafolklabs/boss)

Use this module if you'd like to use boss from within your own python app.
"""
import logging
import os
import re
import shelve
import shutil
from functools import wraps
from tempfile import mkdtemp

from PyQt5 import QtWidgets
from boss.cli import bootstrap
from boss.cli.main import BossApp
from boss.cli.source import SourceManager
from boss.cli.template import TemplateManager
from boss.core import exc
from boss.utils.version import get_version
from cement.core import hook
from cement.utils import fs


BOSS_APP = None


def boss_app(func, default_ret_val=None):
    """
    Decorators that automatically set up the BOSS_APP global variable and
    make sure it is properly closed when the decorated function exits.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        global BOSS_APP
        BOSS_APP = BossApp()
        BOSS_APP.setup()
        try:
            ret_val = func(*args, **kwargs)
        except Exception:
            _logger().exception('failed to execute boss command: %s',
                                func.__name__)
            ret_val = default_ret_val
        BOSS_APP.close()
        return ret_val
    return wrapper


#
# API
#
def version():
    """
    Gets the boss program version
    """
    return get_version()


@boss_app
def create(source, template, dest_dir, input_handler=None, default=False):
    """
    Creates a project from template.

    :param source: Source label
    :param template: Name of the template
    :param dest_dir: Destination directory.
    :param input_handler: callable used to provide answers to the template
        manager. If None, input/raw_input will be used. The function must have
        the following prototype: ``def function(question) -> answer``
    """
    global BOSS_APP
    files = SourceManager(BOSS_APP).create_from_template(
        source, template, dest_dir, input_handler, default)
    return files


@boss_app
def templates():
    """
    Generator that lists the available templates.

    Returns tuples made up of the source label and the template name.
    """
    global BOSS_APP
    sources = BOSS_APP.db['sources']
    ret = []
    for label, data in sources.items():
        src = SourceManager(BOSS_APP)
        try:
            for tmpl in src.get_templates(label):
                ret.append((label, tmpl))
        except FileNotFoundError:
            pass
    return sorted(ret, key=lambda x: x[1])


@boss_app
def project_templates():
    """
    Generator that lists the available project templates.

    Returns tuples made up of the source label and the template name.
    """
    global BOSS_APP
    ret = []
    for label, template in templates():
        src = SourceManager(BOSS_APP)
        meta = src.get_template_metadata(label, template)
        if meta and 'type' in meta and meta['type'] == 'Project':
            ret.append((label, template))
    return sorted(ret, key=lambda x: x[1])


def file_templates(include_meta=False):
    """
    Generator that lists the available project templates.

    Returns tuples made up of the source label and the template name.
    """

    @boss_app
    def filter_templates(tmp):
        global BOSS_APP
        ret = []
        for label, template in tmp:
            src = SourceManager(BOSS_APP)
            meta = src.get_template_metadata(label, template)
            if meta and 'category' in meta and meta['category'] == 'File':
                if include_meta:
                    val = (label, template, meta)
                else:
                    val = (label, template)
                ret.append(val)
        return ret
    tmp = []
    for v in templates():
        tmp.append(v)
    return sorted(filter_templates(tmp), key=lambda x: x[1])


@boss_app
def get_template_metadata(label, template):
    """
    Gets the metadata of a template

    :param label: source label
    :param template: template id
    """
    global BOSS_APP
    src = SourceManager(BOSS_APP)
    ret = src.get_template_metadata(label, template)
    return ret


@boss_app
def sync():
    """
    Syncs all source repositories.
    """
    global BOSS_APP
    if shutil.which('git') is not None:
        for label in BOSS_APP.db['sources']:
            src = SourceManager(BOSS_APP)
            src.sync(label)


@boss_app
def sources():
    """
    Generators that lists the available sources.
    """
    global BOSS_APP
    ret = []
    for key in BOSS_APP.db['sources']:
        src = BOSS_APP.db['sources'][key]
        ret.append(src)
    return sorted(ret, key=lambda x: x['label'])


@boss_app
def add_source(label, path, local=False):
    """
    Adds a source repository. The repository can be either a remote git
    repository or a local path. If you're using a local path, make sure to
    set local to True.

    :param label: Source label.
    :param path: source path.
    :param local: Whether path is local or not (e.g. a git repo).
    """
    global BOSS_APP
    SourceManager(BOSS_APP).add_source(label, path, local)


@boss_app
def rm_source(source_label):
    """
    Removes a source repository.
    """
    global BOSS_APP
    SourceManager(BOSS_APP).rm_source(source_label)


@boss_app
def clean(path):
    """
    Removes ``.boss.bak*`` files from ``path``.

    :param path: path to clean up.
    """
    global BOSS_APP

    def _clean(path, app):
        for items in os.walk(path):
            for _file in items[2]:
                path = fs.abspath(os.path.join(items[0], _file))
                if re.match('(.*)\.boss\.bak(.*)', path):
                    app.log.warn("Removing: %s" % _file)
                    os.remove(path)

    _clean(path, BOSS_APP)


def qt_input_handler(question, default=''):
    answer = ''
    while not answer:
        answer, _ = QtWidgets.QInputDialog.getText(
            QtWidgets.qApp.activeWindow(), 'Create from template', question)
        answer = answer.strip()
    return answer


#
# Monkeypatching for a better integration with a gui app
#
def _create_from_template(self, source, template, dest_dir, input_handler,
                          default=False):
    try:
        src = self.app.db['sources'][source]
    except KeyError:
        raise exc.BossTemplateError(
            "Source repo '%s' " % source + "does not exist.")

    if src['is_local']:
        basedir = os.path.join(src['path'], template)
    else:
        basedir = os.path.join(src['cache'], template)

    tmpl = TemplateManager(self.app, fs.abspath(basedir), input_handler,
                           default)
    tmpl.copy(dest_dir)
    return tmpl.written_files


def _get_template_manager(self, source, template):
    try:
        src = self.app.db['sources'][source]
    except KeyError:
        raise exc.BossTemplateError(
            "Source repo '%s' " % source + "does not exist.")

    if src['is_local']:
        basedir = os.path.join(src['path'], template)
    else:
        basedir = os.path.join(src['cache'], template)

    tmpl = TemplateManager(self.app, fs.abspath(basedir), lambda x: None, True)
    return tmpl


def _get_template_metadata(self, source, templ):
    try:
        return self.get_template_manager(source, templ).config['metadata']
    except KeyError:
        return None


def _add_source(self, label, path, local):
    sources = self.app.db['sources']
    cache_dir = mkdtemp(dir=self.app.config.get('boss', 'cache_dir'))

    if local:
        path = fs.abspath(path)

    sources[label] = dict(
        label=label,
        path=path,
        cache=cache_dir,
        is_local=local,
        last_sync_time='never'
        )
    self.app.db['sources'] = sources


def _rm_source(self, label):
    sources = self.app.db['sources']
    if label not in sources:
        raise exc.BossArgumentError("Unknown source repository.")
    cache = sources[label]['cache']
    if os.path.exists(cache):
        shutil.rmtree(cache)

    del sources[label]
    self.app.db['sources'] = sources


SourceManager.get_template_manager = _get_template_manager
SourceManager.get_template_metadata = _get_template_metadata
SourceManager.create_from_template = _create_from_template
SourceManager.add_source = _add_source
SourceManager.rm_source = _rm_source


def _init(self, app, path, input_handler, default):
    if input_handler is None:
        input_handler = input
    self.default = default
    self.input_handler = input_handler
    self.app = app
    self.basedir = fs.abspath(path)
    try:
        self.config = self._get_config()
    except Exception:
        app.log.warn("Failed to get config for : %s" % path)
        self.config = {}
    self._word_map = dict()
    self._vars = dict()
    self.written_files = []


def _write_file(self, dest_path, data, overwrite=False):
    fn = os.path.split(dest_path)[1]
    if 'boss.yml' not in fn and 'boss.json' not in fn:
        self._original_write_file(dest_path, data, overwrite)
        self.written_files.append(dest_path)


def _populate_vars(self):
    if 'variables' in self.config.keys():
        for var, question in self.config['variables'].items():
            res = self.input_handler("%s: " % question)
            self._vars[var] = res.strip()


TemplateManager.__init__ = _init
TemplateManager._populate_vars = _populate_vars
TemplateManager._original_write_file = TemplateManager._write_file
TemplateManager._write_file = _write_file


def _close(self, code=None):
    """
    Close the application.  This runs the pre_close and post_close hooks
    allowing plugins/extensions/etc to 'cleanup' at the end of program
    execution.

    :param code: An exit code to exit with (`int`), if `None` is passed
     then exit with whatever `self.exit_code` is currently set to.

    """
    for res in hook.run('pre_close', self):
        pass

    for res in hook.run('post_close', self):
        pass

BossApp.close = _close


def _setup_db(app):
    # monkeypatch to avoid the inclusion of the default boss templates
    app.extend('db', shelve.open(app.config.get('boss', 'db_path')))
    if 'sources' not in app.db.keys():
        app.db['sources'] = dict()

    if 'templates' not in app.db.keys():
        app.db['templates'] = dict()


bootstrap.setup_db = _setup_db


def _logger():
    return logging.getLogger(__name__)
