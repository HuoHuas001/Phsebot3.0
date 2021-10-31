# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MCServer\Phsebot3.0\Library\UIs\crontab.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Crontab(object):
    def setupUi(self, Crontab):
        Crontab.setObjectName("Crontab")
        Crontab.resize(681, 551)
        self.newer = QtWidgets.QPushButton(Crontab)
        self.newer.setGeometry(QtCore.QRect(10, 510, 81, 31))
        self.newer.setObjectName("newer")
        self.deleter = QtWidgets.QPushButton(Crontab)
        self.deleter.setGeometry(QtCore.QRect(100, 510, 81, 31))
        self.deleter.setObjectName("deleter")
        self.refrusher = QtWidgets.QPushButton(Crontab)
        self.refrusher.setGeometry(QtCore.QRect(190, 510, 81, 31))
        self.refrusher.setObjectName("refrusher")
        self.tableView = QtWidgets.QTableView(Crontab)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 661, 491))
        self.tableView.setObjectName("tableView")
        self.save = QtWidgets.QPushButton(Crontab)
        self.save.setGeometry(QtCore.QRect(280, 510, 81, 31))
        self.save.setObjectName("save")

        self.retranslateUi(Crontab)
        QtCore.QMetaObject.connectSlotsByName(Crontab)

    def retranslateUi(self, Crontab):
        _translate = QtCore.QCoreApplication.translate
        Crontab.setWindowTitle(_translate("Crontab", "Form"))
        self.newer.setText(_translate("Crontab", "新建"))
        self.deleter.setText(_translate("Crontab", "删除"))
        self.refrusher.setText(_translate("Crontab", "刷新"))
        self.save.setText(_translate("Crontab", "保存"))
