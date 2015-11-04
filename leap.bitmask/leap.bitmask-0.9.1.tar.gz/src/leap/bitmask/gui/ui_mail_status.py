# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/leap/bitmask/gui/ui/mail_status.ui'
#
# Created: Tue Nov  3 10:23:28 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MailStatusWidget(object):
    def setupUi(self, MailStatusWidget):
        MailStatusWidget.setObjectName("MailStatusWidget")
        MailStatusWidget.resize(417, 185)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MailStatusWidget.sizePolicy().hasHeightForWidth())
        MailStatusWidget.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(MailStatusWidget)
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 1, 1)
        self.label_4 = QtGui.QLabel(MailStatusWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 1, 1, 1)
        self.lblMailStatusIcon = QtGui.QLabel(MailStatusWidget)
        self.lblMailStatusIcon.setMaximumSize(QtCore.QSize(24, 24))
        self.lblMailStatusIcon.setText("")
        self.lblMailStatusIcon.setPixmap(QtGui.QPixmap(":/images/black/22/off.png"))
        self.lblMailStatusIcon.setScaledContents(True)
        self.lblMailStatusIcon.setObjectName("lblMailStatusIcon")
        self.gridLayout_3.addWidget(self.lblMailStatusIcon, 0, 4, 1, 1)
        self.lblMailReadyHelp = QtGui.QLabel(MailStatusWidget)
        self.lblMailReadyHelp.setAutoFillBackground(False)
        self.lblMailReadyHelp.setStyleSheet("background-color: #e0efd8;\n"
"padding: 10px;")
        self.lblMailReadyHelp.setFrameShape(QtGui.QFrame.NoFrame)
        self.lblMailReadyHelp.setFrameShadow(QtGui.QFrame.Plain)
        self.lblMailReadyHelp.setLineWidth(0)
        self.lblMailReadyHelp.setTextFormat(QtCore.Qt.AutoText)
        self.lblMailReadyHelp.setScaledContents(False)
        self.lblMailReadyHelp.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblMailReadyHelp.setWordWrap(True)
        self.lblMailReadyHelp.setMargin(0)
        self.lblMailReadyHelp.setIndent(-1)
        self.lblMailReadyHelp.setObjectName("lblMailReadyHelp")
        self.gridLayout_3.addWidget(self.lblMailReadyHelp, 3, 1, 1, 2)
        self.label = QtGui.QLabel(MailStatusWidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/black/32/email.png"))
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.lblMailStatus = QtGui.QLabel(MailStatusWidget)
        self.lblMailStatus.setStyleSheet("color: rgb(80, 80, 80);")
        self.lblMailStatus.setObjectName("lblMailStatus")
        self.gridLayout_3.addWidget(self.lblMailStatus, 2, 1, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.retranslateUi(MailStatusWidget)
        QtCore.QMetaObject.connectSlotsByName(MailStatusWidget)

    def retranslateUi(self, MailStatusWidget):
        MailStatusWidget.setWindowTitle(QtGui.QApplication.translate("MailStatusWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MailStatusWidget", "Email", None, QtGui.QApplication.UnicodeUTF8))
        self.lblMailReadyHelp.setText(QtGui.QApplication.translate("MailStatusWidget", "Congratulations! You are ready to use Bitmask to encrypt your email. Go to <a href=\"https://bitmask.net/en/help/email\">https://bitmask.net/en/help/email</a> for instructions on how to set up your mail client.", None, QtGui.QApplication.UnicodeUTF8))
        self.lblMailStatus.setText(QtGui.QApplication.translate("MailStatusWidget", "You must login to use encrypted email.", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
