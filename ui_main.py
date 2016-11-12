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
        Form.setStyleSheet("QPushButton {\n"
"    background: rgb(255, 37, 66);\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background: rgb(67, 66, 65);\n"
"    color: rgb(218, 218, 203);\n"
"}")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_refresh = QtWidgets.QPushButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/scan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_refresh.setIcon(icon)
        self.btn_refresh.setObjectName("btn_refresh")
        self.horizontalLayout.addWidget(self.btn_refresh)
        self.btn_cut_all = QtWidgets.QPushButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../img/lan-disconnect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_cut_all.setIcon(icon1)
        self.btn_cut_all.setObjectName("btn_cut_all")
        self.horizontalLayout.addWidget(self.btn_cut_all)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
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
        self.btn_cut_all.setText(_translate("Form", "Cut All"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">192.168.1.14</span></p></body></html>"))
        self.label_10.setText(_translate("Form", "MAC Address :"))
        self.label_5.setText(_translate("Form", "IP Address:"))
        self.label_9.setText(_translate("Form", "Gateway Address"))
        self.label_6.setText(_translate("Form", "<b>192.168.1.1</b>"))
        self.label_7.setText(_translate("Form", "<b>5c:f9:6a:23:7c:1a</b>"))

