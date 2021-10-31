from os import write
import yaml
import json
from Library.Tools.motd import Server
from PyQt5.QtWidgets import QPushButton,QMessageBox
from Library.Tools.tool import WriteYaml
from Library.Tools.Logger import *
import re
from datetime import datetime
import time
import psutil
import urllib3
import webbrowser
Bot_Version = 'v3.0.1'

def read_file(file):
    with open(file,'r',encoding='utf-8') as f:
        if '.json' in file:
            content = f.read().replace('\/n','\n')
            return json.loads(content)
        elif '.yml' in file:
            content = f.read().replace('\/n','\n')

            return yaml.load(content, Loader=yaml.FullLoader)

def WriteStartBat(window):
    global windows
    windows = window
    file_content = f'''@echo off
cd {config['ServerPath']}
{config['ServerPath'][0]}:
{config['ServerCmd']}
'''
    if config['AutoWrite']:
        with open('Temp/run.bat','w',encoding='UTF8') as f:
            f.write(file_content)

def ChangeBotName(bot,Port,Started):
    if Started:
        Motd = Server('127.0.0.1',int(Port)).motd()
        if Motd['status'] == 'online':
            server_online = Motd['online']
            server_maxonline = Motd['upperLimit']
            for i in config['Group']:
                bot.changeName(config['Bot'],i,config['AutoChangeBotName']['String'].replace(r'%Online%',str(server_online))\
                    .replace(r'%Max%',str(server_maxonline)))
    else:
        if config['AutoChangeBotName']['StopReset'] != False:
            for i in config['Group']:
                bot.changeName(config['Bot'],i,config['AutoChangeBotName']['StopReset'])

def getRegular(type='All'):
    dic = {'console':[],'group':[]}
    for i in Regular['Regular']:
        if i['from'] == 'console':
            dic['console'].append(i)
        elif i['from'] == 'group':
            dic['group'].append(i)
    if type == 'All':
        return dic
    elif type == 'console':
        return {'console':dic['console']}
    elif type == 'group':
        return {'group':dic['group']}

def get_week_t():
  week_day_dict = {
    0 : '一',
    1 : '二',
    2 : '三',
    3 : '四',
    4 : '五',
    5 : '六',
    6 : '天',
  }
  day = datetime.now().weekday()
  return week_day_dict[day]

def get_week_j():
  week_day_dict = {
    0 : '日',
    1 : '月',
    2 : '火',
    3 : '水',
    4 : '木',
    5 : '金',
    6 : '土',
  }
  day = datetime.now().weekday()
  return week_day_dict[day]

def getAPM():
    h = int(datetime.now().strftime('%H'))
    if h < 12:
        return 'AM'
    else:
        return 'PM'

#获取cpu状态
cpup = 0
def getcpupercent():
    global cpup
    while True:
        psutil.cpu_percent(None)
        time.sleep(0.5)
        cpup = str(psutil.cpu_percent(None))
        time.sleep(2)

def getXboxid(qq):
    #自动以qq号查找xboxid
    for i in Xboxid['Xbox']:
        if qq == i['qq']:
            return i['name']
    return r'%xboxid%'

def getQQlist():
    #获取已绑定的qq列表
    l = []
    for i in Xboxid['Xbox']:
        l.append(i['qq'])
    return l

def getQXlist():
    #获取对应列表
    l = []
    for i in Xboxid['Xbox']:
        l.append({'qq':i['qq'],'id':i['name']})
    return l

def getXboxlist():
    l = []
    for i in Xboxid['Xbox']:
        l.append(i['name'])
    return l


