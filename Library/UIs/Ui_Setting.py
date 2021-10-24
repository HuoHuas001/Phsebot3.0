# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MCServer\Phsebot3.0\Library\UIs\Setting.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Setting(object):
    def setupUi(self, Setting):
        Setting.setObjectName("Setting")
        Setting.resize(681, 551)
        self.lineEdit = QtWidgets.QLineEdit(Setting)
        self.lineEdit.setGeometry(QtCore.QRect(70, 10, 561, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Setting)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 31))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.toolButton = QtWidgets.QToolButton(Setting)
        self.toolButton.setGeometry(QtCore.QRect(640, 10, 31, 31))
        self.toolButton.setObjectName("toolButton")

        self.retranslateUi(Setting)
        QtCore.QMetaObject.connectSlotsByName(Setting)

    def retranslateUi(self, Setting):
        _translate = QtCore.QCoreApplication.translate
        Setting.setWindowTitle(_translate("Setting", "Form"))
        self.label.setText(_translate("Setting", "BDS路径"))
        self.toolButton.setText(_translate("Setting", "..."))
