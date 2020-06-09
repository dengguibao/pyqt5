from and_help_ui import Ui_Dialog as Ui_Help
from PyQt5 import QtWidgets


class HelpDialog:

    def __init__(self):
        self.form = QtWidgets.QDialog()
        ui = Ui_Help()
        ui.setupUi(self.form)

    def show(self):
        self.form.show()
