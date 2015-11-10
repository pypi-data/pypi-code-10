# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/task_widget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(428, 98)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.group = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group.sizePolicy().hasHeightForWidth())
        self.group.setSizePolicy(sizePolicy)
        self.group.setObjectName("group")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.group)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbar_progress = QtWidgets.QProgressBar(self.group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbar_progress.sizePolicy().hasHeightForWidth())
        self.pbar_progress.setSizePolicy(sizePolicy)
        self.pbar_progress.setMinimumSize(QtCore.QSize(0, 0))
        self.pbar_progress.setMaximum(0)
        self.pbar_progress.setProperty("value", -1)
        self.pbar_progress.setTextVisible(True)
        self.pbar_progress.setObjectName("pbar_progress")
        self.horizontalLayout.addWidget(self.pbar_progress)
        self.bt_cancel = QtWidgets.QToolButton(self.group)
        icon = QtGui.QIcon.fromTheme("process-stop")
        self.bt_cancel.setIcon(icon)
        self.bt_cancel.setObjectName("bt_cancel")
        self.horizontalLayout.addWidget(self.bt_cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.lbl_description = QtWidgets.QLabel(self.group)
        self.lbl_description.setObjectName("lbl_description")
        self.verticalLayout_2.addWidget(self.lbl_description)
        self.verticalLayout.addWidget(self.group)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.group.setTitle(_translate("Form", "Name"))
        self.bt_cancel.setToolTip(_translate("Form", "Cancel operation"))
        self.bt_cancel.setText(_translate("Form", "..."))
        self.lbl_description.setText(_translate("Form", "Description"))

