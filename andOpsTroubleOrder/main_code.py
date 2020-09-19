from main import Ui_Form as Ui_Main
from importAccount_code import ImportAccountDialog
from PyQt5 import QtWidgets
import sys


class Main:

    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.ui = Ui_Main()
        self.ui.setupUi(self.form)
        self.account_list = []
        self.init_button_event()

        self.import_window = ImportAccountDialog()

    def show(self):
        self.form.show()

    def init_button_event(self):
        self.ui.btBox.clicked.connect(self.button_onclick_event)
        pass

    def button_onclick_event(self, button):
        btn_text = button.text()
        if 'OK' in btn_text:
            print('ok')
        elif 'Import' in btn_text:
            print('import')
            self.import_window.show()
        elif 'Cancel' in btn_text:
            print('cancel')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())