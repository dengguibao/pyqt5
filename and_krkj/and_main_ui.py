# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'and.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tvList = QtWidgets.QTableView(self.groupBox)
        self.tvList.setObjectName("tvList")
        self.verticalLayout_3.addWidget(self.tvList)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.txbLog = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.txbLog.setReadOnly(True)
        self.txbLog.setObjectName("txbLog")
        self.verticalLayout_4.addWidget(self.txbLog)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.verticalLayout.setStretch(0, 7)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sb_delay = QtWidgets.QSpinBox(self.groupBox_3)
        self.sb_delay.setProperty("value", 1)
        self.sb_delay.setObjectName("sb_delay")
        self.horizontalLayout.addWidget(self.sb_delay)
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.sb_rdelay = QtWidgets.QSpinBox(self.groupBox_3)
        self.sb_rdelay.setProperty("value", 1)
        self.sb_rdelay.setObjectName("sb_rdelay")
        self.horizontalLayout.addWidget(self.sb_rdelay)
        spacerItem = QtWidgets.QSpacerItem(531, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_5.addWidget(self.groupBox_3)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_2.setStretch(0, 9)
        self.verticalLayout_2.setStretch(1, 1)

        self.sb_delay.setMinimum(1)
        self.sb_rdelay.setMinimum(1)
        self.sb_delay.setMaximum(5)
        self.sb_rdelay.setMaximum(5)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "和运维扩容扩建"))
        self.groupBox.setTitle(_translate("Form", "List"))
        self.groupBox_2.setTitle(_translate("Form", "Logs"))
        self.groupBox_3.setTitle(_translate("Form", "Setting"))
        self.label.setText(_translate("Form", "Delay"))
        self.label_2.setText(_translate("Form", "Random Dely"))
