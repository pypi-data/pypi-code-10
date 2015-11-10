import shutil
import os

from PyQt5 import QtWidgets


os.environ['PYTEST_QT_API'] = 'pyqt5'
os.environ['HACKEDIT_CORE_TEST_SUITE'] = '1'
os.environ['HACKEDIT_LIBS_PATH'] = 'data/share/extlibs.zip'


try:
    # THIS IS A HACK
    # On plasma 5, if we don't do that, future instance will segfault.
    # and it must be done before showing the splash screen
    from IPython.qt.inprocess import QtInProcessKernelManager
    _kernel_manager = QtInProcessKernelManager()
    _kernel_manager.start_kernel()
except ImportError:
    pass


QtWidgets.qApp.setOrganizationName('HackEdit-TestSuite')
QtWidgets.qApp.setApplicationDisplayName('HackEdit-TestSuite')
QtWidgets.qApp.setApplicationName('HackEdit-TestSuite')


for pth in ['tests/data/FooBarProj/.hackedit',
            'tests/data/SpamEggsProj/.hackedit',
            'tests/data/SpamEggsProj2/.hackedit',
            'tests/data/SpamEggsProj3/.hackedit']:
    try:
        shutil.rmtree(os.path.join(os.getcwd(), pth))
    except OSError:
        pass
