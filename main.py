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
from Library.Tools.Crontab import *
from Library.Tools.FakePlayer import *
from Library.UIs.Window import *
import subprocess
import threading
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from Library.mcsm.http_req import startServer,stopServer,getServer,sendCmd
from PyQt5.QtCore import Qt,QPoint,QPropertyAnimation,QRect
from PyQt5.QtGui import QIcon,QStandardItemModel,QStandardItem,QTextCursor,QMouseEvent
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedLayout, QWidget,
                             QToolBar, QToolButton, QStyle, QColorDialog, QFontDialog,
                            QVBoxLayout, QGroupBox, QRadioButton,QPushButton,QHeaderView,)

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        #Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
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
        self.actionAbout.triggered.connect(self.showAbout)
        self.qsl = QStackedLayout(self.Show_Content)
        self.initFloating()
        #添加叠加样式
        self.on_bds = BDS()
        self.on_regular = Regular_C()
        self.on_crontab = Crontab_C()
        self.on_setting = Setting()
        self.on_xbox = Xbox()
        self.qsl.addWidget(self.on_bds)
        self.qsl.addWidget(self.on_regular)
        self.qsl.addWidget(self.on_crontab)
        self.qsl.addWidget(self.on_xbox)
        self.qsl.addWidget(self.on_setting)

    def showAbout(self):
        QMessageBox.about(self,"关于Phsebot",f"作者:HuoHuaCore\n版本:{Bot_Version}\nEmail:2351078777@qq.com\n发现任何问题可以发issue或邮件")

    def safe_exit(self):
        try:
            if self.on_bds.getBDSPoll():
                self.on_bds.Runcmd('stop')
                #time.sleep(3)
                return True
            else:
                return True
        except Exception as e:
            log_debug(e)
            return False

    def initFloating(self):
        screen_width = app.primaryScreen().geometry().width()
        screen_height = app.primaryScreen().geometry().height()
        self.floating = Floating()
        self.floating.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.floating.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        window_width = 94
        window_height = 94
        self.floating.setGeometry(screen_width - window_width - 10, screen_height//2 - 150, window_width, window_height)


    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                self.floating.show()
            if self.windowState() == Qt.WindowNoState:
                self.floating.close()
        
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

class InLine_P(QtCore.QThread):
    updated = QtCore.pyqtSignal(str)
    def __init__(self,bds) -> None:
        super(InLine_P,self).__init__()
        self.bds = bds

    def checkBDS(self):
        if not config['mcsm']['enable']:
            while True:
                time.sleep(1)
                if not self.bds.getBDSPoll() and self.bds.NormalStop == True:
                    self.bds.display('[Phsebot] 服务端进程已停止')  
                    self.bds.pushButton_3.setEnabled(False)
                    self.bds.pushButton.setEnabled(True)
                    self.bds.RunCmd.setEnabled(False)
                    self.bds.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/cancel.png)")
                    self.bds.StateBlock.setStyleSheet("border-radius:5px;padding:2px 4px;background-color:rgb(147,147,147);")
                    self.bds.ServerVersion.setText("服务器版本:")
                    self.bds.ServerWorld.setText("服务器存档:")
                    self.bds.ServerState.setText("服务器状态:")
                    myWin.setWindowTitle('Phsebot')
                    break

                elif not self.bds.getBDSPoll() and self.bds.NormalStop == False and config['AutoRestart']:
                    if Language['AbendServer'] != False:
                        for i in config['Group']:
                            bot.sendGroupMsg(i,Language['AbendServer'])
                    if Language['RestartServer'] != False:
                        for i in config['Group']:
                            bot.sendGroupMsg(i,Language['RestartServer'])
                    self.bds.display('[Phsebot] 服务端进程正在重启')
                    self.bds.ServerVersion.setText("服务器版本:")
                    self.bds.ServerWorld.setText("服务器存档:")
                    self.bds.ServerState.setText("服务器状态:")
                    myWin.setWindowTitle('Phsebot')
                    if config['MaxAutoRestart'] > self.bds.Restart:
                        self.bds.startServer()
                        self.bds.Restart += 1
                    else:
                        if Language['MaxRestart'] != False:
                            for i in config['Group']:
                                bot.sendGroupMsg(i,Language['MaxRestart'])
                        self.bds.Restart = 0
                    break

                elif not self.bds.getBDSPoll() and self.bds.NormalStop == False and config['AutoRestart'] == False:
                    if Language['AbendServer'] != False:
                        for i in config['Group']:
                            bot.sendGroupMsg(i,Language['AbendServer'])
                    self.bds.display('[Phsebot] 服务端进程已停止')  
                    self.bds.pushButton_3.setEnabled(False)
                    self.bds.pushButton.setEnabled(True)
                    self.bds.RunCmd.setEnabled(False)
                    self.bds.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/cancel.png)")
                    self.bds.StateBlock.setStyleSheet("border-radius:5px;padding:2px 4px;background-color:rgb(147,147,147);")
                    self.bds.ServerVersion.setText("服务器版本:")
                    self.bds.ServerWorld.setText("服务器存档:")
                    self.bds.ServerState.setText("服务器状态:")
                    myWin.setWindowTitle('Phsebot')
                    break
        else:
            from Library.mcsm.http_req import startServer,stopServer,getServer,sendCmd
            while True:
                time.sleep(5)
                get = getServer(config['mcsm']['serverName'])
                if not get['status']:
                    self.bds.display('[Phsebot] 服务端进程已停止')  
                    self.bds.pushButton_3.setEnabled(False)
                    self.bds.pushButton.setEnabled(True)
                    self.bds.RunCmd.setEnabled(False)
                    self.bds.RunCmd.setStyleSheet("border-image:url(:/q/Library/Images/cancel.png)")
                    self.bds.StateBlock.setStyleSheet("border-radius:5px;padding:2px 4px;background-color:rgb(147,147,147);")
                    self.bds.ServerVersion.setText("服务器版本:")
                    self.bds.ServerWorld.setText("服务器存档:")
                    self.bds.ServerState.setText("服务器状态:")
                    break
        

    def run(self):
        self.checkBDS()
        

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
        self.Version = ''
        self.World = ''
        self.Players = {
            "Now":0,
            "Max":0,
            "Player":[],
            "tps":20.0
        }
        self.lastLine = ''

    def display(self,strs):
        self.BDSLogs.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.BDSLogs.append(strs)
        self.catch_in_regular(strs)
        self.catch_regular(strs)
        self.BDSLogs.moveCursor(QTextCursor.End)
        #self.BDSLogs.moveCursor(QTextCursor.End) 

    def clean_display(self):
        self.BDSLogs.setPlainText('')


    def catch_regular(self,line):
        line += '\r\n'
        useconsoleregular(myWin,bot,self.Port,line)

        #记录list
        lists = re.findall(r'^There\sare\s(.+?)\/(.+?)\splayers',line)
        if lists != []:
            self.lastLine = line
            self.Players['Now'] = lists[0][0]
            self.Players['Max'] = lists[0][1]

        if 'There are ' in self.lastLine:
            self.Players['Player'] = line.replace('\r\n','').split(', ')

        if '[INFO] TPS:' in line:
            self.Players['tps'] = float(line.replace('[INFO] TPS:','').replace('\r\n',''))


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
            self.Version = re.findall(r'Version\s(.+?)\s',line)[0]
            self.ServerVersion.setText("服务器版本: "+self.Version)
            if Language['ServerVersion'] != False:
                for b in config["Group"]:
                    bot.sendGroupMsg(b,Language['ServerVersion'].replace('%Version%',self.Version))
            #打开世界
        if 'opening' in line:
            self.World = re.findall(r'opening\s(.+?)[\r\s]',line)[0].replace('worlds/','')
            self.ServerWorld.setText("服务器存档: "+self.World)
            if Language['OpenWorld'] != False:
                for b in config["Group"]:
                    bot.sendGroupMsg(b,Language['OpenWorld'].replace('%World%',self.World))
            #加载端口
        if 'IPv4' in line:
            port_re = re.findall(r'INFO\]\sIPv4\ssupported,\sport:\s(.+?)$',line)
            self.Port = int(port_re[0])
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
            myWin.setWindowTitle('Phsebot - '+self.World+' '+self.Version)

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
    #输出list名单
    def outList(self):
        time.sleep(1)
        if Language['OnlineList'] != False:
            pl = ''
            for i in self.Players['Player']:
                if(pl == ''):
                    pl += i
                else:
                    pl += ' '+i
            l = Language['OnlineList'].replace(r'%Online%',str(self.Players['Now'])).replace(r'%Max%',str(self.Players['Max'])).replace(r'%Player%',pl)
            for i in config['Group']:
                bot.sendGroupMsg(i,l)

    def cardlist(self):
        time.sleep(1)
        if config['ServerInfoCard']['Enable']:
            card = config['ServerInfoCard']['CardJson']
            #改变
            card = card.replace('%Online%',str(self.Players['Now']))
            card = card.replace('%Max%',str(self.Players["Max"]))
            card = card.replace('%Tps%',str(self.Players['tps']))
            pl = ''
            for i in self.Players['Player']:
                if(pl == ''):
                    pl += i
                else:
                    pl += ' '+i
            card = card.replace('%Players%',pl)
            #替换logo
            if config['ServerInfoCard']['Logo'] != '':
                card = card.replace(r'%Logo%','https:\/\/z3.ax1x.com\/2021\/09\/09\/hOPbZQ.png')
            else:
                card = card.replace(r'%Logo%',config['ServerInfoCard']['Logo'])
            for i in config['Group']:
                bot.send_app(i,card)

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
        self.StateBlock.setStyleSheet('border-radius:5px;padding:2px 4px;background-color:rgb(75,183,75);')

        #开启进程
        self.bds = subprocess.Popen('Temp\\run.bat', stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=-1,bufsize=1,shell=True)
        
        #开启线程
        self.work = InLine(self.bds)
        self.work.start()
        self.work.updated.connect(self.display)
        self.workerr = InLine_ERR(self.bds)
        self.workerr.start()
        self.workerr.updated.connect(self.display)

        #开启进程检查线程
        self.pro = InLine_P(myWin.on_bds)
        self.pro.start()
        self.pro.updated.connect(self.display)

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
        if line != -1:
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

