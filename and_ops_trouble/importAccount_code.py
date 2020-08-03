from importAccount import Ui_Dialog as Ui_import
from PyQt5 import QtWidgets


class ImportAccountDialog:

    account_list = None

    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.ui = Ui_import()
        self.ui.setupUi(self.form)
        self.account_list = []
        self.init_button_event()

    def show(self):
        self.form.show()

    def init_button_event(self):
        self.ui.buttonBox.clicked.connect(self.button_onclick_event)

    def button_onclick_event(self, button):
        btn_text = button.text()
        if 'OK' in btn_text:
            self.get_user_input_text()

    def get_user_input_text(self):
        text = self.ui.plainTextEdit.toPlainText()
        msgBox = QtWidgets.QMessageBox()
        if text.strip() == '':
            msgBox.about(self.form, u'notification', u'failed!')
            return
        for i in text.split('\n'):
            if i.strip() == '' or i.strip()[:1] == '#' or '|' not in i:
                continue
            x = i.strip().split('|')
            self.account_list.append(
                (x[0].strip(), x[1].strip())
            )
        msgBox.about(self.form, u'notification', u'success')
        self.ui.plainTextEdit.setPlainText('')
