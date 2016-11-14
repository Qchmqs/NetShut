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
        dlg_about.setWindowModality(QtCore.Qt.NonModal)
        dlg_about.resize(531, 305)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlg_about.sizePolicy().hasHeightForWidth())
        dlg_about.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(dlg_about)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(dlg_about)
        self.label.setLineWidth(1)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 4)
        self.label_4 = QtWidgets.QLabel(dlg_about)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../img/icon.png"))
        self.label_4.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.lbl_version = QtWidgets.QLabel(dlg_about)
        self.lbl_version.setObjectName("lbl_version")
        self.gridLayout.addWidget(self.lbl_version, 2, 0, 1, 3)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlg_about)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 5)
        self.label_2 = QtWidgets.QLabel(dlg_about)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 5)
        self.lbl_cr = QtWidgets.QLabel(dlg_about)
        self.lbl_cr.setObjectName("lbl_cr")
        self.gridLayout.addWidget(self.lbl_cr, 4, 0, 1, 5)
        self.lbl_name = QtWidgets.QLabel(dlg_about)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_name.sizePolicy().hasHeightForWidth())
        self.lbl_name.setSizePolicy(sizePolicy)
        self.lbl_name.setObjectName("lbl_name")
        self.gridLayout.addWidget(self.lbl_name, 3, 0, 1, 5)

        self.retranslateUi(dlg_about)
        self.buttonBox.accepted.connect(dlg_about.accept)
        self.buttonBox.rejected.connect(dlg_about.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_about)

    def retranslateUi(self, dlg_about):
        _translate = QtCore.QCoreApplication.translate
        dlg_about.setWindowTitle(_translate("dlg_about", "About"))
        self.label.setText(_translate("dlg_about", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">NetShut</span></p><p><span style=\"\">A Network Utility to cut-off connection from any live host on your LAN</span></p></body></html>"))
        self.lbl_version.setText(_translate("dlg_about", "Version : 0.1"))
        self.label_2.setText(_translate("dlg_about", "Licensed under the MIT License"))
        self.lbl_cr.setText(_translate("dlg_about", "Copyright (C) 2016 Ilyes Kechidi"))
        self.lbl_name.setText(_translate("dlg_about", "<html><head/><body><p>By Ilyes Kechidi &lt;ilyes.spd@gmail.com&gt;</p></body></html>"))

