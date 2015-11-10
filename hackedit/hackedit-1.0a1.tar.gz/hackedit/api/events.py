"""
API for showing event notifications to the user.

Event notifications are stored in a history view accessible from the
bottom right corner of the window (Events button) and are automatically
appended to the application log with the corresponding log level.

If enabled, notifications can be logged to the application system tray.

There are 3 level of notification:
    - INFO: used to display information messages, the popup will have a
      native background color and the "dialog-information" icon.
    - WARNING: used to display user warnings, the popup will have a yellow
      background color and the "dialog-warning" icon.
    - ERROR: used to report internal errors, the popup will have a red
      background color and the "dialog-error" icon.

To post an event notifications, create a :class:`Event` instance and pass it
to the :func:`post` function.
"""
import traceback
import datetime
import json
import logging

from PyQt5 import QtCore, QtWidgets

from hackedit.app import settings
from ._shared import _window


# -------------- Event levels
#: Level for showing general information message (updates, ...)
INFO = logging.INFO
#: Level for showing warning messages (possible misconfiguration, ...)
WARNING = logging.WARNING
#: Level for showing errors (e.g. unhandled exceptions are reported that way)
ERROR = logging.ERROR


class Event(QtCore.QObject):
    """
    Base class for showing event notifications using the :func:`post` function

    You can subclass to implement the slots for your ``custom_actions``.
    """
    #: Signal emitted when the event is blacklisted by the user or if the
    #: event wants to be removed (e.g. after a custom action has been executed)
    remove_requested = QtCore.pyqtSignal(object)

    @property
    def actions(self):
        return [self.action_blacklist] + self.custom_actions

    def __init__(self, title, description, level=INFO, custom_actions=[]):
        """
        :param title: Title of the event, 80 characters max.
        :param description: Multiline description
        :param level: Event level (one of attr:`INFO`, :attr:`WARNING`,
            :attr:`ERROR`)
        :param custom_actions: list of custom QAction that will be shown
            on the event widget.
        """
        super().__init__()
        #: Title (short, one liner)
        self.title = title[:80]
        #: Long description
        self.description = description
        #: Level
        self.level = level
        #: List of custom actions
        self.custom_actions = custom_actions
        #: reference to the bound IDE window
        self.window = None
        #: time string, automatically set when the event got instanciated
        self.time_str = datetime.datetime.now().strftime('%H:%M:%S')
        self.action_blacklist = QtWidgets.QAction(None)
        self.action_blacklist.setText("Don't show again")
        self.action_blacklist.setObjectName('actionDontShowAgain')
        self.action_blacklist.triggered.connect(self._blacklist_event)

    def _blacklist_event(self):
        """
        Put this event on the events blacklist.
        """
        add_to_blacklist(self)
        self.remove_requested.emit(self)

    def remove(self):
        self.remove_requested.emit(self)


class ExceptionEvent(Event):
    def __init__(self, title, description, exception, tb=None,
                 custom_actions=None):
        if custom_actions is None:
            custom_actions = []
        if tb is None:
            tb = traceback.format_exc()
        self.traceback = tb
        self.exc = exception
        self.action_details = QtWidgets.QAction('Details', None)
        self.action_details.triggered.connect(self.show_details)
        self.action_report = QtWidgets.QAction('Report', None)
        self.action_report.triggered.connect(self.report_bug)
        actions = [self.action_details, self.action_report] + custom_actions
        super().__init__(
            title, description, level=ERROR, custom_actions=actions)

    def show_details(self):
        QtWidgets.QMessageBox.warning(
            self.window, 'Details',
            'Exception details:\n\n %s' % self.traceback)

    def report_bug(self):
        from hackedit.app import common
        if common.report_bug(
                self.window, title=self.title,
                description='``` \n%s\n```' % self.traceback):
            self.remove()


def add_to_blacklist(event):
    """
    Adds an event to the events blacklist.

    Blacklisted events won't show up in the history.
    """
    blacklist = _get_blacklist()
    blacklist.append(event.title)
    _set_blacklist(blacklist)


def is_blacklisted(event):
    """
    Blacklisted event don't show up in the event log.
    """
    return event.title in _get_blacklist()


def clear_blacklist():
    """
    Clears the event blacklist.
    """
    _set_blacklist([])


def _set_blacklist(blacklist):
    """
    Saves the event blacklist

    :param blacklist: the list of event blacklist to save
    """
    settings._SETTINGS.setValue(
        'env/events_blacklist', json.dumps(list(set(blacklist))))


def _get_blacklist():
    """
    Gets the event blacklist.
    """
    return list(set(json.loads(
        settings._SETTINGS.value('env/events_blacklist', '[]'))))


def post(event, show_balloon=None, force_show=False):
    """
    Sends the notification to the main window.

    :param event: The notification to post
    :type event: Event
    :param show_balloon: True to show a message ballon in the system tray.
        False to only post event internally.
    :param force_show: True to force show the events dock widget.
    """
    # show notifications on the active window
    event.window = _window()
    if show_balloon is None and not event.window._setup:
        show_balloon = not event.window.isVisible()
    _window().notifications.add(event, show_balloon, force_show)


def test():
    """
    Test notifications system.

    Paste the following code in the IPython console to test it:

    from hackedit.api.events import test; test()
    """
    from PyQt5 import QtWidgets

    def show_msg_box():
        QtWidgets.QMessageBox.information(
            QtWidgets.qApp.activeWindow(), 'Click me',
            'Bravo! You successfully clicked on an event link')

    action = QtWidgets.QAction(None)
    action.setText('Click me')
    action.setObjectName('actionClickHere')
    action.triggered.connect(show_msg_box)

    post(Event('Information event', 'An information message...',
               custom_actions=[action]))
    post(Event('Warning event', 'A warning message...', level=WARNING))
    post(Event('Error event', 'An error message...', level=ERROR))


def test_info():
    post(Event('Information event', 'An information message...'))


def test_warning():
    post(Event('Warning event', 'A warning message...', level=WARNING))


def test_error():
    post(Event('Error event', 'An error message...', level=ERROR))
