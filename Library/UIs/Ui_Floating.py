# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MCServer\Phsebot3.0\Library\UIs\Floating.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedLayout, QWidget,
                             QToolBar, QToolButton, QStyle, QColorDialog, QFontDialog,
                            QVBoxLayout, QGroupBox, QRadioButton,QPushButton,QHeaderView)
from PyQt5.QtCore import QPropertyAnimation,QRect


class Ui_Float_Window(object):
    def setupUi(self, Float_Window):
        Float_Window.setObjectName("Float_Window")
        Float_Window.resize(94, 94)
        self.label = QtWidgets.QLabel(Float_Window)
        self.label.setGeometry(QtCore.QRect(13, 11, 60, 60))
        self.label.setStyleSheet("border-image:url(:/q/Library/Images/window.png)")
        self.label.setText("")
        self.label.setObjectName("label")
        self.hidden = False
        self.window_width = 94
        self.window_height = 94

        self.retranslateUi(Float_Window)
        QtCore.QMetaObject.connectSlotsByName(Float_Window)

    def retranslateUi(self, Float_Window):
        _translate = QtCore.QCoreApplication.translate
        Float_Window.setWindowTitle(_translate("Float_Window", "Form"))

    def enterEvent(self, event):
        self.hide_or_show('show', event)

    def leaveEvent(self, event):
        self.hide_or_show('hide', event)

    def hide_or_show(self, mode, event):
        # 获取窗口左上角x,y
        pos = self.frameGeometry().topLeft()
        if mode == 'show' and self.hidden:
            # 窗口左上角x + 窗口宽度 大于屏幕宽度，从右侧滑出
            if pos.x() + self.window_width >= self.screen_width:
                # 需要留10在里边，否则边界跳动
                self.startAnimation(self.screen_width - self.window_width, pos.y())
                event.accept()
                self.hidden = False
            # 窗口左上角x 小于0, 从左侧滑出
            elif pos.x() <= 0:
                self.startAnimation(0, pos.y())
                event.accept()
                self.hidden = False
            # 窗口左上角y 小于0, 从上方滑出
            elif pos.y() <= 0:
                self.startAnimation(pos.x(), 0)
                event.accept()
                self.hidden = False
        elif mode == 'hide' and (not self.hidden):
            if pos.x() + self.window_width >= self.screen_width:
                # 留10在外面
                self.startAnimation(self.screen_width - 40, pos.y(), mode, 'right')
                event.accept()
                self.hidden = True
            elif pos.x() <= 0:
                # 留10在外面
                self.startAnimation(10 - self.window_width, pos.y(), mode, 'left')
                event.accept()
                self.hidden = True
            elif pos.y() <= 0:
                # 留10在外面
                self.startAnimation(pos.x(), 40 - self.window_height, mode, 'up')
                event.accept()
                self.hidden = True

    def startAnimation(self, x, y, mode='show', direction=None):
        animation = QPropertyAnimation(self, b"geometry", self)
        # 滑出动画时长
        animation.setDuration(200)
        # 隐藏时，只留10在外边，防止跨屏
        # QRect限制其大小，防止跨屏
        num = QApplication.desktop().screenCount()
        if mode == 'hide':
            if direction == 'right':
                animation.setEndValue(QRect(x, y, 40, self.window_height))
            elif direction == 'left':
                # 多屏时采用不同的隐藏方法，防止跨屏
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(0, y, 40, self.window_height))
            else:
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(x, 0, self.window_width, 40))
        else:
            animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
        animation.start()

import image_rc
