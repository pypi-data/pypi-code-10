"""
Contains internal objects used to manage the notifications of a specific
window.

"""
# todo:
# - settings
import logging

from PyQt5 import QtWidgets, QtGui, QtCore

from hackedit import api
from hackedit.app import settings
from hackedit.app.forms import event_widget_ui, event_history_widget_ui


ICONS = {
    api.events.INFO: 'dialog-information',
    api.events.WARNING: 'dialog-warning',
    api.events.ERROR: 'dialog-error',
}

MSG_ICONS = {
    api.events.INFO: QtWidgets.QSystemTrayIcon.Information,
    api.events.WARNING: QtWidgets.QSystemTrayIcon.Warning,
    api.events.ERROR: QtWidgets.QSystemTrayIcon.Critical,
}

ICON_SIZE = 24

try:
    import gi
except ImportError:
    Notify = None
else:
    try:
        gi.require_version('Notify', '0.7')
    except ValueError:
        pass
    finally:
        try:
            from gi.repository import Notify
        except ImportError:
            pass
        else:
            Notify.init("HackEdit")


class Widget(QtWidgets.QFrame):
    """
    Widget that shows the content of an event.
    """
    closed = QtCore.pyqtSignal(object)

    def __init__(self, event):
        """
        :type event: hackedit.api.events.Event
        """
        global ICONS, ICON_SIZE
        super().__init__()
        self.event = event
        self.setFrameShape(self.StyledPanel)
        self.setFrameShadow(self.Sunken)
        self.ui = event_widget_ui.Ui_Form()
        self.ui.setupUi(self)
        self.ui.lbl_title.setText(event.title)
        self.ui.lbl_description.setText(event.description)
        self.ui.lbl_time.setText(event.time_str)
        self.ui.lbl_pixmap.setPixmap(QtGui.QIcon.fromTheme(
            ICONS[event.level]).pixmap(ICON_SIZE, ICON_SIZE))
        links = []
        for action in event.actions:
            links.append(
                '<a href="%s">%s</a>\t' % (action.text(), action.text()))
            self.ui.lbl_actions.setText('&nbsp;|&nbsp;'.join(links))
        self.ui.lbl_actions.setOpenExternalLinks(False)
        self.ui.lbl_actions.linkActivated.connect(self._on_link_activated)
        self.adjustSize()
        self.ui.toolButton.clicked.connect(self.close)

    def _request_close(self, *_):
        self.close()

    def _on_link_activated(self, link):
        for action in self.event.actions:
            if action.text() == link:
                action.triggered.emit()
                break

    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit(self)


class HistoryWidget(QtWidgets.QWidget):
    """
    Dock widget that shows the event log history.
    """
    contents_cleared = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = event_history_widget_ui.Ui_Form()
        self.ui.setupUi(self)
        self._events = []
        self.ui.bt_clear.clicked.connect(self._clear)

    def add(self, event):
        global ICONS
        self._events.insert(0, event)
        event.widget = Widget(event)
        event.widget.closed.connect(self._on_widget_closed)
        event.remove_requested.connect(self.remove_event)
        self.ui.vertical_layout.insertWidget(0, event.widget)

    def remove_event(self, event):
        self.ui.vertical_layout.removeWidget(event.widget)
        event.widget.setParent(None)
        event.widget = None
        self._events.remove(event)
        if self.count() == 0:
            self.contents_cleared.emit()

    def _on_widget_closed(self, widget):
        self.remove_event(widget.event)
        widget.event = None

    def count(self):
        return len(self._events)

    def _clear(self):
        while self.count():
            self.remove_event(self._events[0])


class Manager(QtCore.QObject):
    """
    Main object for managing window events. This class creates a dock widget
    view where the events are appended.
    """
    def __init__(self, window):
        super().__init__()
        self._window = window
        # highest level met until now, determine which icon is used
        self._highest_level = api.events.INFO
        #: history of notifications
        self._history = HistoryWidget()
        self._history.contents_cleared.connect(self._on_content_cleared)
        # custom dock widget
        self.dock = api.window.add_dock_widget(
            self._history, 'Events', QtGui.QIcon.fromTheme(
                'preferences-desktop-notification'), special=True)
        api.signals.connect_slot(api.signals.STATE_RESTORED,
                                 self.dock.hide)
        self.tool_button = self.dock.button
        self._update_tool_button()

    def close(self):
        self._window = None

    def show(self):
        self.dock.show()

    def has_errors(self):
        return self._highest_level == api.events.ERROR

    def has_warnings(self):
        return self._highest_level == api.events.WARNING

    def add(self, e, show_balloon=True, force_show=False):
        """
        Adds an event to the history.

        :type e: hackedit.api.events.Event
        """
        if api.events.is_blacklisted(e):
            return
        _logger().log(
            e.level, '%s\n%s', e.title, e.description)
        tray_icon = api.window.get_tray_icon()
        if show_balloon and settings.show_notification_in_sytem_tray():
            if Notify:
                icons = ICONS.copy()
                icons[api.events.INFO] = 'hackedit'
                n = Notify.Notification.new(
                    'HackEdit: %s' % e.title, e.description,
                    icons[e.level])
                n.show()
            else:
                tray_icon.showMessage(
                    'HackEdit: %s' % e.title, e.description,
                    MSG_ICONS[e.level])
        tray_icon.last_window = self._window
        self._history.add(e)
        if e.level > self._highest_level:
            self._highest_level = e.level
        self._update_tool_button()
        # todo make this configurable
        flags = {
            api.events.INFO: settings.auto_open_info_notification(),
            api.events.WARNING: settings.auto_open_warning_notification(),
            api.events.ERROR: settings.auto_open_error_notification()
        }
        if flags[e.level] or force_show:
            self.dock.show()

    def _update_tool_button(self):
        self.tool_button.setEnabled(self._history.count() > 0)
        if self._history.count() > 0:
            self.tool_button.setIcon(self._icon(self._highest_level))
        else:
            self.tool_button.setIcon(QtGui.QIcon.fromTheme(
                'preferences-desktop-notification'))

    def _icon(self, level):
        global ICONS
        return QtGui.QIcon.fromTheme(ICONS[level])

    def _on_content_cleared(self):
        self._highest_level = api.events.INFO
        self._update_tool_button()
        self.dock.hide()


def _logger():
    return logging.getLogger(__name__)
