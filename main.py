import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Library.Tools.Logger import log_debug
from Library.UIs.Ui_main import *
from Library.UIs.Ui_BDSLog import *
from Library.UIs.Ui_regular import *
from Library.UIs.Ui_crontab import *
from Library.UIs.Ui_Setting import *
from Library.UIs.Ui_xbox import *
from Library.Tools.Bot import *
from Library.Tools.basic import *
from Library.Tools.tool import *
from Library.Tools.FakePlayer import *
import subprocess
import threading
import time
import asyncio
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from Library.mcsm.http_req import startServer,stopServer,getServer,sendCmd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QStandardItemModel,QStandardItem,QTextCursor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedLayout, QWidget,
                             QToolBar, QToolButton, QStyle, QColorDialog, QFontDialog,
                            QVBoxLayout, QGroupBox, QRadioButton,QPushButton,QHeaderView)

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        #按钮事件
        self.BDS_logs.clicked.connect(self.show_panel)
        self.Regular.clicked.connect(self.show_panel)
        self.Crontab.clicked.connect(self.show_panel)
        self.Setting.clicked.connect(self.show_panel)
        self.Xbox.clicked.connect(self.show_panel)
        self.actionBDS_Logs.triggered.connect(self.show_panel)
        self.actionRegular.triggered.connect(self.show_panel)
        self.actionCrontab.triggered.connect(self.show_panel)
        self.actionXbox.triggered.connect(self.show_panel)
        self.actionSetting.triggered.connect(self.show_panel)
        self.qsl = QStackedLayout(self.Show_Content)
        #添加叠加样式
        self.on_bds = BDS()
        self.on_regular = Regular_C()
        self.on_crontab = Crontab()
        self.on_setting = Setting()
        self.on_xbox = Xbox()
        self.qsl.addWidget(self.on_bds)
        self.qsl.addWidget(self.on_regular)
        self.qsl.addWidget(self.on_crontab)
        self.qsl.addWidget(self.on_xbox)
        self.qsl.addWidget(self.on_setting)
        
    def show_panel(self):
        ojn = self.sender().objectName()
        dic = {
            "BDS_logs":0,
            "Regular":1,
            "Crontab":2,
            "Xbox":3,
            "Setting":4
        }
        dic2 = {
            "actionBDS_Logs":0,
            "actionRegular":1,
            "actionCrontab":2,
            "actionXbox":3,
            "actionSetting":4
        }
        if ojn in dic:
            index = dic[ojn]
            self.qsl.setCurrentIndex(index)
        else:
            index = dic2[ojn]
            self.qsl.setCurrentIndex(index)

class InLine(QtCore.QThread):
    updated = QtCore.pyqtSignal(str)
    def __init__(self,bds) -> None:
        super(InLine,self).__init__()
        self.bds = bds

    def out(self):
        for line in iter(self.bds.stdout.readline, b''):
            try:
                li = line.decode('UTF8').replace('\r','').replace('\n','')
            except Exception as e:
                li = line.decode('gbk').replace('\r','').replace('\n','')
            self.updated.emit(li)
            
        self.bds.stdout.close()
        self.bds.wait()

    def err(self):
        for li in iter(self.bds.stderr.readline, b''):
            try:
                li = li.decode('UTF8').replace('\n','')
            except Exception as e:
                li = li.decode('gbk').replace('\n','')
            self.updated.emit(li)
        self.err()

    def run(self):
        self.out()

class InLine_ERR(QtCore.QThread):
    updated = QtCore.pyqtSignal(str)
    def __init__(self,bds) -> None:
        super(InLine_ERR,self).__init__()
        self.bds = bds

    def err(self):
        for li in iter(self.bds.stderr.readline, b''):
            try:
                li = li.decode('UTF8').replace('\n','').replace('\r','')
            except Exception as e:
                li = li.decode('gbk').replace('\n','').replace('\r','')
            self.updated.emit(li)
        

    def run(self):
        self.err()
        

