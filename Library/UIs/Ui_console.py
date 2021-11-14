# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MCServer\Phsebot3.0\Library\UIs\console.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OutPut(object):
    def setupUi(self, OutPut):
        OutPut.setObjectName("OutPut")
        OutPut.resize(681, 551)
        OutPut.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/q/Library/Images/creative_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        OutPut.setWindowIcon(icon)
        OutPut.setToolTip("")
        OutPut.setStatusTip("")
        OutPut.setWhatsThis("")
        OutPut.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEdit = QtWidgets.QTextEdit(OutPut)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 661, 501))
        self.textEdit.setObjectName("textEdit")
        self.lineEdit = QtWidgets.QLineEdit(OutPut)
        self.lineEdit.setGeometry(QtCore.QRect(10, 520, 581, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(OutPut)
        self.pushButton.setGeometry(QtCore.QRect(600, 520, 71, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(OutPut)
        QtCore.QMetaObject.connectSlotsByName(OutPut)

    def retranslateUi(self, OutPut):
        _translate = QtCore.QCoreApplication.translate
        OutPut.setWindowTitle(_translate("OutPut", "Phsebot Console"))
        self.pushButton.setText(_translate("OutPut", "run"))
import image_rc
