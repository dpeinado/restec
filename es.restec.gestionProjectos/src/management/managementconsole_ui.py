# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'managementconsole.ui'
#
# Created: Mon Oct 22 14:08:43 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(925, 591)
        self.tree = QtGui.QTreeWidget(Dialog)
        self.tree.setGeometry(QtCore.QRect(20, 10, 871, 461))
        self.tree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tree.setColumnCount(2)
        self.tree.setObjectName(_fromUtf8("tree"))
        self.tree.headerItem().setText(0, _fromUtf8("1"))
        self.tree.headerItem().setText(1, _fromUtf8("2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

