from api import Api
from main_ui import Ui_Form
from PyQt5 import QtWidgets, QtCore
import sys
import time
import os


class Worker(QtCore.QThread):

    signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.api = None
        self.sn_list = None
        self.only_query = False
        self.uninstall_list = []
        self.stopAndExit = False

    def set_env_var(self, api, sn_data, uninstall_list, only_query=False):
        self.api = api
        self.sn_list = sn_data
        self.only_query = only_query
        self.uninstall_list = uninstall_list

    def run(self):
        if not self.sn_list:
            self.update_sys_state()
            exit()

        for sn in self.sn_list:
            if self.stopAndExit:
                break

            dev_info = self.api.query_dev_list(sn)

            if dev_info['totalSize'] >= 1 and len(dev_info['data']) > 0:
                dev_id = dev_info['data'][0]['devId']
                dev_mac = dev_info['data'][0]['devMac']
            else:
                self.signal.emit('SN: %s , message:not found that ONT device' % sn)
                continue

            plugin_list = None
            if dev_mac and dev_id:
                plugin_list = self.api.query_plugin_list(dev_mac)
            else:
                self.signal.emit('SN: %s , message:not found MAC address about that ONT device' % sn)

            if not plugin_list or 'Plugin' not in plugin_list:
                continue

            if plugin_list and len(plugin_list['Plugin']) == 0:
                self.signal.emit('SN:%s , message:not found any plugin about this ont' % sn)
                continue

            for i in plugin_list['Plugin']:
                self.signal.emit(
                    ('SN: %s , plugin_name:{Plugin_Name}, version:{Version}, running:{Run}' % sn).format(**i)
                )
                if not self.only_query:
                    if i['Plugin_Name'] in self.uninstall_list:
                        args = {
                            'devId': dev_id,
                            'mac': dev_mac,
                            'sn': sn,
                            'pluginName': i['Plugin_Name'],
                            'pluginVersion': i['Version']
                        }
                        plugin_info = self.api.check_plugin_exist(args)
                        if plugin_info['result'] == 1 and plugin_info['vars']['pluginId'] > 0:
                            args['pluginId'] = plugin_info['vars']['pluginId']
                            args['pluginVersion'] = '2.2.2' if args['pluginName'] == 'com.chinamobile.smartgateway.cmccdpi' else args['pluginVersion']

                            uninstall_info = self.api.plugin_uninstall(args)
                            self.signal.emit(
                                'SN: %s , action:uninstall_plugin, device_id:%s, dev_mac:%s, plugin_id:%s, uninstall_plugin:%s, plugin_version:%s, return_message:%s' % (
                                    sn,
                                    args['devId'],
                                    args['mac'],
                                    args['pluginId'],
                                    args['pluginName'],
                                    args['pluginVersion'],
                                    uninstall_info['message']
                                )
                            )
            if self.only_query:
                self.signal.emit('split_lines')

        self.stopAndExit = True
        self.signal.emit('update_front_ui')


