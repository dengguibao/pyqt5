import sys
from PyQt5 import QtWidgets
from and_main_ui_code import Entry

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    entry = Entry()
    # help_dialog = HelpDialog()
    # task_list_dialog = TaskListDialog()
    sys.exit(app.exec_())
