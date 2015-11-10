# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/work/hackedit/data/forms/dlg_add_boss_source.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(347, 116)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.edit_label = QtWidgets.QLineEdit(Dialog)
        self.edit_label.setObjectName("edit_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.edit_label)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.edit_url = QtWidgets.QLineEdit(Dialog)
        self.edit_url.setObjectName("edit_url")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.edit_url)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add source"))
        self.label.setText(_translate("Dialog", "Label:"))
        self.edit_label.setToolTip(_translate("Dialog", "Give a meaningfull name to this source so that you can recognize it."))
        self.label_2.setText(_translate("Dialog", "URL"))
        self.edit_url.setToolTip(_translate("Dialog", "<html><head/><body><p>URL of the template repository. </p><p><br/></p><p>Boss supports both local and remote (git) template repositories.</p></body></html>"))

