from main_ui import Ui_Form
from cmcc_sp_api import Api, ReadConfig
from expendApprove.excel_reader import ExcelReader
from PyQt5 import QtWidgets, QtCore, QtGui
import _thread
import time
import sys


class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(list)


class Entry:
    def __init__(self):
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)
        self.init_button_event()

        self.api = Api()

        self.running = False
        self.stopEvent = False

        self.sig = Communicate()
        self.sig.signal.connect(self.subth_refresh_ui)

        self.table_item_model = None
        self.task_list_data = None
        self.data_field = [
            u'工单编号',
            u'主题',
            u'派单时间',
            # u'结束时间',
            # u'发起人',
            u'地市',
            u'区县',
            u'小区',
            # u'小区ID',
            # u'箱体端口使用率',
            u'分纤箱',
            u'当前环节',
            u'当前待办人',
            u'当前待办人账号'

        ]

        rc = ReadConfig()
        user, pwd = rc.get_user_and_pwd()
        self.user = user
        self.pwd = pwd

        self.update_table_view()
        self.Form.show()

    def init_button_event(self):
        self.ui.buttonBox.clicked.connect(self.button_onclick_event)

    def button_onclick_event(self, button):
        btn_text = button.text()
        if 'OK' in btn_text:
            if self.running:
                return
            self.set_sys_status('start')
            self.start()
        elif 'Cancel' in btn_text:
            self.set_sys_status('stop')

    def set_sys_status(self, status):
        if status == 'start':
            self.stopEvent = False
            self.running = True
        elif status == 'stop':
            self.stopEvent = True
            self.running = False

    def subth_refresh_ui(self, data):
        if not data[1]:
            return
        if data[0] > 0:
            self.ui.txbLog.appendPlainText('%s %s' % (time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()), data[1]))
        elif data[0] == 0:
            item = QtGui.QStandardItem('%s' % data[1][2])
            self.table_item_model.setItem(data[1][0], data[1][1], item)

    def start(self):
        if not self.task_list_data:
            self.ui.txbLog.appendPlainText('list data is empty!')
            self.set_sys_status('stop')
            return
        else:
            # start service
            self.api.login(self.user, self.pwd)
            _thread.start_new_thread(self.service_th, (self.task_list_data,))
            # start a new thread list request error logs
            _thread.start_new_thread(self.listen_error_msg, ())

    # def table_item_double_click_event(self, index):
    #     row = index.row()
    #     areaname_tag = u'小区'
    #     username_tag = u'账号'
    #     a_index = self.data_field.index(areaname_tag)
    #     u_index = self.data_field.index(username_tag)
    #     username = self.table_item_model.data(self.table_item_model.index(row, u_index))
    #     areaname = self.table_item_model.data(self.table_item_model.index(row, a_index))
    #     self.task_list_dialog.update_task_list(username, areaname)
    #     self.task_list_dialog.show()

    def service_th(self, data):
        n = 0
        for i in data:
            if self.stopEvent:
                self.sig.signal.emit([0, (n, len(self.data_field)-2, 'cancel')])
                break
            order_no_field = u'工单编号'
            u_index = self.data_field.index(order_no_field)
            order_no = i[u_index]

            # row start
            self.sig.signal.emit([0, (n, len(self.data_field)-1, 'running')])
            order_data = self.api.query_order(order_no)
            code = 1
            if order_data and order_data['totalCount'] > 0:
                code, result = self.api.submit(order_data['root'][0])
            if code == 0:
                # success ok
                #  update completed total
                self.sig.signal.emit([code, (n, len(self.data_field)-2, result)])
                #  update status cell
                self.sig.signal.emit([code, (n, len(self.data_field)-1, 'done')])
            else:
                # has error
                #  update cell data
                self.sig.signal.emit([0, (n, len(self.data_field)-1, 'failed')])
                #  send error msg to logs
                self.sig.signal.emit([code, result])
            n += 1
        self.set_sys_status('stop')

    def listen_error_msg(self):
        old_msg = ''
        while True:
            if self.stopEvent:
                break
            if self.api.error != old_msg:
                self.sig.signal.emit([1, self.api.error])
            old_msg = self.api.error

    def update_table_view(self):
        table_reader = ExcelReader(**{
            'book_name': 'data.xls',
            'sheet_name': 'Sheet1'
        })
        origin_field_length = len(self.data_field)
        table_data = table_reader.get_data(self.data_field)
        if table_data:
            model = QtGui.QStandardItemModel(len(table_data), origin_field_length + 2)
            self.data_field.append(u'完成情况')
            self.data_field.append(u'状态')
        else:
            model = QtGui.QStandardItemModel(0, len(self.data_field))
        model.setHorizontalHeaderLabels(self.data_field)

        if table_data:
            for i in range(len(table_data)):
                for n in range(origin_field_length):
                    # print(i, n, table_data[i][n])
                    item = QtGui.QStandardItem('%s' % table_data[i][n])
                    model.setItem(i, n, item)

        self.ui.tvList.setModel(model)
        # set horizontal stretch
        self.ui.tvList.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tvList.horizontalHeader().setStretchLastSection(True)
        # disable edit mode
        self.ui.tvList.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        # just select rows
        self.ui.tvList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # self.ui.tvList.setColumnWidth(0, 60)
        self.table_item_model = model
        self.task_list_data = table_data
        # double click event
        # self.ui.tvList.doubleClicked.connect(self.table_item_double_click_event)
        # dynamic update cell
        # item = QtGui.QStandardItem('11111')
        # model.setItem(1, origin_field_length+1, item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    entry = Entry()
    # help_dialog = HelpDialog()
    # task_list_dialog = TaskListDialog()
    sys.exit(app.exec_())