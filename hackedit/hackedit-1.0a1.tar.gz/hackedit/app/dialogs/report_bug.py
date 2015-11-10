import logging
import platform
import sys
import urllib.parse

from pyqode.qt import QtWidgets, QtCore, QtGui

from hackedit import __version__
from hackedit.api import utils
from hackedit.app import logger, versions
from hackedit.app.forms.dlg_report_bug_ui import Ui_Dialog


BUG_DESCRIPTION = '''%s

## System information

%s
'''

EMAIL_ADDRESS = 'colin.duquesnoy@gmail.com'


def _logger():
    return logging.getLogger(__name__)


class DlgReportBug(QtWidgets.QDialog):
    GITHUB_REPORT_LIMIT = 1200

    def __init__(self, parent, title, description):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        icons = [
            ':/icons/GitHub-Mark-32px.png',
            ':/icons/GitHub-Mark-Light-32px.png'
        ]
        icon = icons[0]
        if utils.is_dark_theme():
            icon = icons[1]
        self.ui.bt_submit.setIcon(QtGui.QIcon(icon))
        print(icon)
        self.ui.edit_title.textChanged.connect(self.enable_submit)
        self.ui.edit_desc.textChanged.connect(self.enable_submit)
        self.ui.edit_title.setText(title)
        self.ui.edit_desc.setPlainText(description)
        self.ui.bt_submit.clicked.connect(self.submit)
        self.ui.bt_send_mail.clicked.connect(self.send_mail)
        self.enable_submit()

    def enable_submit(self, *_):
        enable = self.ui.edit_title.text().strip() != '' and \
            self.ui.edit_desc.toPlainText().strip() != ''
        self.ui.bt_submit.setEnabled(enable)
        self.ui.bt_send_mail.setEnabled(enable)

    def _get_data(self):
        title = self.ui.edit_title.text().strip()
        description = self.ui.edit_desc.toPlainText().strip()
        if self.ui.cb_include_sys_info.isChecked():
            description = BUG_DESCRIPTION % (
                description, self.get_system_infos())
        return title, description

    def submit(self):
        title, description = self._get_data()
        url_data = urllib.parse.urlencode({
            'title': title, 'body': description[:self.GITHUB_REPORT_LIMIT]
        })
        url = b'https://github.com/HackEdit/hackedit/issues/new?' + \
              bytes(url_data, encoding='utf-8')
        QtWidgets.QMessageBox.information(
            self, 'Complete bug report on www.github.com',
            'To complete the report process, we need you to submit the '
            'generated ticket on our issue tracker. We will open a browser to '
            'our tracker. You just need to login with your github account and '
            'press the submit button at the bottom of the page.')
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromEncoded(url))
        self.accept()

    def send_mail(self):
        title, description = self._get_data()
        url = QtCore.QUrl("mailto:%s?subject=%s&body=%s" %
                          (EMAIL_ADDRESS, title, description))
        QtGui.QDesktopServices.openUrl(url)
        self.accept()

    @classmethod
    def report_bug(cls, parent, title='', description=''):
        dlg = cls(parent, title, description)
        return dlg.exec_() == dlg.Accepted

    @classmethod
    def crash_report(cls, parent, exception_info):
        dlg = cls(parent)
        dlg.ui.edit_title.setText(
            '[Unhandled exception] %s' % exception_info.splitlines()[-1])
        dlg.ui.edit_desc.setPlainText('``` python\n%s\n```' %
                                      exception_info.lstrip())
        dlg.ui.cb_include_sys_info.setChecked(True)
        dlg.ui.cb_include_sys_info.hide()
        dlg.exec_()

    def get_system_infos(self):
        return '\n'.join([
            '- Operating System: %s' % versions.get_versions()['system'],
            '- HackEdit: %s' % __version__,
            '- Python: %s (%dbits)' % (
                platform.python_version(), 64 if sys.maxsize > 2**32 else 32),
            '- Qt: %s' % QtCore.QT_VERSION_STR,
            '- PyQt: %s' % QtCore.PYQT_VERSION_STR,
        ])

    def get_application_log(self):
        with open(logger.get_path(), 'r') as f:
            return f.read()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    DlgReportBug.report_bug(None)
