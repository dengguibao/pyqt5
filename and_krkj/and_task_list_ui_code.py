from PyQt5 import QtWidgets, QtGui
from and_task_list_ui import Ui_Dialog as Ui_taskList
from and_krkj_api import Api


class TaskListDialog:

    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.ui = Ui_taskList()
        self.ui.setupUi(self.form)
        self.update_task_list()
        self.api = Api()

    def show(self):
        self.form.show()

    def update_task_list(self, username=None, area_name=None):
        header = [
            'id',
            'activityinstname',
            'flowId',
            # 'workitemId',
            'processinstname',
            'createTime',
            'flowNo',
            # 'participantid',
            'participantname'
        ]
        if username:
            userinfo = self.api.get_userinfo_by_username(username)
            empid = userinfo['data']['empId']
            task_list = self.api.get_task_list_by_area_name(area_name, empid)

            model = QtGui.QStandardItemModel(len(task_list['data']), len(header))
            r = 0
            for i in task_list['data']:
                c = 0
                for c in range(len(header)):
                    key = header[c]
                    item = QtGui.QStandardItem('%s' % i[key])
                    model.setItem(r, c, item)
                    c += 1
                r += 1
        else:
            model = QtGui.QStandardItemModel(0, len(header))

        model.setHorizontalHeaderLabels(header)
        self.ui.tableView.setModel(model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.ui.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)