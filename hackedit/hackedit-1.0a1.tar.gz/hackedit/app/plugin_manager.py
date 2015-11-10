"""
This module contains the plugins manager that loads and store the various
plugins.
"""
import logging

import pkg_resources
from pyqode.core.widgets import SplittableCodeEditTabWidget

from hackedit.api import plugins, events
from hackedit.api.widgets import FileIconProvider


def _logger():
    return logging.getLogger(__name__)


class LoadPluginFailedEvent(events.ExceptionEvent):
    def __init__(self, title, description, exception, tb=None,
                 custom_actions=None):
        super().__init__(title, description, exception, tb, custom_actions)
        self.level = events.WARNING


class PluginManager:
    """
    Loads and store the various kind of plugins
    """
    def __init__(self):
        #: Map of workspace plugin classes
        self.workspace_plugins = {}
        #: List of window plugins.
        self.window_plugins = []
        #: List of preference pages plugins
        self.preferences_page_plugins = []
        #: The list of editor plugins classes
        self.editor_plugins = []
        #: The list of template provider plugins
        self.template_providers = []
        self.load_template_provider_plugins()
        self.load_editor_plugins()
        self.load_preferences_page_plugins()
        FileIconProvider.load_plugins()
        SplittableCodeEditTabWidget.icon_provider_klass = FileIconProvider

    def load_preferences_page_plugins(self):
        """
        Loads preferences pages plugins.
        """
        _logger().info('loading preferences pages plugins')
        entrypoints = list(pkg_resources.iter_entry_points(
            plugins.PreferencePagePlugin.ENTRYPOINT))
        for entrypoint in entrypoints:
            _logger().info('  - loading plugin: %s', entrypoint)
            try:
                plugin_class = entrypoint.load()
            except Exception:
                _logger().exception('failed to load preferences page plugin')
            else:
                self.preferences_page_plugins.append(plugin_class)
        _logger().debug('preferences page plugins: %r',
                        self.preferences_page_plugins)

    def load_template_provider_plugins(self):
        """
        Loads preferences pages plugins.
        """
        _logger().info('loading template provider plugins')
        entrypoints = list(pkg_resources.iter_entry_points(
            plugins.TemplateProviderPlugins.ENTRYPOINT))
        for entrypoint in entrypoints:
            _logger().info('  - loading plugin: %s', entrypoint)
            try:
                plugin_class = entrypoint.load()
            except Exception:
                _logger().exception('failed to load template provider plugin')
            else:
                self.template_providers.append(plugin_class())
        _logger().debug('template providers plugins: %r',
                        self.template_providers)

    def load_workspace_plugins(self, win=None):
        """
        Loads workspace plugins (plugins that are tied to a specific worskpace)
        """
        _logger().info('loading workspace plugins')
        entrypoints = list(pkg_resources.iter_entry_points(
            plugins.WorkspacePlugin.ENTRYPOINT))
        for entrypoint in entrypoints:
            _logger().info('  - loading plugin: %s', entrypoint)
            try:
                plugin_class = entrypoint.load()
            except Exception as e:
                name = str(entrypoint).split('=')[0].strip()
                if win:
                    event = LoadPluginFailedEvent(
                        '%r load failed' % name,
                        'Failed to load plugin %r because of the following '
                        'error: %r' % (name, str(e)), e)
                    win.notifications.add(event, force_show=True)
                else:
                    _logger().exception('Failed to load workspace plugin')
            else:
                self.workspace_plugins[plugin_class.__name__] = plugin_class
        _logger().debug('available workspace plugins: %r',
                        self.workspace_plugins)

    def load_editor_plugins(self):
        """
        Loads editor plugins.
        """
        _logger().info('loading editor plugins')
        entrypoints = list(pkg_resources.iter_entry_points(
            plugins.EditorPlugin.ENTRYPOINT))
        for entrypoint in entrypoints:
            _logger().info('  - loading plugin: %s', entrypoint)
            try:
                plugin_class = entrypoint.load()
            except Exception:
                _logger().exception('Failed to load editor plugin')
            else:
                try:
                    klass = plugin_class.get_editor_class()
                except AttributeError:
                    _logger().exception(
                        'invalid editor plugin: register_editor not '
                        'implemented')
                else:
                    SplittableCodeEditTabWidget.register_code_edit(klass)
                    self.editor_plugins.append(plugin_class)
