# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchStruct.ui'
#
# Created: Tue Feb 21 20:08:27 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_Search_Structure(object):

    def setupUi(self, Search_Structure):
        Search_Structure.setObjectName(_fromUtf8("Search_Structure"))
        Search_Structure.resize(404, 385)
        Search_Structure.setWindowTitle(
            QtGui.QApplication.translate(
                "Search_Structure",
                "Search for a Structure",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_2 = QtGui.QGridLayout(Search_Structure)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.dialog_search_structure_buttonbox = QtGui.QDialogButtonBox(
            Search_Structure)
        self.dialog_search_structure_buttonbox.setOrientation(
            QtCore.Qt.Horizontal)
        self.dialog_search_structure_buttonbox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.dialog_search_structure_buttonbox.setObjectName(
            _fromUtf8("dialog_search_structure_buttonbox"))
        self.gridLayout_2.addWidget(
            self.dialog_search_structure_buttonbox,
            1,
            0,
            1,
            1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tabWidget = QtGui.QTabWidget(Search_Structure)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.search_tab_structure = QtGui.QWidget()
        self.search_tab_structure.setObjectName(
            _fromUtf8("search_tab_structure"))
        self.layoutWidget = QtGui.QWidget(self.search_tab_structure)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 410, 250))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.searchWidget_tree = QtGui.QTreeWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.searchWidget_tree.sizePolicy().hasHeightForWidth())
        self.searchWidget_tree.setSizePolicy(sizePolicy)
        self.searchWidget_tree.setBaseSize(QtCore.QSize(0, 0))
        self.searchWidget_tree.setEditTriggers(
            QtGui.QAbstractItemView.DoubleClicked | QtGui.QAbstractItemView.EditKeyPressed | QtGui.QAbstractItemView.SelectedClicked)
        self.searchWidget_tree.setObjectName(_fromUtf8("searchWidget_tree"))
        self.searchWidget_tree.headerItem().setText(0, _fromUtf8("1"))
        self.searchWidget_tree.header().setVisible(False)
        self.gridLayout.addWidget(self.searchWidget_tree, 3, 0, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "Structure name/Filter :",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_filter = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_filter.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_filter.setObjectName(_fromUtf8("lineEdit_filter"))
        self.gridLayout.addWidget(self.lineEdit_filter, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "Registered allocators :",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.search_tab_structure, _fromUtf8(""))
        self.search_tab_value = QtGui.QWidget()
        self.search_tab_value.setObjectName(_fromUtf8("search_tab_value"))
        self.gridLayoutWidget_3 = QtGui.QWidget(self.search_tab_value)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 381, 61))
        self.gridLayoutWidget_3.setObjectName(_fromUtf8("gridLayoutWidget_3"))
        self.gridLayout_5 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_3.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "RegExp value :",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_5.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit_regexp = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_regexp.setObjectName(_fromUtf8("lineEdit_regexp"))
        self.gridLayout_5.addWidget(self.lineEdit_regexp, 1, 0, 1, 1)
        self.tabWidget.addTab(self.search_tab_value, _fromUtf8(""))
        self.search_tab_classics = QtGui.QWidget()
        self.search_tab_classics.setObjectName(
            _fromUtf8("search_tab_classics"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.search_tab_classics)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(2, 0, 371, 301))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.checkBox_email = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_email.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "Email",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_email.setObjectName(_fromUtf8("checkBox_email"))
        self.gridLayout_4.addWidget(self.checkBox_email, 0, 0, 1, 1)
        self.toolButton_email = QtGui.QToolButton(self.gridLayoutWidget_2)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 119, 70))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 193, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ToolTipText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Midlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 193, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ToolTipText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Midlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ToolTipText,
            brush)
        self.toolButton_email.setPalette(palette)
        self.toolButton_email.setAutoFillBackground(True)
        self.toolButton_email.setText(_fromUtf8(""))
        self.toolButton_email.setObjectName(_fromUtf8("toolButton_email"))
        self.gridLayout_4.addWidget(self.toolButton_email, 0, 1, 1, 1)
        self.checkBox_url = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_url.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "URL",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_url.setObjectName(_fromUtf8("checkBox_url"))
        self.gridLayout_4.addWidget(self.checkBox_url, 1, 0, 1, 1)
        self.checkBox_winfile = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_winfile.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "Windows Filenames",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_winfile.setObjectName(_fromUtf8("checkBox_winfile"))
        self.gridLayout_4.addWidget(self.checkBox_winfile, 2, 0, 1, 1)
        self.checkBox_ipv4 = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_ipv4.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "IPv4",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_ipv4.setObjectName(_fromUtf8("checkBox_ipv4"))
        self.gridLayout_4.addWidget(self.checkBox_ipv4, 3, 0, 1, 1)
        self.toolButton_url = QtGui.QToolButton(self.gridLayoutWidget_2)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 119, 70))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 193, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ToolTipText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Midlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 193, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ToolTipText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Midlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ToolTipText,
            brush)
        self.toolButton_url.setPalette(palette)
        self.toolButton_url.setAutoFillBackground(True)
        self.toolButton_url.setText(_fromUtf8(""))
        self.toolButton_url.setObjectName(_fromUtf8("toolButton_url"))
        self.gridLayout_4.addWidget(self.toolButton_url, 1, 1, 1, 1)
        self.toolButton_winfile = QtGui.QToolButton(self.gridLayoutWidget_2)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 119, 70))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 193, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ToolTipText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Midlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 193, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ToolTipText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Midlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ToolTipText,
            brush)
        self.toolButton_winfile.setPalette(palette)
        self.toolButton_winfile.setAutoFillBackground(True)
        self.toolButton_winfile.setText(_fromUtf8(""))
        self.toolButton_winfile.setObjectName(_fromUtf8("toolButton_winfile"))
        self.gridLayout_4.addWidget(self.toolButton_winfile, 2, 1, 1, 1)
        self.toolButton_ipv4 = QtGui.QToolButton(self.gridLayoutWidget_2)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 119, 70))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 193, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.ToolTipText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Midlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 193, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.ToolTipText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.WindowText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 189, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Midlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 87, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.BrightText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 65, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ButtonText,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Highlight,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 131, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ToolTipBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.ToolTipText,
            brush)
        self.toolButton_ipv4.setPalette(palette)
        self.toolButton_ipv4.setAutoFillBackground(True)
        self.toolButton_ipv4.setText(_fromUtf8(""))
        self.toolButton_ipv4.setObjectName(_fromUtf8("toolButton_ipv4"))
        self.gridLayout_4.addWidget(self.toolButton_ipv4, 3, 1, 1, 1)
        self.checkBox_ipv6 = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_ipv6.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "IPv6",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_ipv6.setObjectName(_fromUtf8("checkBox_ipv6"))
        self.gridLayout_4.addWidget(self.checkBox_ipv6, 4, 0, 1, 1)
        self.toolButton_ipv6 = QtGui.QToolButton(self.gridLayoutWidget_2)
        self.toolButton_ipv6.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "...",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.toolButton_ipv6.setObjectName(_fromUtf8("toolButton_ipv6"))
        self.gridLayout_4.addWidget(self.toolButton_ipv6, 4, 1, 1, 1)
        self.checkBox_sql = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_sql.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "SQL Statements",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_sql.setObjectName(_fromUtf8("checkBox_sql"))
        self.gridLayout_4.addWidget(self.checkBox_sql, 5, 0, 1, 1)
        self.toolButton_sql = QtGui.QToolButton(self.gridLayoutWidget_2)
        self.toolButton_sql.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "...",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.toolButton_sql.setObjectName(_fromUtf8("toolButton_sql"))
        self.gridLayout_4.addWidget(self.toolButton_sql, 5, 1, 1, 1)
        self.checkBox_cc = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_cc.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "Credit Cards {VISA,Mastercard,Amex}",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_cc.setObjectName(_fromUtf8("checkBox_cc"))
        self.gridLayout_4.addWidget(self.checkBox_cc, 6, 0, 1, 1)
        self.toolButton_cc = QtGui.QToolButton(self.gridLayoutWidget_2)
        self.toolButton_cc.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "...",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.toolButton_cc.setObjectName(_fromUtf8("toolButton_cc"))
        self.gridLayout_4.addWidget(self.toolButton_cc, 6, 1, 1, 1)
        self.checkBox_ssn = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_ssn.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "SSN (North America)",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_ssn.setObjectName(_fromUtf8("checkBox_ssn"))
        self.gridLayout_4.addWidget(self.checkBox_ssn, 7, 0, 1, 1)
        self.toolButton_ssn = QtGui.QToolButton(self.gridLayoutWidget_2)
        self.toolButton_ssn.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "...",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.toolButton_ssn.setObjectName(_fromUtf8("toolButton_ssn"))
        self.gridLayout_4.addWidget(self.toolButton_ssn, 7, 1, 1, 1)
        self.checkBox_guid = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_guid.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "GUID/UUID",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_guid.setObjectName(_fromUtf8("checkBox_guid"))
        self.gridLayout_4.addWidget(self.checkBox_guid, 8, 0, 1, 1)
        self.toolButton_guid = QtGui.QToolButton(self.gridLayoutWidget_2)
        self.toolButton_guid.setText(
            QtGui.QApplication.translate(
                "Search_Structure",
                "...",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.toolButton_guid.setObjectName(_fromUtf8("toolButton_guid"))
        self.gridLayout_4.addWidget(self.toolButton_guid, 8, 1, 1, 1)
        self.tabWidget.addTab(self.search_tab_classics, _fromUtf8(""))
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.retranslateUi(Search_Structure)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(
            self.dialog_search_structure_buttonbox,
            QtCore.SIGNAL(
                _fromUtf8("accepted()")),
            Search_Structure.accept)
        QtCore.QObject.connect(
            self.dialog_search_structure_buttonbox,
            QtCore.SIGNAL(
                _fromUtf8("rejected()")),
            Search_Structure.reject)
        QtCore.QMetaObject.connectSlotsByName(Search_Structure)

    def retranslateUi(self, Search_Structure):
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(
                self.search_tab_structure),
            QtGui.QApplication.translate(
                "Search_Structure",
                "Structure...",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(
                self.search_tab_value),
            QtGui.QApplication.translate(
                "Search_Structure",
                "Value...",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(
                self.search_tab_classics),
            QtGui.QApplication.translate(
                "Search_Structure",
                "Classics",
                None,
                QtGui.QApplication.UnicodeUTF8))
