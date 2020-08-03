# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './main.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import re
import time
import json
import urllib3
import _thread
from evaluateResult import evaluateResult

urllib3.disable_warnings()


class Poll:
    proxies = {
        # 'http': 'http://172.31.10.84:2345',
        # 'https': 'http://172.31.10.84:2345'
    }

    req_headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json, text/javascript, */*; q=0.01,',
        'Connection': 'Keep-Alive',
        'Host': 'eva.customer.10086.cn',
        'Origin': 'https://eva.customer.10086.cn',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/79.0.3945.130 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    s = None

    def __init__(self):
        s = requests.session()
        s.headers.update(self.req_headers)

        if not len(self.proxies):
            s.proxies = self.proxies
        self.s = s

    def submit_poll(self, url, poll_type):
        r = self.s.get(url, verify=False)
        if '重复提交' in r.text:
            return '%s 链接已提交,请勿重复提交' % url
        if '请求超时' in r.text:
            return '%s 链接已失效超时' % url

        jump302_url = r.url
        if 'token' in jump302_url:
            args = self.get_url_args(jump302_url)
        else:
            return '%s 无效链接' % url

        new_score_data = [
            {
                "score": 10,
                "questionId": "2019112612330061201052001",
                "questionTitle": "装机整体满意度",
                "answerOrder": 1,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": ""
            },
            {
                "score": 10,
                "questionId": "2020011919364267101052001",
                "questionTitle": "上门及时性",
                "answerOrder": 2,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "上门快,上门准时,提前预约时间"
            },
            {
                "score": 10,
                "questionId": "2019112614320298901052001",
                "questionTitle": "安装专业性",
                "answerOrder": 3,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "装机快,布线美观,现场干净整洁"
            },
            {
                "score": 10,
                "questionId": "2019112614355544701052001",
                "questionTitle": "安装人员服务",
                "answerOrder": 4,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "服务态度好,答疑指导耐心,工装整洁大方"
            },
            {
                "score": "",
                "questionId": "2019112614363640001053001",
                "questionTitle": "装机完成后是否测速",
                "suggestion": "",
                "surveyLables": "是",
                "surveyObjType": "0",
                "answerOrder": 5
            }
        ]

        trouble_score_data = [
            {
                "score": 10,
                "questionId": "2019112714221718701051001",
                "questionTitle": "故障维修整体满意度",
                "answerOrder": 1,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": ""
            },
            {
                "score": 10,
                "questionId": "2019112714472810201052001",
                "questionTitle": "上门及时性",
                "answerOrder": 2,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "上门快,上门准时,有提前预约时间"
            },
            {
                "score": 10,
                "questionId": "2019112714481805801051001",
                "questionTitle": "故障解决专业性",
                "answerOrder": 3,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "故障解决快,现场干净整洁"
            },
            {
                "score": 10,
                "questionId": "2019112714504311401052001",
                "questionTitle": "维修人员服务",
                "answerOrder": 4,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "服务态度好,答疑指导耐心,工装整洁大方"
            },
            {
                "score": "",
                "questionId": "2019112714514659501053001",
                "questionTitle": "维修完成后是否测速",
                "suggestion": "",
                "surveyLables": "是",
                "surveyObjType": "0",
                "answerOrder": 5
            }
        ]

        score_data = {
            "qnrSuggestion": "",
            "questionList": new_score_data if poll_type else trouble_score_data
        }
        # print(score_data)
        # 0新装　１故障
        eva_result = evaluateResult[0] if poll_type else evaluateResult[1]
        eva_result['qnrId'] = args['questionnaireId']
        post_data = {
            "questionList": json.dumps(score_data, ensure_ascii=False),
            "serNum": '',
            "channelId": '',
            "serType": '',
            "prvo": '',
            "servalue": '',
            "detailsUrl": '/survey/detailsofTomatoOrange.html?taskSheetId=',
            'qnrId': args['questionnaireId'],
            'h5PageUrlWeb': 'https://eva.customer.10086.cn/surv/QnrTomatoOrange.html?questionnaireId=%s' % args[
                'questionnaireId'],
            'token': args['token'],
            'evaluateResult': eva_result
        }

        self.req_headers['Referer'] = jump302_url
        self.s.headers.update(self.req_headers)
        # print(json.dumps(post_data, ensure_ascii=False))
        r = self.s.post(
            'https://eva.customer.10086.cn/surveyH5Response/dynamicQuestion',
            data=post_data,
            verify=False
        )
        if r.status_code == 200:
            del self.req_headers['Referer']
            return 'msg:success, status_code:%s, url:%s, return_text:%s' % (r.status_code, url, r.text)
            # return r.content
        else:
            return 'msg:failed, status_code:%s, url:%s, return_text:%s' % (r.status_code, url, r.text)

    def get_url_args(self, url):
        args = url.split('?')[1].replace('&&', '&').split('&')
        data = {}
        for i in args:
            x = i.split('=')
            data[x[0]] = x[1]
        return data


class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(list)


class Ui_Form(QtWidgets.QWidget):
    stopEvent = False
    running = False

    def __init__(self):
        super().__init__()
        self.setObjectName("Form")
        self.resize(744, 545)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.txbList = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.txbList.setObjectName("txbList")
        self.verticalLayout_7.addWidget(self.txbList)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.txbLogs = QtWidgets.QPlainTextEdit(self.groupBox)
        self.txbLogs.setBaseSize(QtCore.QSize(800, 600))
        self.txbLogs.setReadOnly(True)
        self.txbLogs.setObjectName("txbLogs")
        self.verticalLayout_6.addWidget(self.txbLogs)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_ok = QtWidgets.QPushButton(self)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout_4.addWidget(self.btn_ok)
        self.btn_stop = QtWidgets.QPushButton(self)
        self.btn_stop.setObjectName("btn_stop")
        self.horizontalLayout_4.addWidget(self.btn_stop)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMaximum(60)
        self.spinBox.setMinimum(1)
        self.horizontalLayout_4.addWidget(self.spinBox)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)

        # self.rb_new = QtWidgets.QRadioButton(self)
        # self.rb_new.setObjectName(u"rb_new")
        # self.rb_new.setChecked(True)
        # self.horizontalLayout_4.addWidget(self.rb_new)
        #
        # self.rb_trouble = QtWidgets.QRadioButton(self)
        # self.rb_trouble.setObjectName(u"rb_trouble")
        # self.horizontalLayout_4.addWidget(self.rb_trouble)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.setStretch(0, 10)
        self.verticalLayout_3.setStretch(1, 1)

        self.sig = Communicate()
        self.sig.signal.connect(self.update_log)

        self.msgBox = QtWidgets.QMessageBox()
        self.btn_ok.clicked.connect(self.btn_start_click_event)
        self.btn_stop.clicked.connect(self.btn_stop_click_event)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", u"10086问卷调查"))
        self.groupBox_2.setTitle(_translate("Form", "列表"))
        self.groupBox.setTitle(_translate("Form", "日志"))
        self.btn_ok.setText(_translate("Form", "开始"))
        self.btn_stop.setText(_translate("Form", "停止"))
        self.label.setText(_translate("Form", u"       延后"))
        self.label_2.setText(_translate("Form", "小时"))
        # self.rb_new.setText(_translate("Form", "新装"))
        # self.rb_trouble.setText(_translate("Form", "故障"))

    def update_log(self, val):
        self.progressBar.setValue(int(val[0] * 100))
        self.txbLogs.appendPlainText(val[1])

    def btn_stop_click_event(self):
        self.txbList.setReadOnly(False)
        self.progressBar.setValue(0)
        self.spinBox.setReadOnly(False)
        self.stopEvent = True
        if self.running is False:
            return
        self.txbLogs.appendPlainText(u"停止执行")
        self.running = False

    def btn_start_click_event(self):
        # self.msgBox.about(self.form, 'test title', 'test content')
        self.stopEvent = False
        if self.running == True:
            return

        text = self.txbList.toPlainText()
        if not text.strip():
            self.msgBox.about(self, u'通知', u'内容为空')
            return
        self.txbList.setReadOnly(True)
        self.spinBox.setReadOnly(True)
        self.txbLogs.setPlainText('开始执行...')
        text = text.replace('	', '|')
        text = re.sub(' +', ' ', text)
        # is_new_poll = self.rb_new.isChecked()
        _thread.start_new_thread(self.poll_start, (text, True))

    def poll_start(self, text, poll_type):
        # print(lines)
        self.running = True
        pre_time = self.spinBox.value()
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
            if self.stopEvent:
                break

            # print(success_list)
            if len(success_list) == len(data):
                self.sig.signal.emit([0, u'执行结束'])
                self.stopEvent = True
                self.running = False
                self.spinBox.setReadOnly(False)
                self.txbList.setReadOnly(False)

            for line in data:
                try:
                    x = line.split('|')
                    now = int(time.time())
                    user_date = time.mktime(time.strptime(x[0], fmt))
                except Exception as e:
                    self.sig.signal.emit([0, u'列表格式错误，已停止执行'])
                    self.stopEvent = True
                    self.running = False
                    self.spinBox.setReadOnly(False)
                    self.txbList.setReadOnly(False)
                    exit()

                is_start = user_date + pre_time * 60 * 60
                print(is_start, now, now - is_start)
                if (is_start == now + 1 or is_start == now - 1) and line not in success_list:
                    resp_text = poll.submit_poll(x[1], poll_type)
                    # self.txbLogs.appendPlainText(resp_text)
                    success_list.append(line)
                    progress_percent = len(success_list) / len(data)
                    self.sig.signal.emit([progress_percent, resp_text])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Form()
    ui.show()

    sys.exit(app.exec_())
