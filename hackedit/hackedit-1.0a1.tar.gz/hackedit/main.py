#!/usr/bin/env python3
"""
Entry point of HackEdit.
"""
import logging
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from hackedit import __version__
from hackedit.app import argparser, logger


ZIP_PATH = os.environ.get('HACKEDIT_LIBS_PATH', None)
if not ZIP_PATH:
    # make sure external libs can be imported even if not installed.
    BASE = os.path.join(sys.prefix, 'share/hackedit/')
    if not os.path.exists(BASE):
        BASE = os.path.join(sys.prefix, 'local/share/hackedit/')
    if not os.path.exists(BASE):
        BASE = '/usr/local/share/hackedit/'
    ZIP_PATH = os.path.join(BASE, 'extlibs.zip')
    os.environ['HACKEDIT_LIBS_PATH'] = ZIP_PATH

# append insead of prepend to allow user to
# install another version if they want to...
sys.path.append(ZIP_PATH)


def main():
    """
    Application entry point, runs the application
    """
    try:
        sys.stdout.flush()
    except AttributeError:
        # this happen on windows when running with pythonw or the native
        # launcher
        sys.stdout = open('stdout', 'w')
        sys.stderr = open('stderr', 'w')

    # parse command line args
    args = argparser.parse_args()
    if args.log:
        # print the last application log
        try:
            with open(logger.get_path(), 'r') as f:
                print(f.read())
        finally:
            sys.exit(0)
    if args.version:
        # print versions
        from hackedit.api.versions import versions_str
        print(versions_str())
        sys.exit(0)

    # tell pyqode that we use the PyQt5 API.
    os.environ['QT_API'] = 'pyqt5'

    # Setup Qt Application
    qapp = QtWidgets.QApplication(sys.argv)
    qapp.setOrganizationName('HackEdit')
    qapp.setOrganizationDomain('hackedit.com')
    qapp.setApplicationDisplayName('HackEdit')
    qapp.setApplicationName('HackEdit')
    qapp.setApplicationVersion(__version__)

    # setup logger
    from hackedit.app import settings
    settings.load()

    log_level = settings.log_level()
    # override log level
    if args.log_level:
        log_level = args.log_level
    elif args.verbose:
        log_level = logging.DEBUG
    logger.setup(log_level)

    _logger().info('starting up...')

    try:
        import hackedit_python
    except ImportError:
        pass
    else:
        assert hackedit_python
        # THIS IS A HACK
        # On Ubuntu 15.04, if we don't do that, future instance will segfault.
        # and it must be done before showing the splash screen
        try:
            from IPython.qt.inprocess import QtInProcessKernelManager
        except ImportError:
            pass
        else:
            _kernel_manager = QtInProcessKernelManager()
            _kernel_manager.start_kernel()

    # Setup splash screen
    if settings.show_splashscreen():
        from hackedit.app.forms import hackedit_rc
        assert hackedit_rc

        pixmap = QtGui.QPixmap(':/splashscreen.png')
        splash = QtWidgets.QSplashScreen(pixmap)
        splash.show()
        splash.raise_()
        qapp.processEvents()

        splash.showMessage('Loading application module',
                           QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter,
                           QtCore.Qt.white)
        qapp.processEvents()

    else:
        splash = None

    # Setup hackedit application, this may take a while as we have
    # to load all plugin entry points, load the icon theme,...
    from hackedit.app.application import Application
    app = Application(qapp, splash, args)

    # Run the application!
    _logger().info('running...')
    app.run()


def _logger():
    return logging.getLogger(__name__)


if __name__ == '__main__':
    main()