def replaceconsole(Port,string):
    motdinfo = Server('127.0.0.1',int(Port)).motd()
    if motdinfo['status'] == 'online':
        server_motd = motdinfo['name']
        server_version = motdinfo['version']
        server_online = motdinfo['online']
        server_maxonline = motdinfo['upperLimit']
        server_levelname = motdinfo['save']
    else:
        server_motd = '服务器未启动'
        server_version = '服务器未启动'
        server_online = '0'
        server_maxonline = '0'
        server_levelname = '服务器未启动'
    # 系统的CPU利用率
    cpu = str(cpup)+'%'
    mem = psutil.virtual_memory()
    ram_1 = str(mem.total)+'%'
    ram_2 = str(int((mem.free/1024)/1024))+'MB'
    ram_3 = str(int((mem.used/1024)/1024))+'MB'
    ram_4 = str(mem.percent)+'%'
    #时间类
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    hour_12 = str(int(datetime.now().strftime('%H'))-12)
    hour_24 = datetime.now().strftime('%H')
    week_n = str(datetime.now().weekday()+1)
    week_t = get_week_t()
    week_j = get_week_j()
    day = datetime.now().strftime('%d')
    APM = getAPM()
    mins = datetime.now().strftime('%M')
    sec = datetime.now().strftime('%S')
    s = string.replace(r'%cpu%',cpu)\
        .replace(r'%ram_1%',ram_1)\
        .replace(r'%ram_2%',ram_2)\
        .replace(r'%ram_3%',ram_3)\
        .replace(r'%ram_4%',ram_4)\
        .replace(r'%server_motd%',server_motd)\
        .replace(r'%server_version%',server_version)\
        .replace(r'%server_online%',server_online)\
        .replace(r'server_maxonline',server_maxonline)\
        .replace(r'%server_levelname%',server_levelname)\
        .replace('\\n','\n')\
        .replace(r'%date%',date)\
        .replace(r'%time%',time)\
        .replace(r'%year%',year)\
        .replace(r'%month%',month)\
        .replace(r'%week_n%',week_n)\
        .replace(r'%week_t%',week_t)\
        .replace(r'%week_j%',week_j)\
        .replace(r'%day%',day)\
        .replace(r'%hour_12%',hour_12)\
        .replace(r'%hour_24%',hour_24)\
        .replace(r'%ampm%',APM)\
        .replace(r'%min%',mins)\
        .replace(r'%sec%',sec)
    return s

def replaceRE(re_list,action):
    l = []
    for i in re_list:
        if type(i) == tuple:
            for t in i:
                l.append(t)
        elif type(i) == str:
            l.append(i)
    for i in range(1,len(l)+1):
        action = action.replace('$'+str(i),l[i-1])
    return action

#控制台正则匹配
def useconsoleregular(myWin,bot,Port,text):
    regular = getRegular('console')
    for i in regular['console']:
        p = re.findall(i['re'],text)
        #执行操作
        if p != []:
            cmd = replaceRE(p,i['re'])
            #发群消息
            rps = replaceconsole(Port,cmd[2:])
            if i['action'][:2] == '>>':
                for g in config["Group"]:
                    bot.sendGroupMsg(g,rps)
            #执行命令
            elif i['action'][:2] == '<<':
                myWin.on_bds.Botruncmd(i['action'][:2]+'\n')

