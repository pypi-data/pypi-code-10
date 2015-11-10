# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/dlg_report_bug.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(601, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.edit_title = QtWidgets.QLineEdit(Dialog)
        self.edit_title.setObjectName("edit_title")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.edit_title)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.edit_desc = QtWidgets.QPlainTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.edit_desc.sizePolicy().hasHeightForWidth())
        self.edit_desc.setSizePolicy(sizePolicy)
        self.edit_desc.setObjectName("edit_desc")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.edit_desc)
        self.cb_include_sys_info = QtWidgets.QCheckBox(Dialog)
        self.cb_include_sys_info.setChecked(True)
        self.cb_include_sys_info.setObjectName("cb_include_sys_info")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cb_include_sys_info)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.bt_submit = QtWidgets.QPushButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/GitHub-Mark-32px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_submit.setIcon(icon)
        self.bt_submit.setObjectName("bt_submit")
        self.horizontalLayout.addWidget(self.bt_submit)
        self.bt_send_mail = QtWidgets.QPushButton(Dialog)
        icon = QtGui.QIcon.fromTheme("mail-send")
        self.bt_send_mail.setIcon(icon)
        self.bt_send_mail.setObjectName("bt_send_mail")
        self.horizontalLayout.addWidget(self.bt_send_mail)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Report a bug"))
        self.label.setText(_translate("Dialog", "Title:"))
        self.edit_title.setToolTip(_translate("Dialog", "<html><head/><body><p>Bug report title</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Description:"))
        self.edit_desc.setToolTip(_translate("Dialog", "<html><head/><body><p>Use <span style=\" font-weight:600;\">markdown</span> to format text and make sure to mention the context of the issue and the <span style=\" font-weight:600;\">steps to reproduce</span>!</p></body></html>"))
        self.cb_include_sys_info.setToolTip(_translate("Dialog", "Enable/Disable sending system infos (OS name, versions,...)"))
        self.cb_include_sys_info.setText(_translate("Dialog", "Include system informations"))
        self.bt_submit.setToolTip(_translate("Dialog", "<html><head/><body><p>Submit bug report on our issue tracker on Github.</p><p>Note that you\'ll need a github account to actually submit the issue.</p></body></html>"))
        self.bt_submit.setText(_translate("Dialog", "Submit on github"))
        self.bt_send_mail.setToolTip(_translate("Dialog", "<html><head/><body><p>Send an email with the bug report directly to the main author.</p></body></html>"))
        self.bt_send_mail.setText(_translate("Dialog", "Send an e-mail"))

from . import hackedit_rc
