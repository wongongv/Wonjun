# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'check.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(331, 131)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 70, 311, 52))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox = QtGui.QCheckBox(self.widget)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(self.widget)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout.addWidget(self.checkBox_2, 0, 1, 1, 1)
        self.checkBox_4 = QtGui.QCheckBox(self.widget)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.gridLayout.addWidget(self.checkBox_4, 0, 2, 1, 1)
        self.checkBox_3 = QtGui.QCheckBox(self.widget)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.gridLayout.addWidget(self.checkBox_3, 1, 0, 1, 1)
        self.checkBox_5 = QtGui.QCheckBox(self.widget)
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.gridLayout.addWidget(self.checkBox_5, 1, 1, 1, 1)
        self.checkBox_6 = QtGui.QCheckBox(self.widget)
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.gridLayout.addWidget(self.checkBox_6, 1, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.checkBox.setText(_translate("Form", "dd", None))
        self.checkBox_2.setText(_translate("Form", "CheckBox", None))
        self.checkBox_4.setText(_translate("Form", "CheckBox", None))
        self.checkBox_3.setText(_translate("Form", "CheckBox", None))
        self.checkBox_5.setText(_translate("Form", "CheckBox", None))
        self.checkBox_6.setText(_translate("Form", "CheckBox", None))

