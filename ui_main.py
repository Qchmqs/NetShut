# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 480)
        Form.setMinimumSize(QtCore.QSize(640, 480))
        Form.setMaximumSize(QtCore.QSize(640, 480))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_refresh = QtWidgets.QPushButton(Form)
        self.btn_refresh.setObjectName("btn_refresh")
        self.horizontalLayout.addWidget(self.btn_refresh)
        self.btn_cut = QtWidgets.QPushButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/lan-disconnect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_cut.setIcon(icon)
        self.btn_cut.setObjectName("btn_cut")
        self.horizontalLayout.addWidget(self.btn_cut)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tbl_hosts = QtWidgets.QTableWidget(Form)
        self.tbl_hosts.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tbl_hosts.setShowGrid(False)
        self.tbl_hosts.setObjectName("tbl_hosts")
        self.tbl_hosts.setColumnCount(0)
        self.tbl_hosts.setRowCount(0)
        self.tbl_hosts.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tbl_hosts)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "NetShut"))
        self.btn_refresh.setText(_translate("Form", "Scan"))
        self.btn_cut.setText(_translate("Form", "Cut All"))
        self.pushButton.setText(_translate("Form", "PushButton"))

