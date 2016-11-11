#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QAbstractItemView

from ui_main import Ui_Form

R_IP, R_MAC, R_STATUS = range(3)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_refresh.clicked.connect(self.btn_refresh_clicked)
        self.ui.tbl_hosts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tbl_hosts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tbl_hosts.verticalHeader().setVisible(False)

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

    def get_live_hosts(self):
        (s_code, s_out) = subprocess.getstatusoutput("arp-scan --interface=wlp2s0 192.168.1.1/24")

        if s_code == 0:
            hosts = self.pat_arp.findall(s_out)
            self.populate_model(hosts)
            print(hosts)

        else:
            QMessageBox.critical(self, "Netshut", "Code : " + str(s_out))

    def populate_model(self, hosts):
        model = QStandardItemModel(0, 3, self)
        model.setHeaderData(R_IP, Qt.Horizontal, "IP Address")
        model.setHeaderData(R_MAC, Qt.Horizontal, "MAC Address")
        model.setHeaderData(R_STATUS, Qt.Horizontal, "Status")
        for host in hosts:
            model.insertRow(0)
            model.setData(model.index(0, R_IP), host[0])
            model.setData(model.index(0, R_MAC), host[1])
            model.setData(model.index(0, R_STATUS), "Up")

        self.ui.tbl_hosts.setModel(model)
        self.ui.tbl_hosts.resizeColumnsToContents()

    def btn_refresh_clicked(self):
        self.get_live_hosts()


def main():
    os.environ["QT_STYLE_OVERRIDE"] = "breeze"
    app = QApplication(sys.argv)

    w = MainWidget()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