class Crontab_C(QWidget,Ui_Crontab):
    def __init__(self) -> None:
        super(Crontab_C,self).__init__()
        self.setupUi(self)
        self.update()
        self.refrusher.clicked.connect(self.update)
        self.deleter.clicked.connect(self.remove)
        self.newer.clicked.connect(self.addF)
        self.save.clicked.connect(self.saveF)

    def update(self):
        readFile()
        from Library.Tools.basic import config,Language,Xboxid,Regular
        self.model= QStandardItemModel(len(Crontab['Crontab']),2)
        self.model.setHorizontalHeaderLabels(['表达式','操作'])
        for i in Crontab['Crontab']:
            cr_item=QStandardItem(i['crontab'])
            action_item = QStandardItem(i['action'])
            self.model.setItem(Crontab['Crontab'].index(i),0,cr_item)
            self.model.setItem(Crontab['Crontab'].index(i),1,action_item)

        self.tableView.setModel(self.model)
        #水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #水平方向，表格大小拓展到适当的尺寸      
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def addF(self):
        CrontabX = Crontab
        Crontab['Crontab'].append({
            'crontab': '*/5 * * * *',
            'action': '>>say hello'
        }) 
        changeFile('Crontab',CrontabX)
        self.update()

    def remove(self):
        line = self.tableView.currentIndex().row()
        if line != -1:
            CrontabX = Crontab
            CrontabX['Crontab'].pop(line)
            changeFile('Crontab',CrontabX)
            self.update()

    def saveF(self):
        l = []
        for b in range(len(Crontab['Crontab'])):
            ln = []
            for i in range(2):
                new_index = self.tableView.model().index(b,i)
                ln.append(self.tableView.model().data(new_index))
            l.append(ln)
        CrontabX = {'Crontab':[]}
        for i in l:
            CrontabX['Crontab'].append({
                'crontab': i[0],
                'action': i[1],
            }) 
        changeFile('Crontab',CrontabX)
        self.update()

