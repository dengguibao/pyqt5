import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import re
import time
import _thread
from api import Poll
from main_ui import Ui_Form


class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(list)


class Main():
    running = False
    log_fo = None

    def __init__(self):
        self.sig = Communicate()
        self.sig.signal.connect(self.update_log)

        self.form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.form)

        self.msgBox = QtWidgets.QMessageBox()
        self.ui.btn_ok.clicked.connect(self.btn_start_click_event)
        self.ui.btn_stop.clicked.connect(self.btn_stop_click_event)
        self.form.setWindowTitle('10086问卷调查')
        # self.ui.label.setText('延迟')
        # self.ui.label_2.setText('小时')

    def update_log(self, val):
        self.ui.progressBar.setValue(int(val[0] * 100))
        self.ui.txbLogs.appendPlainText(val[1])

    def btn_stop_click_event(self):
        self.ui.txbList.setReadOnly(False)
        self.ui.progressBar.setValue(0)
        self.ui.spinBox.setReadOnly(False)
        if self.running is False:
            return
        self.ui.txbLogs.appendPlainText(u"停止执行")
        self.running = False
        self.log_close()

    def btn_start_click_event(self):
        if self.running:
            return
        text = self.ui.txbList.toPlainText()
        if not text.strip():
            self.msgBox.warning(self.form, u'通知', u'内容为空')
            return
        self.ui.txbList.setReadOnly(True)
        self.ui.spinBox.setReadOnly(True)
        self.ui.txbLogs.setPlainText('开始执行...')
        # replace user input text
        text = text.replace('	', '|')
        text = re.sub(' +', ' ', text)
        # init log file handler
        self.init_log()
        # start new thread
        _thread.start_new_thread(self.poll_start, (text, ))

    def init_log(self):
        if self.log_fo:
            pass
        else:
            filename = '%s.txt' % time.strftime('%Y%m%d%H%M%S', time.localtime())
            self.log_fo = open(filename, 'w+', encoding='utf-8')

    def log_close(self):
        if self.log_fo:
            self.log_fo.close()
            self.log_fo = None

    def write_log(self, msg):
        if self.log_fo:
            self.log_fo.write(msg+'\r\n')

    def poll_start(self, text):
        self.running = True
        pre_time = self.ui.spinBox.value()
        fmt = '%Y/%m/%d %H:%M'
        poll = Poll()
        success_list = []
        data = []
        for i in text.split('\n'):
            if i[0:1] == '#' or i.strip() == '':
                continue
            else:
                data.append(i)

        while True:
            if not self.running:
                self.log_close()
                break

            # print(success_list)
            if len(success_list) == len(data):
                self.sig.signal.emit([0, u'执行结束'])
                self.running = False
                self.ui.spinBox.setReadOnly(False)
                self.ui.txbList.setReadOnly(False)
                self.log_close()

            for line in data:
                try:
                    x = line.split('|')
                    now = int(time.time())
                    user_date = time.mktime(time.strptime(x[0], fmt))
                except Exception as e:
                    self.sig.signal.emit([0, u'列表格式错误，已停止执行'])
                    self.running = False
                    self.ui.spinBox.setReadOnly(False)
                    self.ui.txbList.setReadOnly(False)
                    self.log_close()
                    exit()

                is_start = user_date + pre_time * 60 * 60
                print(is_start, now, now - is_start)
                if (now-is_start > 0) and line not in success_list:
                    resp_text = poll.submit_poll(x[1])
                    # self.txbLogs.appendPlainText(resp_text)
                    success_list.append(line)
                    progress_percent = len(success_list) / len(data)
                    if 'success' in resp_text:
                        a = resp_text.split(', ')
                        x.append(a[-1])
                        x.append(a[-2])
                        self.write_log(', '.join(x))
                    self.sig.signal.emit([progress_percent, resp_text])
            self.log_close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main()
    main_window.form.show()
    sys.exit(app.exec_())