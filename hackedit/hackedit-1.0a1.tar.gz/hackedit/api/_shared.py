"""
**Internal** helper module shared by most api modules to retrieve the current
MainWindow instance.
"""
import inspect

from PyQt5 import QtWidgets


_APP = None


def _window():
    """
    Retrieves window instance from the caller object (usually a WorkspacePlugin
    or a WindowPlugin).

    If there is no caller object, the active window is used, this allow
    to hack HackEdit from the IPython console!

    This is used to simplify the public API: plugins don't need to pass
    the `window` parameter to the public API functions everytime...

    :rtype: hackedit.app.gui.main_window.MainWindow
    """
    def caller():
        frame = inspect.stack()[3][0]
        caller = frame.f_locals.get('self', None)
        return caller

    try:
        w = caller()._window
        if w:
            return w
        raise AttributeError('None _window')
    except (AttributeError, IndexError):
        # not from a plugin, use active window instead
        w = QtWidgets.qApp.activeWindow()

        from hackedit.app.main_window import MainWindow

        if not isinstance(w, MainWindow):
            try:
                try:
                    w = _APP._last_window
                except AttributeError:
                    w = None
                if w is None:
                    w = _APP._editor_windows[0]
            except IndexError:
                w = None

        return w
