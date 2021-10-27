# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MCServer\Phsebot3.0\Library\UIs\main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton,QMessageBox
from Library.UIs.Ui_Floating import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(775, 600)
        MainWindow.setMinimumSize(QtCore.QSize(775, 600))
        MainWindow.setMaximumSize(QtCore.QSize(775, 600))
        font = QtGui.QFont()
        font.setFamily("HarmonyOS Sans SC")
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/q/Library/Images/window.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 71, 581))
        self.widget.setStyleSheet("background-color:#ff5558;")
        self.widget.setObjectName("widget")
        self.BDS_logs = QtWidgets.QPushButton(self.widget)
        self.BDS_logs.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.BDS_logs.setStyleSheet("border-image:url(:/q/Library/Images/creative_icon.png)")
        self.BDS_logs.setText("")
        self.BDS_logs.setObjectName("BDS_logs")
        self.Regular = QtWidgets.QPushButton(self.widget)
        self.Regular.setGeometry(QtCore.QRect(10, 80, 51, 51))
        self.Regular.setStyleSheet("border-image:url(:/q/Library/Images/ChainSquare.png)")
        self.Regular.setText("")
        self.Regular.setObjectName("Regular")
        self.Crontab = QtWidgets.QPushButton(self.widget)
        self.Crontab.setGeometry(QtCore.QRect(10, 150, 51, 51))
        self.Crontab.setStyleSheet("border-image:url(:/q/Library/Images/clock_item.png)")
        self.Crontab.setText("")
        self.Crontab.setObjectName("Crontab")
        self.Setting = QtWidgets.QPushButton(self.widget)
        self.Setting.setGeometry(QtCore.QRect(10, 520, 51, 51))
        self.Setting.setStyleSheet("border-image:url(:/q/Library/Images/icon_setting.png)")
        self.Setting.setText("")
        self.Setting.setObjectName("Setting")
        self.Xbox = QtWidgets.QPushButton(self.widget)
        self.Xbox.setGeometry(QtCore.QRect(10, 220, 51, 51))
        self.Xbox.setStyleSheet("border-image:url(:/q/Library/Images/xbox.png)")
        self.Xbox.setText("")
        self.Xbox.setObjectName("Xbox")
        self.Show_Content = QtWidgets.QFrame(self.centralwidget)
        self.Show_Content.setGeometry(QtCore.QRect(80, 10, 681, 551))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setBold(False)
        font.setWeight(50)
        self.Show_Content.setFont(font)
        self.Show_Content.setStyleSheet("")
        self.Show_Content.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Show_Content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Show_Content.setObjectName("Show_Content")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 775, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuMirai = QtWidgets.QMenu(self.menubar)
        self.menuMirai.setObjectName("menuMirai")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionReconnect = QtWidgets.QAction(MainWindow)
        self.actionReconnect.setObjectName("actionReconnect")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionBDS_Logs = QtWidgets.QAction(MainWindow)
        self.actionBDS_Logs.setObjectName("actionBDS_Logs")
        self.actionRegular = QtWidgets.QAction(MainWindow)
        self.actionRegular.setObjectName("actionRegular")
        self.actionConsole = QtWidgets.QAction(MainWindow)
        self.actionConsole.setObjectName("actionConsole")
        self.actionCrontab = QtWidgets.QAction(MainWindow)
        self.actionCrontab.setObjectName("actionCrontab")
        self.actionXbox = QtWidgets.QAction(MainWindow)
        self.actionXbox.setObjectName("actionXbox")
        self.actionSetting = QtWidgets.QAction(MainWindow)
        self.actionSetting.setObjectName("actionSetting")
        self.menu.addAction(self.actionAbout)
        self.menuMirai.addAction(self.actionReconnect)
        self.menuMirai.addAction(self.actionDisconnect)
        self.menu_2.addAction(self.actionBDS_Logs)
        self.menu_2.addAction(self.actionRegular)
        self.menu_2.addAction(self.actionCrontab)
        self.menu_2.addAction(self.actionXbox)
        self.menu_2.addAction(self.actionSetting)
        self.menu_2.addSeparator()
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuMirai.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Phsebot"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.menuMirai.setTitle(_translate("MainWindow", "Mirai"))
        self.menu_2.setTitle(_translate("MainWindow", "视图"))
        self.actionAbout.setText(_translate("MainWindow", "关于"))
        self.actionReconnect.setText(_translate("MainWindow", "重连"))
        self.actionDisconnect.setText(_translate("MainWindow", "断开连接"))
        self.actionBDS_Logs.setText(_translate("MainWindow", "服务器控制台"))
        self.actionRegular.setText(_translate("MainWindow", "正则表达式"))
        self.actionConsole.setText(_translate("MainWindow", "Console"))
        self.actionCrontab.setText(_translate("MainWindow", "定时任务"))
        self.actionXbox.setText(_translate("MainWindow", "Xbox名称"))
        self.actionSetting.setText(_translate("MainWindow", "设置"))

    def closeEvent(self, event):
        # 创建一个消息盒子（提示框）
        quitMsgBox = QMessageBox()
        # 设置提示框的标题
        quitMsgBox.setWindowTitle('Phsebot - 警告')
        # 设置提示框的内容
        quitMsgBox.setText('你确定退出吗？')
        # 创建两个点击的按钮，修改文本显示内容
        buttonY = QPushButton('确定')
        buttonN = QPushButton('取消')
        # 将两个按钮加到这个消息盒子中去，并指定yes和no的功能
        quitMsgBox.addButton(buttonY, QMessageBox.YesRole)
        quitMsgBox.addButton(buttonN, QMessageBox.NoRole)
        quitMsgBox.exec_()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/q/Library/Images/window.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        quitMsgBox.setWindowIcon(icon)
        # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
        if quitMsgBox.clickedButton() == buttonY:
            if self.safe_exit():
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

import image_rc
