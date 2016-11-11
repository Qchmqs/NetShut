#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QAbstractItemView, QTableWidgetItem, QPushButton, qApp

from ui_main import Ui_Form

R_IP, R_MAC, R_STATUS = range(3)

VERSION = 0.1
TITLE = "Netshut {}".format(VERSION)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_refresh.clicked.connect(self.btn_refresh_clicked)
        self.ui.btn_refresh.setIcon(QIcon("img/scan.png"))
        self.ui.tbl_hosts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tbl_hosts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tbl_hosts.verticalHeader().setVisible(False)
        self.ui.tbl_hosts.setColumnCount(3)
        self.ui.tbl_hosts.setHorizontalHeaderLabels(["IP Address","MAC Address","Status"])
        self.ui.tbl_hosts.setColumnWidth(0,200)
        self.ui.tbl_hosts.setColumnWidth(1,200)
        self.ui.tbl_hosts.setShowGrid(False)

        self._gw = self.get_gateway()
        self._iface = "wlp2s0"

        # TODO Remove after ui complete
        self.populate_model([('192.168.1.1', '5c:f9:6a:23:7c:1a'), ('192.168.1.13', '00:2d:00:06:a0:2f'),
                             ('192.168.1.10', 'd0:6f:4a:61:9b:06'), ('192.168.1.11', '94:35:0a:ef:86:4d'),
                             ('192.168.1.12', '30:19:66:71:49:6f')])

        # Compile Re's
        self.pat_arp = re.compile("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\S+)", re.MULTILINE)

    def gso(self, *args, **kwargs):
        # Get Status output
        p = subprocess.Popen(*args, **kwargs)
        stdout, stderr = p.communicate()
        return p.returncode, stdout, stderr


    def get_gateway(self):
        (s_code, s_out) = subprocess.getstatusoutput("ip route list")
        gw_ip = s_out.split("\n")[0].split(" ")[2]
        return gw_ip


    def get_live_hosts(self):
        (s_code, s_out) = subprocess.getstatusoutput("arp-scan --interface={} {}/24".format(self._iface,self._gw))

        if s_code == 0:
            hosts = self.pat_arp.findall(s_out)

            self.populate_model(hosts)

        else:
            QMessageBox.critical(self, TITLE, s_out)

    def populate_model(self,hosts):
        self.ui.tbl_hosts.setRowCount(len(hosts))
        for i,host in enumerate(hosts):
            self.ui.tbl_hosts.setItem(i,R_IP,QTableWidgetItem(host[0]))
            self.ui.tbl_hosts.setItem(i,R_MAC,QTableWidgetItem(host[1]))
            self.btn_cut = QPushButton("Cut")
            self.btn_cut.setIcon(QIcon("img/lan-connect.png"))
            self.btn_cut.clicked.connect(self.btn_cut_clicked)
            self.ui.tbl_hosts.setCellWidget(i,R_STATUS,self.btn_cut)

    def btn_refresh_clicked(self):
        self.get_live_hosts()

    def btn_cut_clicked(self):
        button = qApp.focusWidget()

        # or button = self.sender()
        index = self.ui.tbl_hosts.indexAt(button.pos())

        if index.isValid():
            if button.text().startswith("C"):
                button.setText("Uncut")
                button.setIcon(QIcon("img/lan-disconnect.png"))
            else:
                button.setText("Cut")
                button.setIcon(QIcon("img/lan-connect.png"))
            print(index.row(), index.column())

def main():
    os.environ["QT_STYLE_OVERRIDE"] = "breeze"
    app = QApplication(sys.argv)

    w = MainWidget()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
