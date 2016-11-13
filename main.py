#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import subprocess
import sys

from PyQt5 import QtNetwork
from PyQt5.QtCore import QThread, pyqtSignal, QSettings, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QAbstractItemView, QTableWidgetItem, QPushButton, qApp, \
    QMainWindow, QInputDialog, QDesktopWidget, QActionGroup
from about import AboutDialog

from ui.main_ui import Ui_MainWindow

TABLE_COLUMN_COUNT = 4
R_IP, R_MAC, R_MAC_MAN, R_STATUS = range(TABLE_COLUMN_COUNT)

VERSION = 0.1
TITLE = "Netshut {}".format(VERSION)


class CommandThread(QThread):
    results = pyqtSignal(object, object)

    def __init__(self, cmd, parent=None):
        super().__init__(parent)
        self.cmd = cmd

    def run(self):
        (s_code, s_out) = subprocess.getstatusoutput(self.cmd)
        self.results.emit(s_code, s_out)


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.settings = QSettings("IK", "Netshut")
        self.th = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        self.center()


        if int(self.settings.value("toolbar_show", Qt.ToolButtonIconOnly)) == Qt.ToolButtonIconOnly:
            self.ui.actionShow_Icons.setChecked(True)
            self.ui.toolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        else:
            self.ui.actionShow_Icons_Text.setChecked(True)
            self.ui.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Compile Re's
        self.pat_arp = re.compile("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\S+)", re.MULTILINE)
        self.pat_gip = re.compile("inet\s(.+)/")

        self.hosts = []
        self._gw = self.get_gateway()
        self._gw_mac = ""
        self._iface = "wlp2s0"
        self._mac = ""
        self._ip = ""

        self.prompt_iface()

        self.get_ip()

        self.ui.lbl_gw.setText("<b>{}</b>".format(self._gw))
        self.ui.lbl_mac.setText("<b>{}</b>".format(self._mac))
        self.ui.lbl_ip.setText("<b>{}</b>".format(self._ip))
        self.ui.lbl_iface.setText("<b>{}</b>".format(self._iface))

        self.cutall = True

        self.ui.act_scan.trigger()

    def init_ui(self):
        self.ui.action_Help.setIcon(QIcon("img/help-circle.png"))
        self.ui.action_About.triggered.connect(self.act_about_triggered)
        self.ui.act_scan.triggered.connect(self.act_scan_triggered)
        self.ui.act_scan.setIcon(QIcon("img/scan.png"))
        self.ui.act_cut.setIcon(QIcon("img/cut_all.png"))
        self.ui.act_cut.triggered.connect(self.act_cutall_triggered)
        self.ui.tbl_hosts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tbl_hosts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tbl_hosts.verticalHeader().setVisible(False)
        self.ui.tbl_hosts.setColumnCount(TABLE_COLUMN_COUNT)
        self.ui.tbl_hosts.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Device Manufacturer", "Status"])
        self.ui.tbl_hosts.setColumnWidth(0, 100)
        self.ui.tbl_hosts.setColumnWidth(1, 150)
        self.ui.tbl_hosts.setColumnWidth(2, 240)
        self.ui.tbl_hosts.setShowGrid(False)

        self.ui.actionShow_Icons_Text.setData(Qt.ToolButtonTextUnderIcon)
        self.ui.actionShow_Icons.setData(Qt.ToolButtonIconOnly)

        group = QActionGroup(self)
        group.addAction(self.ui.actionShow_Icons)
        group.addAction(self.ui.actionShow_Icons_Text)
        group.triggered.connect(self.act_toolbar_show)


    def act_toolbar_show(self, action):
        self.settings.setValue("toolbar_show", action.data())
        self.ui.toolBar.setToolButtonStyle(action.data())

    def act_cutall_triggered(self):
        if self.cutall:
            self.cutall = False
            self.ui.act_cut.setIcon(QIcon("img/uncut_all.png"))
            self.ui.act_cut.setText("Resume All")
        else:
            self.cutall = True
            self.ui.act_cut.setIcon(QIcon("img/cut_all.png"))
            self.ui.act_cut.setText("Cut All")

    def get_ip(self):
        (s_code, s_out) = subprocess.getstatusoutput("ip addr show {}".format(self._iface))
        try:
            self._ip = self.pat_gip.findall(s_out)[0]
        except IndexError:
            print("COULD NOT GET IP")
            exit()

    def prompt_iface(self):
        ifaces_names = []
        ifaces_macs = []
        ifaces = QtNetwork.QNetworkInterface.allInterfaces()
        for i in ifaces:
            ifaces_names.append(str(i.name()))
            ifaces_macs.append(str(i.hardwareAddress()))

        if not self.settings.value("iface") or self.settings.value("iface") not in ifaces_names:
            result, ok = QInputDialog.getItem(self, self.tr("Network Interfaces"), self.tr("Select your Interface:"),
                                              ifaces_names, 0, False)
            if ok:
                self._iface = result
                self._mac = ifaces_macs[ifaces_names.index(result)]
                self.settings.setValue("iface", self._iface)
            else:
                QMessageBox.critical(self, TITLE, "You must select an interface card")
                exit()
        else:
            self._iface = self.settings.value("iface")
            self._mac = ifaces_macs[ifaces_names.index(self._iface)]

    def get_gateway(self):
        (s_code, s_out) = subprocess.getstatusoutput("ip route list")
        try:
            gw_ip = s_out.split("\n")[0].split(" ")[2]
        except IndexError:
            print("COULD NOT GET GATEWAY IP")
            exit()

        return gw_ip

    def populate_model(self, hosts):
        self.hosts = hosts
        self.ui.tbl_hosts.setRowCount(len(hosts))
        for i, k in enumerate(hosts):
            self.ui.tbl_hosts.setItem(i, R_IP, QTableWidgetItem(k))
            self.ui.tbl_hosts.setItem(i, R_MAC, QTableWidgetItem(hosts[k]))
            self.ui.tbl_hosts.setItem(i, R_MAC_MAN, QTableWidgetItem("Unknown"))
            self.btn_cut = QPushButton("Cut")
            self.btn_cut.setCheckable(True)
            self.btn_cut.setChecked(False)
            self.btn_cut.setIcon(QIcon("img/lan-connect.png"))
            self.btn_cut.clicked.connect(self.btn_cut_clicked)
            self.ui.tbl_hosts.setCellWidget(i, R_STATUS, self.btn_cut)

        self.set_device_man()

    def set_device_man(self):
        f = open("/usr/share/nmap/nmap-mac-prefixes")

        for line in f.readlines():
            for i, k in enumerate(self.hosts):
                mac = self.hosts[k].replace(":", "").upper()[:6]
                if line.startswith(mac):
                    self.ui.tbl_hosts.setItem(i, R_MAC_MAN, QTableWidgetItem(line[7:]))
                    break
        f.close()

    def get_device_name(self, mac):
        f = open("/usr/share/nmap/nmap-mac-prefixes")

        for line in f.readlines():
            mac = mac.replace(":", "").upper()[:6]
            if line.startswith(mac):
                f.close()
                return line[7:]
        else:
            f.close()
            return ""

    def act_scan_triggered(self):
        self.ui.tbl_hosts.clearContents()
        self.ui.tbl_hosts.setRowCount(0)
        self.ui.act_scan.setEnabled(False)
        self.ui.statusbar.showMessage("Scanning")
        ct = CommandThread("arp-scan --interface={} {}/24".format(self._iface, self._gw), self)
        ct.results.connect(self.scan_completed)
        ct.start()

    def act_about_triggered(self):
        AboutDialog(self).show()

    def scan_completed(self, s_code, s_out):
        if s_code == 0:
            hosts = self.pat_arp.findall(s_out)
            # Get gatway mac address
            hosts = dict(hosts)
            self._gw_mac = hosts[self._gw]
            # Remove gateway from list
            del hosts[self._gw]

            self.populate_model(hosts)
            self.ui.lbl_gw.setText("<b>{} ({})</b>".format(self._gw, self.get_device_name(self._gw_mac)))
            self.ui.lbl_mac.setText("<b>{} ({})</b>".format(self._mac, self.get_device_name(self._mac)))
        else:
            QMessageBox.critical(self, TITLE, s_out)

        self.ui.statusbar.showMessage("Done")
        self.ui.act_scan.setEnabled(True)

    def btn_cut_clicked(self):
        button = qApp.focusWidget()

        # or button = self.sender()
        index = self.ui.tbl_hosts.indexAt(button.pos())

        if index.isValid():
            self.ui.tbl_hosts.selectRow(index.row())
            if button.isChecked():
                button.setText("&Uncut")
                button.setIcon(QIcon("img/lan-disconnect.png"))
            else:
                button.setText("&Cut")
                button.setIcon(QIcon("img/lan-connect.png"))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)

    w = MainWidget()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