class Main:

    def __init__(self):
        # self.running = False

        self.form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.form)

        self.api = Api()

        self.worker = Worker()
        self.worker.signal.connect(self.sub_th_refresh_ui)
        # self.sig.signal.connect(self.sub_th_refresh_ui)

        self.form.setFixedSize(self.form.width(), self.form.height())
        self.ui.btnStart.setDisabled(True)
        self.ui.btnStop.setDisabled(True)
        self.ui.btnQuery.setDisabled(True)
        self.ui.txbLogs.setReadOnly(True)

        self.msg = QtWidgets.QMessageBox()

        self.ui.btnStop.clicked.connect(self.init_button_event)
        self.ui.btnStart.clicked.connect(self.init_button_event)
        self.ui.btnQuery.clicked.connect(self.init_button_event)
        self.form.setWindowTitle('ONT plugin operator')

        filename = '%s.txt' % time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
        self.fo = open(filename, 'a+', encoding='utf-8')

        self.user_login()

    def init_button_event(self):
        btn_text = self.form.sender().text()

        uninstall_txt = self.ui.txbUninstall_list.text().strip()
        uninstall_list = [] if uninstall_txt == '' else uninstall_txt.split(',')

        if btn_text == 'Start' and not self.worker.isRunning():
            sn_list = self.get_sn_list_from_file()
            if sn_list:
                self.empty_logs()
                self.ui.txbLogs.appendPlainText('从文件共读取%s个SN码' % len(sn_list))
                self.worker.set_env_var(self.api, sn_list, uninstall_list)
                self.worker.start()
                self.worker.stopAndExit = False
                self.update_sys_state()
                # _thread.start_new_thread(self.th_process, (sn_list,))
            else:
                self.msg.critical(self.form, '警告', '未读取到任何SN码')

        if btn_text == 'Stop' and self.worker.isRunning():
            self.worker.stopAndExit = True
            self.update_sys_state()

        if btn_text == 'Query' and not self.worker.isRunning():
            sn = self.ui.txbSn.text().strip()
            print(sn)
            if sn:
                self.empty_logs()
                self.worker.set_env_var(self.api, [sn], uninstall_list, True)
                self.worker.start()
                self.worker.stopAndExit = False

    def empty_logs(self):
        if self.fo:
            self.fo.write('\n')
        self.ui.txbLogs.setPlainText('')

    @staticmethod
    def get_sn_list_from_file(file='data.txt'):
        if not os.path.exists(file):
            return
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.read()

        data = []
        for item in lines.splitlines():
            line = item.strip()
            if line[0:1] == '#' or line == '':
                continue
            else:
                data.append(line)

        if data:
            return data
        return

    def sub_th_refresh_ui(self, msg):
        if msg == 'split_lines':
            self.ui.txbLogs.appendPlainText('')
        elif msg == 'update_front_ui':
            self.update_sys_state()
        else:
            self.ui.txbLogs.appendPlainText(
                '%s, %s' % (
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                    msg
                )
            )
            if self.fo:
                self.fo.write(
                    '%s, %s\n' % (
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                        msg
                    )
                )

    def update_sys_state(self):
        if not self.worker.stopAndExit:
            self.ui.btnStop.setDisabled(False)
            self.ui.btnStart.setDisabled(True)
            self.ui.btnQuery.setDisabled(True)
        else:
            self.ui.btnStop.setDisabled(True)
            self.ui.btnStart.setDisabled(False)
            self.ui.btnQuery.setDisabled(False)

    def user_login(self):
        try:
            login_state = self.api.user_login()
        except:
            self.ui.txbLogs.appendPlainText('网络链接失败')
            return

        if login_state != '登录成功':
            self.ui.txbLogs.appendPlainText('登陆失败')
            return

        self.ui.btnStart.setDisabled(False)
        self.ui.btnStop.setDisabled(True)
        self.ui.btnQuery.setDisabled(False)

        self.ui.txbLogs.appendPlainText('登陆成功')
        self.api.build_token()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main()
    main_window.form.show()
    sys.exit(app.exec_())

    # a = Api()
    # login_state = a.user_login()
    #
    # if login_state != '登录成功':
    #     exit()
    #
    # sn = ''
    #
    # dev_info = a.query_dev_list(sn)
    #
    # if dev_info['totalSize'] >= 1 and len(dev_info['data']) > 0:
    #     dev_id = dev_info['data'][0]['devId']
    #     dev_mac = dev_info['data'][0]['devMac']
    #
    # if dev_mac and dev_id:
    #     plugin_list = a.query_plugin_list(dev_mac)
    #
    # if len(plugin_list['Plugin']) == 0:
    #     exit()
    #
    # for i in plugin_list['Plugin']:
    #     print('plugin_name:{Plugin_Name}, version:{Version}, running:{Run}'.format(**i))
    #     if '.cmccdpi' in i['Plugin_Name']:
    #         args = {
    #             'devId': dev_id,
    #             'mac': dev_mac,
    #             'sn': sn,
    #             'pluginName': i['Plugin_Name'],
    #             'pluginVersion': i['Version']
    #         }
    #         plugin_info = a.check_plugin_exist(args)
    #         if plugin_info['result'] == 1 and plugin_info['vars']['pluginId'] > 0:
    #             args['pluginId'] = plugin_info['vars']['pluginId']
    #             uninstall_info = a.plugin_uninstall(args)
    #             print(uninstall_info['message'])