class BDS(QWidget, Ui_BDS):
    def __init__(self):
        super(BDS,self).__init__()
        # 子窗口初始化时实现子窗口布局
        self.setupUi(self)
        #链接函数
        self.RunCmd.clicked.connect(self.Runcmd)
        self.pushButton.clicked.connect(self.startServer)
        self.pushButton_2.clicked.connect(self.clean_display)
        self.pushButton_3.clicked.connect(self.forceStop)

        #设置是否可使用
        self.RunCmd.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.BDSLogs.setReadOnly(True)

        #更新一些杂项
        self.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/cancel.png)")

        self.NormalStop = False
        self.Restart = 0
        self.Port = 0
    def display(self,strs):
        self.BDSLogs.append(strs)
        self.catch_in_regular(strs)
        self.catch_regular(strs)
        self.BDSLogs.moveCursor(QTextCursor.End)
        #self.BDSLogs.moveCursor(QTextCursor.End) 

    def clean_display(self):
        self.BDSLogs.setPlainText('')

    def checkBDS(self):
        if not config['mcsm']['enable']:
            while True:
                time.sleep(1)
                if not self.getBDSPoll() and self.NormalStop == True:
                    self.display('[Phsebot] 服务端进程已停止')  
                    self.pushButton_3.setEnabled(False)
                    self.pushButton.setEnabled(True)
                    self.RunCmd.setEnabled(False)
                    self.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/cancel.png)")
                    self.StateBlock.setStyleSheet("background-color:rgb(147, 147, 147)")
                    self.ServerVersion.setText("服务器版本:")
                    self.ServerWorld.setText("服务器存档:")
                    self.ServerState.setText("服务器状态:")
                    break

                elif not self.getBDSPoll() and self.NormalStop == False and config['AutoRestart']:
                    if Language['AbendServer'] != False:
                        for i in config['Group']:
                            bot.sendGroupMsg(i,Language['AbendServer'])
                    if Language['RestartServer'] != False:
                        for i in config['Group']:
                            bot.sendGroupMsg(i,Language['RestartServer'])
                    self.display('[Phsebot] 服务端进程正在重启')
                    self.ServerVersion.setText("服务器版本:")
                    self.ServerWorld.setText("服务器存档:")
                    self.ServerState.setText("服务器状态:")
                    if config['MaxAutoRestart'] > self.Restart:
                        self.startServer()
                        self.Restart += 1
                    else:
                        if Language['MaxRestart'] != False:
                            for i in config['Group']:
                                bot.sendGroupMsg(i,Language['MaxRestart'])
                        self.Restart = 0
                    break

                elif not self.getBDSPoll() and self.NormalStop == False and config['AutoRestart'] == False:
                    if Language['AbendServer'] != False:
                        for i in config['Group']:
                            bot.sendGroupMsg(i,Language['AbendServer'])
                    self.display('[Phsebot] 服务端进程已停止')  
                    self.pushButton_3.setEnabled(False)
                    self.pushButton.setEnabled(True)
                    self.RunCmd.setEnabled(False)
                    self.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/cancel.png)")
                    self.StateBlock.setStyleSheet("background-color:rgb(147, 147, 147)")
                    self.ServerVersion.setText("服务器版本:")
                    self.ServerWorld.setText("服务器存档:")
                    self.ServerState.setText("服务器状态:")
                    break
        else:
            from Library.mcsm.http_req import startServer,stopServer,getServer,sendCmd
            while True:
                time.sleep(5)
                get = getServer(config['mcsm']['serverName'])
                if not get['status']:
                    self.display('[Phsebot] 服务端进程已停止')  
                    self.pushButton_3.setEnabled(False)
                    self.pushButton.setEnabled(True)
                    self.RunCmd.setEnabled(False)
                    self.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/cancel.png)")
                    self.StateBlock.setStyleSheet("background-color:rgb(147, 147, 147)")
                    self.ServerVersion.setText("服务器版本:")
                    self.ServerWorld.setText("服务器存档:")
                    self.ServerState.setText("服务器状态:")
                    break

    def catch_regular(self,line):
        line += '\r\n'
        useconsoleregular(myWin,bot,self.Port,line)

    def catch_in_regular(self,line):
        global Port
        line += '\r\n'
        #使用控制台正则
        try:
            updateLine = line
            #玩家退服
            if re.findall(r'^\[INFO\]\sPlayer\sdisconnected:\s(.+?),\sxuid:\s(.+?)$',updateLine) != []:
                r = re.findall(r'^\[INFO\]\sPlayer\sdisconnected:\s(.+?),\sxuid:\s(.+?)$',updateLine)
                if Language['PlayerLeft'] != False:
                    for g in config["Group"]:
                        bot.sendGroupMsg(g,Language['PlayerLeft'].replace('%player%',r[0][0]).replace(r'%xuid%',r[0][1]))

            #玩家进服
            if re.findall(r'^\[INFO\]\sPlayer\sconnected:\s(.+?),\sxuid:\s(.+?)$',updateLine) != []:
                r = re.findall(r'^\[INFO\]\sPlayer\sconnected:\s(.+?),\sxuid:\s(.+?)$',updateLine)
                if Language['PlayerJoin'] != False:
                    for g in config["Group"]:
                        bot.sendGroupMsg(g,Language['PlayerJoin'].replace('%player%',r[0][0]).replace(r'%xuid%',r[0][1]))

        except OSError as e:
            log_debug(e)
        

        #内置正则
            #版本
        if 'INFO] Version' in line:
            Version = re.findall(r'Version\s(.+?)\s',line)[0]
            self.ServerVersion.setText("服务器版本: "+Version)
            if Language['ServerVersion'] != False:
                for b in config["Group"]:
                    bot.sendGroupMsg(b,Language['ServerVersion'].replace('%Version%',Version))
            #打开世界
        if 'opening' in line:
            World = re.findall(r'opening\s(.+?)[\r\s]',line)[0]
            self.ServerWorld.setText("服务器存档: "+World)
            if Language['OpenWorld'] != False:
                for b in config["Group"]:
                    bot.sendGroupMsg(b,Language['OpenWorld'].replace('%World%',World))
            #加载端口
        if 'IPv4' in line:
            self.Port = int(re.findall(r'^\[INFO\]\sIPv4\ssupported,\sport:\s(.+?)$',line)[0])
            if Language['PortOpen'] != False:
                for b in config["Group"]:
                    bot.sendGroupMsg(b,Language['PortOpen'].replace('%Port%',str(self.Port)))

            #开服完成
        if 'Server started' in line:
            if Language['ServerStart'] != False:
                for b in config["Group"]:
                    bot.sendGroupMsg(b,Language['ServerStart'])
            #触发假人服务
            ConnectAllPlayer()
            self.Started = True
            ChangeBotName(bot,self.Port,self.Started)

            #关服中
        if '[INFO] Server stop requested.' in line:
            if Language['ServerStopping'] != False:
                for b in config["Group"]:
                    bot.sendGroupMsg(b,Language['ServerStopping'])
                self.Started = False
                ChangeBotName(bot,self.Port,self.Started)
        
        #关服完成
        if 'Quit correctly' in line:
            if Language['ServerStoped'] != False:
                for b in config["Group"]:
                    bot.sendGroupMsg(b,Language['ServerStoped'])

            #崩溃
        if 'Crashed' in line:
            if Language['Crashed'] != False:
                for b in config["Group"]:
                    bot.sendGroupMsg(b,Language['Crashed'])

    def Botruncmd(self,text:str):
        global NormalStop,Started
        result=text+'\n'
        cmd = result

        #开服
        if text == 'start':
            if not self.getBDSPoll():
                self.startServer()
            else:
                if Language['ServerRunning'] != False:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['ServerRunning'])
                    
        #正常关服
        elif text == 'stop':
            self.NormalStop = True
            DisConnectAllPlayer()
            self.Started = False
            if self.getBDSPoll():
                self.Runcmd('stop'+'\n')
            else:
                if Language['ServerNotRunning'] != False:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['ServerNotRunning'])

        #绑定XboxID
        elif 'bindid' in text:
            if '"' not in text:
                args = text.split(' ')
                try:
                    qqid = int(args[1])
                    group = int(args[-1])
                    name = args[2]
                    bind(bot,qqid,name,group)
                except:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['ArgError'])
            else:
                try:
                    args = text.split(' ')
                    qqid = int(args[1])
                    group = int(args[-1])
                    name = re.search(r'\"(.*)\"',text)[0].replace('"','')
                    bind(bot,qqid,name,group)
                except:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['ArgError'])

        #解绑XboxID
        elif 'unbind' in text:
            try:
                args = text.split(' ')
                qqid = int(args[1])
                group = int(args[-1])
                unbind(bot,qqid,group)
            except:
                for i in config['Group']:
                    bot.sendGroupMsg(i,Language['ArgError'])

        #发送卡片list
        elif 'cardlist' == text:
            if self.getBDSPoll():
                self.Runcmd('list')
                self.Runcmd('tps')
                cl = threading.Thread(target=self.cardlist)
                cl.setName('CardList')
                cl.start()
            else:
                if Language['ServerNotRunning']:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['ServerNotRunning'])

        #Motd请求
        elif 'motd' in text:
            args = text.split(' ')
            addr = ''
            port = ''
            group = int(args[-1])
            args.remove(str(group))
            #匹配域名
            for i in args:
                if re.search(r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])',i) or re.search(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+.?',i):
                    addr = i
            #赋值地址
            if ':' in addr:
                d = addr.split(':')
                addr = d[0]
                port = d[1]
            else:
                port = '19132'
            m = threading.Thread(target=motdServer,args=(bot,addr,port,group))
            m.setName('MotdServer')
            m.start()

        #输出名单
        elif 'outlist' == text:
            if self.getBDSPoll():
                self.Runcmd('list')
                self.Runcmd('tps')
                cl = threading.Thread(target=self.outList)
                cl.setName('OutList')
                cl.start()
            else:
                if Language['ServerNotRunning']:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['ServerNotRunning'])

        #解析假人命令
        elif 'FakePlayer' in text:
            args = text.split(' ')
            #获取假人名
            if '"' in text:
                name = re.search(r'\"(.*)\"',text)[0].replace('"','')
            else:
                if len(args) > 2:
                    name = args[2]
                else:
                    name = ''

            #添加假人FakePlayer add Test <Steve> <AllowChat>
            if args[1] == 'add':
                if len(args) >= 5:
                    if args[4] == 'true':
                        b = True
                    else:
                        b = False
                    AddFakePlayer(name,args[3],b)
                
                elif len(args) == 4:
                    AddFakePlayer(name,args[3])

                elif len(args) == 3:
                    AddFakePlayer(name)
                
                else:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['FakePlayerError'].replace(r'%error%','参数错误'))
            
            #移除假人FakePlayer remove Test:
            elif args[1] == 'remove':
                if len(args) == 3:
                    RemoveFakePlayer(name)
                else:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['FakePlayerError'].replace(r'%error%','参数错误'))

            #断开连接假人FakePlayer disconnect Test:
            elif args[1] == 'disconnect':
                if len(args) == 3:
                    RemoveFakePlayer(name)
                else:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['FakePlayerError'].replace(r'%error%','参数错误'))

            #连接假人
            elif args[1] == 'connect':
                if len(args) == 3:
                    ConnectPlayer(name)
                else:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['FakePlayerError'].replace(r'%error%','参数错误'))

            #设置聊天
            elif args[1] == 'setchat':
                if len(args) == 4:
                    setChatControl(name,args[3])
                elif len(args) == 3:
                    setChatControl(name)
                else:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['FakePlayerError'].replace(r'%error%','参数错误'))

            #获取状态
            elif args[1] == 'getstate':
                if len(args) == 3:
                    GetState(name)
                else:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['FakePlayerError'].replace(r'%error%','参数错误'))

            #获取所有状态
            elif args[1] == 'allstate':
                GetAllState()

            #获取所有假人
            elif args[1] == 'list':
                GetList()

            #移除所有假人
            elif args[1] == 'removeall':
                Remove_All()
        #执行指令
        else:
            self.Runcmd(text)

    def startServer(self):
        #修改变量
        self.NormalStop = False
        #对界面进行修改
        self.BDSLogs.append('[Phsebot] 正在对服务端执行开启命令')
        self.pushButton.setEnabled(False)
        self.pushButton_3.setEnabled(True)
        self.RunCmd.setEnabled(True)
        self.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/check.png)")
        self.StateBlock.setStyleSheet('background-color:rgb(75,183,75)')

        #开启进程
        self.bds = subprocess.Popen('Temp\\run.bat', stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=-1,bufsize=1,shell=True)
        
        #开启线程
        self.work = InLine(self.bds)
        self.work.start()
        self.work.updated.connect(self.display)
        self.workerr = InLine_ERR(self.bds)
        self.workerr.start()
        self.workerr.updated.connect(self.display)
        checkbds = threading.Thread(target=self.checkBDS)
        checkbds.setName('CheckBDS')
        checkbds.start()

    def forceStop(self):
        self.NormalStop = True
        #修改界面
        self.BDSLogs.append('[Phsebot] 正在对服务端执行强制停止命令')
        self.pushButton_3.setEnabled(False)
        self.pushButton.setEnabled(True)
        self.RunCmd.setEnabled(False)
        self.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/cancel.png)")
        self.StateBlock.setStyleSheet("background-color:rgb(147, 147, 147)")
        #windows终止命令
        subprocess.Popen("taskkill /F /T /PID %i" % self.bds.pid,stdout=subprocess.PIPE)
        

    def getBDSPoll(self) -> bool:
        #获取bds是否运行中
        if not config['mcsm']['enable']:
            try:
                if self.bds.poll() == None:
                    return True
                else:
                    return False
            except:
                return False
        else:
            try:
                serverstate = getServer(config['mcsm']['serverName'])
                if serverstate != {}:
                    return serverstate['status']
                else:
                    return False
            except:
                return False
    
    def getcmd(self):
        return str(self.InputCmd.toPlainText())

    def Runcmd(self,text=None) -> None:
        #运行一个bds命令
        cmd = text
        #获取命令
        if (not text):
            cmd = self.getcmd()
            self.InputCmd.setText('')
        if cmd[:4] == 'stop':
            self.NormalStop = True
        #发送命令
        if not config['mcsm']['enable']:
            if self.getBDSPoll():
                if not '\n' in cmd:
                    cmd += '\n'
                self.bds.stdin.write(cmd.encode('utf8'))
                self.bds.stdin.flush()
                if cmd == 'stop':
                    self.NormalStop = True
                    self.Started = False
            else:
                if Language['ServerNotRunning']:
                    for i in config['Group']:
                        bot.sendGroupMsg(i,Language['ServerNotRunning'])
        else:
            sendCmd(config['mcsm']['serverName'],cmd)
        

