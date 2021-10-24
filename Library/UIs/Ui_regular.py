# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MCServer\Phsebot3.0\Library\UIs\regular.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Regular(object):
    def setupUi(self, Regular):
        Regular.setObjectName("Regular")
        Regular.resize(681, 546)
        self.deleter = QtWidgets.QToolButton(Regular)
        self.deleter.setGeometry(QtCore.QRect(100, 510, 81, 31))
        self.deleter.setObjectName("deleter")
        self.add = QtWidgets.QToolButton(Regular)
        self.add.setGeometry(QtCore.QRect(10, 510, 81, 31))
        self.add.setObjectName("add")
        self.refrush = QtWidgets.QPushButton(Regular)
        self.refrush.setGeometry(QtCore.QRect(190, 510, 81, 31))
        self.refrush.setObjectName("refrush")
        self.tableView = QtWidgets.QTableView(Regular)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 661, 491))
        self.tableView.setObjectName("tableView")
        self.pushButton = QtWidgets.QPushButton(Regular)
        self.pushButton.setGeometry(QtCore.QRect(280, 510, 81, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Regular)
        QtCore.QMetaObject.connectSlotsByName(Regular)

    def retranslateUi(self, Regular):
        _translate = QtCore.QCoreApplication.translate
        Regular.setWindowTitle(_translate("Regular", "Form"))
        self.deleter.setText(_translate("Regular", "删除"))
        self.add.setText(_translate("Regular", "添加"))
        self.refrush.setText(_translate("Regular", "刷新"))
        self.pushButton.setText(_translate("Regular", "保存"))
