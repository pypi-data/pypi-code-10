# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/leap/bitmask/gui/ui/login.ui'
#
# Created: Mon Aug 24 15:15:53 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LoginWidget(object):
    def setupUi(self, LoginWidget):
        LoginWidget.setObjectName("LoginWidget")
        LoginWidget.resize(468, 363)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginWidget.sizePolicy().hasHeightForWidth())
        LoginWidget.setSizePolicy(sizePolicy)
        LoginWidget.setMinimumSize(QtCore.QSize(0, 0))
        LoginWidget.setStyleSheet("")
        self.gridLayout = QtGui.QGridLayout(LoginWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(12, 0, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.login_widget = QtGui.QWidget(LoginWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_widget.sizePolicy().hasHeightForWidth())
        self.login_widget.setSizePolicy(sizePolicy)
        self.login_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.login_widget.setObjectName("login_widget")
        self.gridLayout_4 = QtGui.QGridLayout(self.login_widget)
        self.gridLayout_4.setContentsMargins(-1, -1, 24, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btnLogin = QtGui.QPushButton(self.login_widget)
        self.btnLogin.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLogin.sizePolicy().hasHeightForWidth())
        self.btnLogin.setSizePolicy(sizePolicy)
        self.btnLogin.setObjectName("btnLogin")
        self.gridLayout_4.addWidget(self.btnLogin, 3, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.chkRemember = QtGui.QCheckBox(self.login_widget)
        self.chkRemember.setObjectName("chkRemember")
        self.verticalLayout.addWidget(self.chkRemember)
        self.lblStatus = QtGui.QLabel(self.login_widget)
        self.lblStatus.setText("")
        self.lblStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lblStatus.setWordWrap(True)
        self.lblStatus.setObjectName("lblStatus")
        self.verticalLayout.addWidget(self.lblStatus)
        self.gridLayout_4.addLayout(self.verticalLayout, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.login_widget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)
        self.lnUser = QtGui.QLineEdit(self.login_widget)
        self.lnUser.setObjectName("lnUser")
        self.gridLayout_4.addWidget(self.lnUser, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.login_widget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 1, 0, 1, 1)
        self.lnPassword = QtGui.QLineEdit(self.login_widget)
        self.lnPassword.setInputMask("")
        self.lnPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lnPassword.setObjectName("lnPassword")
        self.gridLayout_4.addWidget(self.lnPassword, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.login_widget, 2, 2, 1, 2)
        self.label = QtGui.QLabel(LoginWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 800))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/black/32/user.png"))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setMargin(0)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 1, 2, 1)
        self.clblErrorMsg = ClickableLabel(LoginWidget)
        self.clblErrorMsg.setMinimumSize(QtCore.QSize(0, 50))
        self.clblErrorMsg.setStyleSheet("background-color: rgb(255, 127, 114);")
        self.clblErrorMsg.setText("")
        self.clblErrorMsg.setAlignment(QtCore.Qt.AlignCenter)
        self.clblErrorMsg.setObjectName("clblErrorMsg")
        self.gridLayout.addWidget(self.clblErrorMsg, 0, 0, 1, 4)
        self.logged_widget = QtGui.QWidget(LoginWidget)
        self.logged_widget.setObjectName("logged_widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.logged_widget)
        self.horizontalLayout.setContentsMargins(-1, 0, 25, 18)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblUser = QtGui.QLabel(self.logged_widget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setWeight(75)
        font.setBold(True)
        self.lblUser.setFont(font)
        self.lblUser.setObjectName("lblUser")
        self.horizontalLayout.addWidget(self.lblUser)
        spacerItem1 = QtGui.QSpacerItem(24, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnLogout = QtGui.QPushButton(self.logged_widget)
        self.btnLogout.setObjectName("btnLogout")
        self.horizontalLayout.addWidget(self.btnLogout)
        spacerItem2 = QtGui.QSpacerItem(24, 24, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addWidget(self.logged_widget, 3, 2, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(0, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)

        self.retranslateUi(LoginWidget)
        QtCore.QObject.connect(self.lnPassword, QtCore.SIGNAL("returnPressed()"), self.btnLogin.click)
        QtCore.QObject.connect(self.lnUser, QtCore.SIGNAL("returnPressed()"), self.lnPassword.setFocus)
        QtCore.QMetaObject.connectSlotsByName(LoginWidget)
        LoginWidget.setTabOrder(self.lnUser, self.lnPassword)
        LoginWidget.setTabOrder(self.lnPassword, self.chkRemember)
        LoginWidget.setTabOrder(self.chkRemember, self.btnLogin)
        LoginWidget.setTabOrder(self.btnLogin, self.btnLogout)

    def retranslateUi(self, LoginWidget):
        LoginWidget.setWindowTitle(QtGui.QApplication.translate("LoginWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLogin.setText(QtGui.QApplication.translate("LoginWidget", "Log In", None, QtGui.QApplication.UnicodeUTF8))
        self.chkRemember.setText(QtGui.QApplication.translate("LoginWidget", "Remember username and password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LoginWidget", "<b>Username:</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("LoginWidget", "<b>Password:</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.lblUser.setText(QtGui.QApplication.translate("LoginWidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLogout.setText(QtGui.QApplication.translate("LoginWidget", "Logout", None, QtGui.QApplication.UnicodeUTF8))

from clickablelabel import ClickableLabel
import icons_rc