class Regular_C(QWidget,Ui_Regular):
    def __init__(self) -> None:
        super(Regular_C,self).__init__()
        self.setupUi(self)
        self.update()
        self.refrush.clicked.connect(self.update)
        self.add.clicked.connect(self.addF)
        self.deleter.clicked.connect(self.remove)
        self.pushButton.clicked.connect(self.saveF)

    def update(self):
        readFile()
        from Library.Tools.basic import config,Language,Xboxid,Regular
        self.model= QStandardItemModel(len(Regular['Regular']),4)
        self.model.setHorizontalHeaderLabels(['正则','来源','权限','操作'])
        for i in Regular['Regular']:
            re_item=QStandardItem(i['re'])
            from_item = QStandardItem(i['from'])
            perm = ''
            if i['perm']:
                perm = '管理员'
            perm_item = QStandardItem(perm)
            action_item = QStandardItem(i['action'])
            self.model.setItem(Regular['Regular'].index(i),0,re_item)
            self.model.setItem(Regular['Regular'].index(i),1,from_item)
            self.model.setItem(Regular['Regular'].index(i),2,perm_item)
            self.model.setItem(Regular['Regular'].index(i),3,action_item)

        self.tableView.setModel(self.model)
        #水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #水平方向，表格大小拓展到适当的尺寸      
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def addF(self):
       RegularX = Regular
       RegularX['Regular'].append({
            're':'',
            'from':'console',
            'perm': False,
            'action': '',
       }) 
       changeFile('Regular',RegularX)
       self.update()

    def remove(self):
        line = self.tableView.currentIndex().row()
        RegularX = Regular
        RegularX['Regular'].pop(line)
        changeFile('Regular',RegularX)
        self.update()

    def saveF(self):
        l = []
        for b in range(len(Regular['Regular'])):
            ln = []
            for i in range(4):
                new_index = self.tableView.model().index(b,i)
                ln.append(self.tableView.model().data(new_index))
            l.append(ln)
        RegularX = {'Regular':[]}
        for i in l:
            g = False
            if i[2] == '管理员':
                g = True
            RegularX['Regular'].append({
                'action': i[3],
                'from': i[1],
                'perm': g,
                're': i[0]
            }) 
        changeFile('Regular',RegularX)
        self.update()

