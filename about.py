from PyQt5.QtWidgets import QDialog

from ui.about_ui import Ui_dlg_about

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_dlg_about()
        self.ui.setupUi(self)

