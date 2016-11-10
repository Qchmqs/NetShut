#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication,QWidget
from ui_main import Ui_Form


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)


def main():
    app = QApplication(sys.argv)

    w = MainWidget()

    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()