class Crontab(QWidget,Ui_Crontab):
    def __init__(self) -> None:
        super(Crontab,self).__init__()
        self.setupUi(self)

class Setting(QWidget,Ui_Setting):
    def __init__(self) -> None:
        super(Setting,self).__init__()
        self.setupUi(self)

class Xbox(QWidget,Ui_Xbox):
    def __init__(self) -> None:
        super(Xbox,self).__init__()
        self.setupUi(self)
        self.update()
        self.refursh.clicked.connect(self.update)
        self.add.clicked.connect(self.addF)
        self.deleter.clicked.connect(self.remove)
        self.pushButton.clicked.connect(self.saveF)

    def update(self):
        readFile()
        from Library.Tools.basic import config,Language,Xboxid,Regular
        self.model= QStandardItemModel(len(Xboxid['Xbox']),3)
        self.model.setHorizontalHeaderLabels(['玩家名称','QQ号','群号'])
        for i in Xboxid['Xbox']:
            name_item=QStandardItem(i['name'])
            qq_item = QStandardItem(str(i['qq']))
            group_item = QStandardItem(str(i['group']))
            self.model.setItem(Xboxid['Xbox'].index(i),0,name_item)
            self.model.setItem(Xboxid['Xbox'].index(i),1,qq_item)
            self.model.setItem(Xboxid['Xbox'].index(i),2,group_item)

        self.tableView.setModel(self.model)
        #self.tableView.setModel(self.editdata)
        #水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #水平方向，表格大小拓展到适当的尺寸      
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def addF(self):
       XboxidX = Xboxid
       Xboxid['Xbox'].append({
            'group': config['Group'][0],
            'name':'',
            'qq': 123456
       }) 
       changeFile('Xboxid',XboxidX)
       self.update()

    def remove(self):
        line = self.tableView.currentIndex().row()
        XboxidX = Xboxid
        XboxidX['Xbox'].pop(line)
        changeFile('Xboxid',XboxidX)
        self.update()

    def saveF(self):
        l = []
        for b in range(len(Xboxid['Xbox'])):
            ln = []
            for i in range(3):
                new_index = self.tableView.model().index(b,i)
                ln.append(self.tableView.model().data(new_index))
            l.append(ln)
        XboxidX = {'Xbox':[]}
        for i in l:
            try:
                gr = int(i[2])
            except:
                gr = config['Group'][0]

            try:
                qq = int(i[1])
            except:
                qq = 0
            XboxidX['Xbox'].append({
                'group': gr,
                'name': i[0],
                'qq': qq
            }) 
        changeFile('Xboxid',XboxidX)
        self.update()

if __name__ == '__main__':
    #写入路径
    WriteStartBat()
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    bot = Bot()
    bot.login(bot,myWin)
    os._exit(app.exec_())
