import platform
from ievv_opensource.utils.desktopnotifications import mocknotification
from ievv_opensource.utils.desktopnotifications import osxnotification


if platform.system().lower() == 'darwin':
    _notificationbackend = osxnotification.Notification()
else:
    _notificationbackend = mocknotification.Notification()


def show_message(title, message):
    """
    Show a message in the desktop notification system of the OS.

    Examples::

        Show a message::

            desktopnotifications.show_message(
                title='Hello world',
                message='This is a test')

    Currently this only works in OSX, but we would be happy
    to accept patches for other operating systems/desktop managers.
    See https://github.com/appressoas/ievv_opensource/issues/12.
    """
    _notificationbackend.show_message(title=title, message=message)


# if __name__ == '__main__':
#     show_message('Hello world', 'Testing "d\'s\'ad')
