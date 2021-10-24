# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MCServer\Phsebot3.0\Library\UIs\BDSLog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BDS(object):
    def setupUi(self, BDS):
        BDS.setObjectName("BDS")
        BDS.resize(681, 551)
        BDS.setMinimumSize(QtCore.QSize(681, 551))
        BDS.setMaximumSize(QtCore.QSize(681, 551))
        self.BDSLogs = QtWidgets.QTextEdit(BDS)
        self.BDSLogs.setGeometry(QtCore.QRect(10, 10, 651, 431))
        self.BDSLogs.setObjectName("BDSLogs")
        self.RunCmd = QtWidgets.QPushButton(BDS)
        self.RunCmd.setGeometry(QtCore.QRect(640, 450, 31, 31))
        self.RunCmd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/check.png)")
        self.RunCmd.setText("")
        self.RunCmd.setObjectName("RunCmd")
        self.pushButton = QtWidgets.QPushButton(BDS)
        self.pushButton.setGeometry(QtCore.QRect(10, 490, 81, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(BDS)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 490, 81, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(BDS)
        self.pushButton_3.setGeometry(QtCore.QRect(190, 490, 81, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.InputCmd = QtWidgets.QTextEdit(BDS)
        self.InputCmd.setGeometry(QtCore.QRect(10, 450, 621, 31))
        self.InputCmd.setObjectName("InputCmd")
        self.ServerVersion = QtWidgets.QLabel(BDS)
        self.ServerVersion.setGeometry(QtCore.QRect(280, 490, 391, 21))
        self.ServerVersion.setObjectName("ServerVersion")
        self.ServerWorld = QtWidgets.QLabel(BDS)
        self.ServerWorld.setGeometry(QtCore.QRect(280, 510, 391, 16))
        self.ServerWorld.setObjectName("ServerWorld")
        self.ServerState = QtWidgets.QLabel(BDS)
        self.ServerState.setGeometry(QtCore.QRect(280, 530, 81, 16))
        self.ServerState.setObjectName("ServerState")
        self.StateBlock = QtWidgets.QLabel(BDS)
        self.StateBlock.setGeometry(QtCore.QRect(350, 530, 16, 16))
        self.StateBlock.setStyleSheet("background-color:rgb(147, 147, 147)")
        self.StateBlock.setText("")
        self.StateBlock.setObjectName("StateBlock")

        self.retranslateUi(BDS)
        QtCore.QMetaObject.connectSlotsByName(BDS)

    def retranslateUi(self, BDS):
        _translate = QtCore.QCoreApplication.translate
        BDS.setWindowTitle(_translate("BDS", "BDS Console"))
        self.pushButton.setText(_translate("BDS", "启动服务器"))
        self.pushButton_2.setText(_translate("BDS", "清除控制台"))
        self.pushButton_3.setText(_translate("BDS", "强制停止"))
        self.ServerVersion.setText(_translate("BDS", "服务器版本:"))
        self.ServerWorld.setText(_translate("BDS", "服务器存档:"))
        self.ServerState.setText(_translate("BDS", "服务器状态:"))
import image_rc
