# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MCServer\Phsebot3.0\Library\UIs\xbox.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Xbox(object):
    def setupUi(self, Xbox):
        Xbox.setObjectName("Xbox")
        Xbox.resize(681, 551)
        self.add = QtWidgets.QPushButton(Xbox)
        self.add.setGeometry(QtCore.QRect(10, 510, 81, 31))
        self.add.setObjectName("add")
        self.deleter = QtWidgets.QPushButton(Xbox)
        self.deleter.setGeometry(QtCore.QRect(100, 510, 81, 31))
        self.deleter.setObjectName("deleter")
        self.tableView = QtWidgets.QTableView(Xbox)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 661, 491))
        self.tableView.setObjectName("tableView")
        self.refursh = QtWidgets.QPushButton(Xbox)
        self.refursh.setGeometry(QtCore.QRect(190, 510, 81, 31))
        self.refursh.setObjectName("refursh")
        self.pushButton = QtWidgets.QPushButton(Xbox)
        self.pushButton.setGeometry(QtCore.QRect(280, 510, 76, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Xbox)
        QtCore.QMetaObject.connectSlotsByName(Xbox)

    def retranslateUi(self, Xbox):
        _translate = QtCore.QCoreApplication.translate
        Xbox.setWindowTitle(_translate("Xbox", "Form"))
        self.add.setText(_translate("Xbox", "添加"))
        self.deleter.setText(_translate("Xbox", "删除"))
        self.refursh.setText(_translate("Xbox", "刷新"))
        self.pushButton.setText(_translate("Xbox", "保存"))