def replacegroup(Port,string,qqnick,qqid):
    motdinfo = Server('localhost',int(Port)).motd()
    if motdinfo['status'] == 'online':
        server_motd = motdinfo['name']
        server_version = motdinfo['version']
        server_online = motdinfo['online']
        server_maxonline = motdinfo['upperLimit']
        server_levelname = motdinfo['save']
    else:
        server_motd = '服务器未启动'
        server_version = '服务器未启动'
        server_online = '0'
        server_maxonline = '0'
        server_levelname = '服务器未启动'
    # 系统的CPU利用率
    cpu = str(cpup)+'%'
    mem = psutil.virtual_memory()
    ram_1 = str(mem.total)+'%'
    ram_2 = str(int((mem.free/1024)/1024))+'MB'
    ram_3 = str(int((mem.used/1024)/1024))+'MB'
    ram_4 = str(mem.percent)+'%'
    xboxid = getXboxid(qqid)
    #时间类
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    hour_12 = str(int(datetime.now().strftime('%H'))-12)
    hour_24 = datetime.now().strftime('%H')
    week_n = str(datetime.now().weekday()+1)
    week_t = get_week_t()
    week_j = get_week_j()
    day = datetime.now().strftime('%d')
    APM = getAPM()
    mins = datetime.now().strftime('%M')
    sec = datetime.now().strftime('%S')
    #替换文本
    s = string.replace(r'%qqnick%',qqnick)\
        .replace(r'%qqid%',str(qqid))\
        .replace(r'%xboxid%',xboxid)\
        .replace(r'%cpu%',cpu)\
        .replace(r'%ram_1%',ram_1)\
        .replace(r'%ram_2%',ram_2)\
        .replace(r'%ram_3%',ram_3)\
        .replace(r'%ram_4%',ram_4)\
        .replace(r'%server_motd%',server_motd)\
        .replace(r'%server_version%',server_version)\
        .replace(r'%server_online%',server_online)\
        .replace(r'%server_maxonline%',server_maxonline)\
        .replace(r'%server_levelname%',server_levelname)\
        .replace('\\n','\n')\
        .replace(r'%date%',date)\
        .replace(r'%time%',time)\
        .replace(r'%year%',year)\
        .replace(r'%month%',month)\
        .replace(r'%week_n%',week_n)\
        .replace(r'%week_t%',week_t)\
        .replace(r'%week_j%',week_j)\
        .replace(r'%day%',day)\
        .replace(r'%hour_12%',hour_12)\
        .replace(r'%hour_24%',hour_24)\
        .replace(r'%ampm%',APM)\
        .replace(r'%min%',mins)\
        .replace(r'%sec%',sec)
    return s

def changeFile(file,dic):
    global config,Language,Regular,Xboxid
    if file == 'config':
        config = dic
        WriteYaml('data/config.yml',config)
        WriteStartBat(windows)
    elif file == 'Language':
        Language = dic
        WriteYaml('data/Language.yml',config)
    elif file == 'Regular':
        Regular = dic
        WriteYaml('data/regular.yml',Regular)
    elif file == 'Xboxid':
        Xboxid = dic
        WriteYaml('data/xbox.yml',Xboxid)
    elif file == 'Crontab':
        from Library.Tools.Crontab import crontab
        Crontab = dic
        crontab()
        WriteYaml('data/crontab.yml',Crontab)

class Update():
    def __init__(self) -> None:
        pass

    def showEvent(self, body):
        quitMsgBox = QMessageBox()
        quitMsgBox.setWindowTitle('Phsebot - 更新提示')
        version = body['tag_name']
        bodys = body['body'].replace('\\r','\r').replace('\\n','\n')
        quitMsgBox.setText(f'Phsebot发现新版本\n版本号:{version}\n更新内容:\n\n{bodys}')
        buttonY = QPushButton('确定')
        buttonN = QPushButton('取消')
        quitMsgBox.addButton(buttonY, QMessageBox.YesRole)
        quitMsgBox.addButton(buttonN, QMessageBox.NoRole)
        quitMsgBox.exec_()
        if quitMsgBox.clickedButton() == buttonY:
            webbrowser.open('https://hub.fastgit.org/HuoHuas001/Phsebot3.0/releases/latest')


    def checkUpdate(self):
        log_info('正在检查更新...')
        http = urllib3.PoolManager()
        # get请求指定网址
        url = "https://api.github.com/repos/HuoHuas001/Phsebot3.0/releases/latest"
        res = http.request("GET",url)
        #检测是否请求成功
        if res.status == 200:
            data = json.loads(res.data.decode("utf-8"))
            if Bot_Version != data["tag_name"]:
                self.showEvent(data)
        else:
            log_warn(f'检测更新时出了问题{res.status}')


def readFile():
    global config,Language,Regular,Xboxid,Crontab
    config = read_file('data/config.yml')
    Language = read_file('data/Language.yml')
    Regular = read_file('data/regular.yml')
    Xboxid = read_file('data/xbox.yml')
    Crontab = read_file('data/crontab.yml')

readFile()
