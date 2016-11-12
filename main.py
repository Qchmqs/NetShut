#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtNetwork
import os
import re
import subprocess
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QAbstractItemView, QTableWidgetItem, QPushButton, qApp, \
    QMainWindow, QInputDialog

from ui_main import Ui_MainWindow

TABLE_COLUMN_COUNT = 4
R_IP, R_MAC, R_MAC_MAN, R_STATUS = range(TABLE_COLUMN_COUNT)

VERSION = 0.1
TITLE = "Netshut {}".format(VERSION)


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()

        # Compile Re's
        self.pat_arp = re.compile("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\S+)", re.MULTILINE)
        self.pat_gip = re.compile("inet\s(.+)\/")

        self._gw = self.get_gateway()
        self._iface = "wlp2s0"
        self._mac = ""
        self._ip = ""

        self.prompt_iface()
        self.get_ip()


        self.ui.lbl_gw.setText("<b>{}</b>".format(self._gw))
        self.ui.lbl_mac.setText("<b>{}</b>".format(self._mac))
        self.ui.lbl_ip.setText("<b>{}</b>".format(self._ip))

        # TODO Remove after ui complete
        self.populate_model([('192.168.1.1', '5c:f9:6a:23:7c:1a'), ('192.168.1.13', '00:2d:00:06:a0:2f'),
                             ('192.168.1.10', 'd0:6f:4a:61:9b:06'), ('192.168.1.11', '94:35:0a:ef:86:4d'),
                             ('192.168.1.12', '30:19:66:71:49:6f')])

    def initUi(self):
        self.ui.act_scan.triggered.connect(self.btn_refresh_clicked)
        self.ui.act_scan.setIcon(QIcon("img/scan.png"))
        self.ui.act_cut.setIcon(QIcon("img/lan-disconnect.png"))
        self.ui.tbl_hosts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tbl_hosts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tbl_hosts.verticalHeader().setVisible(False)
        self.ui.tbl_hosts.setColumnCount(TABLE_COLUMN_COUNT)
        self.ui.tbl_hosts.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Device Manufacturer", "Status"])
        self.ui.tbl_hosts.setColumnWidth(0, 100)
        self.ui.tbl_hosts.setColumnWidth(1, 150)
        self.ui.tbl_hosts.setColumnWidth(2, 240)
        self.ui.tbl_hosts.setShowGrid(False)

    def get_ip(self):
        (s_code, s_out) = subprocess.getstatusoutput("ip addr show {}".format(self._iface))
        self._ip = self.pat_gip.findall(s_out)[0]

    def prompt_iface(self):
        ifaces_names = []
        ifaces_macs = []
        ifaces = QtNetwork.QNetworkInterface.allInterfaces()
        for i in ifaces:
            ifaces_names.append(str(i.name()))
            ifaces_macs.append(str(i.hardwareAddress()))
        result, ok = QInputDialog.getItem(self, self.tr("Network Interfaces"), self.tr("Select your Interface:"),
                                          ifaces_names, 0, True)
        if ok:
            self._iface = result
            self._mac = ifaces_macs[ifaces_names.index(result)]
        else:
            QMessageBox.critical(self,TITLE,"You must select an interface card")
            exit()

    def gso(self, *args, **kwargs):
        # Get Status output
        p = subprocess.Popen(*args, **kwargs)
        stdout, stderr = p.communicate()
        return p.returncode, stdout, stderr

    def get_gateway(self):
        (s_code, s_out) = subprocess.getstatusoutput("ip route list")
        try:
            gw_ip = s_out.split("\n")[0].split(" ")[2]
        except IndexError:
            print("COULD NOT GET GATEWAY IP")
            exit()

        return gw_ip

    def get_live_hosts(self):

        (s_code, s_out) = subprocess.getstatusoutput("arp-scan --interface={} {}/24".format(self._iface, self._gw))

        if s_code == 0:
            hosts = self.pat_arp.findall(s_out)

            self.populate_model(hosts)

        else:
            QMessageBox.critical(self, TITLE, s_out)

    def populate_model(self, hosts):
        self.hosts = hosts
        self.ui.tbl_hosts.setRowCount(len(hosts))
        for i, host in enumerate(hosts):
            self.ui.tbl_hosts.setItem(i, R_IP, QTableWidgetItem(host[0]))
            self.ui.tbl_hosts.setItem(i, R_MAC, QTableWidgetItem(host[1]))
            self.ui.tbl_hosts.setItem(i, R_MAC_MAN, QTableWidgetItem("Unknown"))
            self.btn_cut = QPushButton("Cut")
            self.btn_cut.setIcon(QIcon("img/lan-connect.png"))
            self.btn_cut.clicked.connect(self.btn_cut_clicked)
            self.ui.tbl_hosts.setCellWidget(i, R_STATUS, self.btn_cut)

        self.set_device_man()

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

    def set_device_man(self):
        f = open("/usr/share/nmap/nmap-mac-prefixes")

        for line in f.readlines():
            for i, host in enumerate(self.hosts):
                mac = host[1].replace(":", "").upper()[:6]
                if line.startswith(mac):
                    self.ui.tbl_hosts.setItem(i, R_MAC_MAN, QTableWidgetItem(line[7:]))
                    break


def main():
    os.environ["QT_STYLE_OVERRIDE"] = "breeze"
    app = QApplication(sys.argv)

    w = MainWidget()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