class Setting(QWidget,Ui_Setting):
    def __init__(self) -> None:
        super(Setting,self).__init__()
        self.setupUi(self)
        self.toolButton.clicked.connect(self.open_file)
        self.update()

    def open_file(self):
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), 
        "All Files(*)")
        filepath,tempfilename = os.path.split(fileName)
        filepath = filepath.replace('/','\\')
        configc = config
        configc['ServerCmd'] = tempfilename
        configc['ServerPath'] = filepath
        changeFile('config',configc)
        self.update()
    
    def update(self):
        path = config['ServerPath']
        if path[-1] != '\\':
            path += '\\'
        self.lineEdit.setText(path+config['ServerCmd'])


class Floating(QWidget,Ui_Float_Window):
    def __init__(self) -> None:
        super(Floating,self).__init__()
        self.setupUi(self)
        self.setCursor(Qt.PointingHandCursor)
        dsk = QApplication.primaryScreen()
        self.screen_width = dsk.geometry().width()
        self.screen_height = dsk.geometry().height()
        self.hidden = False
        self.window_width = 60
        self.window_height = 60

    def mouseDoubleClickEvent(self, e):   # 双击
        state = myWin.windowState()
        if state == Qt.WindowMinimized:
            myWin.setWindowState(Qt.WindowNoState)
            self.close()

    #鼠标按下时，记录鼠标相对窗口的位置
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._startPos = event.pos()

    # 鼠标移动时，移动窗口跟上鼠标；同时限制窗口位置，不能移除主屏幕
    def mouseMoveEvent(self, event: QMouseEvent):
        # event.pos()减去最初相对窗口位置，获得移动距离(x,y)
        self._wmGap = event.pos() - self._startPos
        # 移动窗口，保持鼠标与窗口的相对位置不变
        # 检查是否移除了当前主屏幕
        # 左方界限
        final_pos = self.pos() + self._wmGap
        if self.frameGeometry().topLeft().x() + self._wmGap.x() <= 0:
            final_pos.setX(0)
        # 上方界限
        if self.frameGeometry().topLeft().y() + self._wmGap.y() <= 0:
            final_pos.setY(0)
        # 右方界限
        if self.frameGeometry().bottomRight().x() + self._wmGap.x() >= self.screen_width:
            final_pos.setX(self.screen_width - self.window_width)
        # 下方界限
        if self.frameGeometry().bottomRight().y() + self._wmGap.y() >= self.screen_height:
            final_pos.setY(self.screen_height - self.window_height)
        self.move(final_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        pass

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
                self.startAnimation(self.screen_width - 10, pos.y(), mode, 'right')
                event.accept()
                self.hidden = True
            elif pos.x() <= 0:
                # 留10在外面
                self.startAnimation(10 - self.window_width, pos.y(), mode, 'left')
                event.accept()
                self.hidden = True
            elif pos.y() <= 0:
                # 留10在外面
                self.startAnimation(pos.x(), 10 - self.window_height, mode, 'up')
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
                animation.setEndValue(QRect(x, y, 10, self.window_height))
            elif direction == 'left':
                # 多屏时采用不同的隐藏方法，防止跨屏
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(0, y, 10, self.window_height))
            else:
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(x, 0, self.window_width, 10))
        else:
            animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
        animation.start()

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
        if line != -1:
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
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    bot = Bot()
    bot.login(bot,myWin)
    myWin.actionReconnect.triggered.connect(bot.tReconnect)
    myWin.actionDisconnect.triggered.connect(bot.disconnect)
    #写入启动bat
    WriteStartBat(myWin)
    #执行Crontab任务
    if config['EnableCron']:
        crontab()
        crontab_thread = threading.Thread(target=runcron,args=(bot,myWin))
        crontab_thread.setDaemon(True)
        crontab_thread.setName('Crontab')
        crontab_thread.start()
    update = Update()
    update.checkUpdate()
    os._exit(app.exec_())
