# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/about.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlg_about(object):
    def setupUi(self, dlg_about):
        dlg_about.setObjectName("dlg_about")
        dlg_about.resize(461, 343)
        self.verticalLayout = QtWidgets.QVBoxLayout(dlg_about)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(dlg_about)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(dlg_about)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(dlg_about)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlg_about)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dlg_about)
        self.buttonBox.accepted.connect(dlg_about.accept)
        self.buttonBox.rejected.connect(dlg_about.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_about)

    def retranslateUi(self, dlg_about):
        _translate = QtCore.QCoreApplication.translate
        dlg_about.setWindowTitle(_translate("dlg_about", "About"))
        self.label.setText(_translate("dlg_about", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">NetShut - Perfect tool to monitor you lan</span></p></body></html>"))
        self.label_2.setText(_translate("dlg_about", "<html><head/><body><p>By Ilyes Kechidi</p><p>&lt;ilyes.spd@gmail.com&gt;</p></body></html>"))
        self.label_3.setText(_translate("dlg_about", "Copyright (C) 2016 Ilyes Kechidi"))

