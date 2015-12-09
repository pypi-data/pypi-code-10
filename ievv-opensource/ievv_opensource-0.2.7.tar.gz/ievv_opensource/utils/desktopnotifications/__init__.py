import platform
from ievv_opensource.utils.desktopnotifications import mocknotification
from ievv_opensource.utils.desktopnotifications import osxnotification

notifications = None

if platform.system().lower() == 'darwin':
    _notificationbackend = osxnotification.Notification()
else:
    _notificationbackend = mocknotification.Notification()


def show_message(title, message):
    _notificationbackend.show_message(title=title, message=message)


# if __name__ == '__main__':
#     show_message('Test', 'ing"d\'s\'ad')
