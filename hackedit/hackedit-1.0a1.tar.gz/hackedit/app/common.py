"""
Functions shared across the main window, the welcome window and the system
tray.

"""
import os

from PyQt5 import QtWidgets

from hackedit.app import boss_wrapper as boss, settings
from hackedit.app.dialogs.dlg_about import DlgAbout
from hackedit.app.dialogs.preferences import DlgPreferences
from hackedit.app.dialogs.report_bug import DlgReportBug
from hackedit.app.wizards.new import WizardNew


def show_about(window):
    """
    Shows the about dialog on the parent window

    :param window: parent window.
    """
    DlgAbout.show_about(window)


def check_for_update(window, show_up_to_date_msg=True):
    """
    Checks for update.

    :param window: parent window
    :param show_up_to_date_msg: True to show a message box when the
        app is up to date.
    """
    # todo: improve this: make an update wizard that update both hackedit
    # and its packages (to ensure compatiblity)
    # if pip_tools.check_for_update('hackedit', __version__):
    #     answer = QtWidgets.QMessageBox.question(
    #         window, 'Check for update',
    #         'A new version of HackEdit is available...\n'
    #         'Would you like to install it now?')
    #     if answer == QtWidgets.QMessageBox.Yes:
    #         try:
    #             status = pip_tools.graphical_install_package(
    #                 'hackedit', autoclose_dlg=True)
    #         except RuntimeError as e:
    #             QtWidgets.qApp.processEvents()
    #             QtWidgets.QMessageBox.warning(
    #                 window, 'Update failed',
    #                 'Failed to update hackedit: %r' % e)
    #         else:
    #             QtWidgets.qApp.processEvents()
    #             if status:
    #                 QtWidgets.QMessageBox.information(
    #                     window, 'Check for update',
    #                     'Update completed with sucess, the application '
    #                     'will now restart...')
    #                 window._app.restart()
    #             else:
    #                 QtWidgets.QMessageBox.warning(
    #                     window, 'Update failed',
    #                     'Failed to update hackedit')
    # else:
    #     _logger().debug('HackEdit up to date')
    #     if show_up_to_date_msg:
    #         QtWidgets.QMessageBox.information(
    #             window, 'Check for update', 'HackEdit is up to date.')
    pass


def open_folder(window, app):
    path = QtWidgets.QFileDialog.getExistingDirectory(
        window, 'Open directory', settings.last_open_dir())
    if path:
        settings.set_last_open_dir(os.path.dirname(path))
        app.open_path(path, sender=window)


def report_bug(window, title='', description=''):
    return DlgReportBug.report_bug(window, title=title,
                                   description=description)


def edit_preferences(window, app):
    DlgPreferences.edit_preferences(window, app)


def not_implemented_action(window):
    QtWidgets.QMessageBox.information(
        window, 'Not implementeded',
        'This action has not been implemented yet...')


def create_new(app, window, current_project=None):
    source, template, dest_dir, single_file = WizardNew.get_parameters(
        window, current_project)
    if source is not None:
        create_new_from_template(source, template, dest_dir, single_file,
                                 window, app)


def create_new_from_template(source, template, dest_dir, single_file, window,
                             app):
    files = boss.create(source, template, dest_dir,
                        input_handler=boss.qt_input_handler)
    if single_file:
        path = files[0]
    else:
        path = dest_dir

    from hackedit.app.welcome_window import WelcomeWindow
    if isinstance(window, WelcomeWindow):
        sender = None
    else:
        sender = window
    app.open_path(path, sender=sender)
