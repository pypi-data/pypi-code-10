"""
A set of utility functions that plugin would use.
"""
from PyQt5 import QtWidgets

from hackedit.app import settings, mime_types


def add_mimetype_extension(mimetype, extension):
    """
    Adds an extension to an existing mimetype.

    :param mimetype: mimetype to modify
    :param extension: extension to add
    :return:
    """
    exts = mime_types.get_extensions(mimetype)
    exts.append(extension)
    exts = list(set(exts))
    mime_types.set_extensions(mimetype, exts)


def get_mimetype_filter(mtype):
    """
    Gets the open file dialog filter for a given mimetype.

    :param mtype: Mime type (e.g. 'text/x-python' or 'text/x-cobol').
    """
    exts = ' '.join(mime_types.get_extensions(mtype))
    return '%s (%s)' % (mtype, exts)


def get_ignored_patterns():
    """
    Gets the list of ignored patterns.

    :return: a list of ignored patterns (fnmatch)
    """
    return settings.ignored_patterns()


def get_cmd_open_folder_in_terminal():
    """
    Returns the command to use to open a folder in a terminal.

    This takes the user's preferences into account.
    """
    return settings.get_cmd_open_folder_in_terminal()


def get_cmd_run_command_in_terminal():
    """
    Returns the command to use to run a file in a terminal

    This takes the user's preferences into account.
    """
    return settings.get_cmd_run_command_in_terminal()


def get_cmd_open_in_explorer():
    """
    Returns the command used to show a file/folder in the file explorer.
    """
    return settings.file_manager_cmd()


def color_scheme():
    """
    Returns the color scheme chosen by the usser
    """
    return settings.color_scheme()


def is_dark_color_scheme(scheme):
    """
    Checks if a given color scheme is a dark or not

    :param scheme: color scheme to test

    :return: True if scheme is a dark color scheme.
    """
    return settings.is_dark_color_scheme()


def is_dark_theme():
    """
    Checks if the dark theme is ON.

    Dark theme is either set by a stylesheet or by a gtk/kde color scheme.

    This function takes both into account.

    :return: True if the IDE is running in dark mode, False otherwise.
    """
    dark_stylesheet = settings.dark_theme()
    if not dark_stylesheet:
        dark_stylesheet = \
            QtWidgets.qApp.palette().base().color().lightness() < 128
    return dark_stylesheet


def editor_font():
    """
    Returns the editor font chose by the user.
    """
    return settings.editor_font()


def editor_font_size():
    """
    Returns the editor font chose by the user.
    """
    return settings.editor_font_size()
