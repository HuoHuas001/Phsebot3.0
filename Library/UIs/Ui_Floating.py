# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MCServer\Phsebot3.0\Library\UIs\Floating.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Float_Window(object):
    def setupUi(self, Float_Window):
        Float_Window.setObjectName("Float_Window")
        Float_Window.resize(60, 60)
        self.label = QtWidgets.QLabel(Float_Window)
        self.label.setGeometry(QtCore.QRect(0, 0, 60, 60))
        self.label.setMinimumSize(QtCore.QSize(60, 60))
        self.label.setMaximumSize(QtCore.QSize(60, 60))
        self.label.setStyleSheet("border-image:url(:/q/Library/Images/window.png)")
        self.label.setText("")
        self.label.setObjectName("label")

        self.retranslateUi(Float_Window)
        QtCore.QMetaObject.connectSlotsByName(Float_Window)

    def retranslateUi(self, Float_Window):
        _translate = QtCore.QCoreApplication.translate
        Float_Window.setWindowTitle(_translate("Float_Window", "Form"))
import image_rc
