# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.txbList = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.txbList.setObjectName("txbList")
        self.verticalLayout_7.addWidget(self.txbList)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(Form)
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
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_4.addWidget(self.spinBox)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.btn_ok = QtWidgets.QPushButton(Form)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout_4.addWidget(self.btn_ok)
        self.btn_stop = QtWidgets.QPushButton(Form)
        self.btn_stop.setObjectName("btn_stop")
        self.horizontalLayout_4.addWidget(self.btn_stop)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.setStretch(0, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "10086问卷调查"))
        self.groupBox_2.setTitle(_translate("Form", "List"))
        self.groupBox.setTitle(_translate("Form", "Logs"))
        self.label.setText(_translate("Form", "delay"))
        self.label_2.setText(_translate("Form", "hour"))
        self.btn_ok.setText(_translate("Form", "start"))
        self.btn_stop.setText(_translate("Form", "stop"))
