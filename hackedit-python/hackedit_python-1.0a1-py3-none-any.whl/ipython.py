"""
This plugin adds an IPython Console widget to HackEdit
"""
import logging

from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.qt.console.styles import default_dark_style_template, \
    default_light_style_sheet
from IPython.qt.inprocess import QtInProcessKernelManager
from PyQt5 import QtCore, QtGui
from hackedit import api
from hackedit.api import plugins, utils
from pyqode.core.api import ColorScheme


try:
    from PyQt5 import QtSvg
except ImportError:
    raise ImportError('IPython require PyQt5.QtSvg module')
else:
    assert QtSvg


def _logger():
    return logging.getLogger(__name__)


dark_stylesheet = default_dark_style_template % dict(
    bgcolor='#252525', fgcolor='#A9B7C6', select="#3d8ec9")


class QIPythonWidget(RichIPythonWidget):
    def __init__(self, custom_banner=None, *args, **kwargs):
        if custom_banner is not None:
            self.banner = custom_banner
        super(QIPythonWidget, self).__init__(*args, **kwargs)
        self.kernel_manager = kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        kernel_manager.kernel.gui = 'qt'
        self.kernel_client = kernel_client = self._kernel_manager.client()
        kernel_client.start_channels()


class IPythonConsole(plugins.WorkspacePlugin):
    def __init__(self, window):
        super().__init__(window)
        _logger().debug('initializing IPython widget')
        self._control = QIPythonWidget()
        if QtGui.QIcon.hasThemeIcon('ipython'):
            icon = QtGui.QIcon.fromTheme('ipython')
        else:
            icon = QtGui.QIcon(':/icons/ipython.png')
        dock = api.window.add_dock_widget(
            self._control, 'IPython console', icon,
            QtCore.Qt.BottomDockWidgetArea)
        dock.hide()
        dock.visibilityChanged.connect(self._on_visiblity_changed)
        self.apply_preferences()

    def _on_visiblity_changed(self, visible):
        if visible:
            self._control._control.setFocus()

    def apply_preferences(self):
        if utils.is_dark_theme() or \
                utils.is_dark_color_scheme(utils.color_scheme()):
            scheme = ColorScheme(utils.color_scheme())
            dark_stylesheet = default_dark_style_template % dict(
                bgcolor=scheme.background.name(), fgcolor='#A9B7C6',
                select="#3d8ec9")
            self._control.style_sheet = dark_stylesheet
        else:
            self._control.style_sheet = default_light_style_sheet
        self._control.syntax_style = utils.color_scheme()
        self._control._style_sheet_changed()
        self._control._syntax_style_changed()
        self._control.font = QtGui.QFont(utils.editor_font(),
                                         utils.editor_font_size())
