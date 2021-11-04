# ==========================
# 插件加载器 By HuoHua
# ==========================
import threading
import time
myWins = 0
bots = 0
command = []
Events = {
    'PlayerJoin':[],#玩家加入 -> playername:str
    'PlayerExit':[],#玩家退出 -> playername:str
    'LoadVersion':[],#加载版本号 -> version:str
    'OpenWorld':[],#加载存档 -> world:str
    'LoadPort':[],#加载端口 -> port:int
    'ServerStarted':[],#服务器开服完成 -> 无
    'StoppingServer':[],#关服中 -> 无
    'StoppedServer':[],#服务器关服完成 ->无
    'Crash':[],#服务器崩溃 -> 无
    'StartingServer':[],#开服中 -> 无
    'ForcedStop':[],#强制停止 -> 无
    'ConsoleUpdate':[],#控制台更新 -> line:str
    'RunCmd':[],#运行命令 -> cmd:str
    'Exit':[],#程序退出 -> 无
    'Running':[]#程序开启 -> 无
}


class Logger():
    def __init__(self) -> None:
        pass

    def info(self, text):
        from Library.Tools.Logger import log_info
        log_info('[Plugin] '+text)

    def warn(self, text):
        from Library.Tools.Logger import log_warn
        log_warn('[Plugin] '+text)

    def error(self, text):
        from Library.Tools.Logger import log_error
        log_error('[Plugin] '+text)

    def debug(self, text):
        from Library.Tools.Logger import log_debug
        log_debug('[Plugin] '+text)

# 定义一个MyThread.py线程类
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
    def run(self):
        time.sleep(2)
        self.result = self.func(*self.args)
    def get_result(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None


def Init(myWin, bot):
    global myWins, bots, logger
    myWins = myWin
    bots = bot
    #加载插件
    from Plugin import loadlist
    for i in loadlist:
        logger.info(f'Loading Plugin:{i}')
    logger.info('Plugin Loader inited.')


class Rcommand():
    def __init__(self, cmd, recall):
        self.cmd = cmd
        self.recall = recall

    def check(self):
        for i in command:
            if i.cmd == self.cmd:
                return False
        else:
            return True


def runcmd(cmd:str):
    '''
    运行命令
    参数: cmd - 命令
    '''
    if myWins.on_bds.getBDSPoll():
        myWins.on_bds.Botruncmd(cmd)
        return {'code': 0}
    else:
        return {'code': 1, 'msg': 'server not running.'}


def RegCommand(cmd:str, recall):
    global command
    '''
    注册一个可以让bot调用的命令
    参数: cmd - 命令关键字
          recall - 回调函数(无需括号)
    '''
    com = Rcommand(cmd, recall)
    if com.check():
        command.append(com)
        return {'code': 0}
    else:
        return {'code': 2, 'msg': 'a same command in command list'}

#向所有群发送消息
def SendAllGroup(text:str) -> dict:
    '''向所有群发消息
    参数: text: 发送的文本
    '''
    from Library.Tools.basic import config
    for i in config['Group']:
        bots.sendGroupMsg(i,text)
    return {'code':0,'msg':'Send message success'}

#指定群发消息
def SendGroup(group:int,text:str):
    '''向指定群发消息
    参数: group: 指定的群号
          text: 发送的文本
    '''
    from Library.Tools.basic import config
    if group in config['Group']:
        bots.sendGroupMsg(group,text)
        return {'code':0,'msg':'Send message success'}
    else:
        return {'code':1,'msg':'Not Found Group'}

#注册一个事件
def regEvent(Event:str,function) -> dict:
    '''注册一个事件
    参数: Event: 事件名称
          function: 回调函数
    '''
    global Events
    if Event in Events:
        Events[Event].append(function)
        return {'code':0,'msg':'register event success'}
    else:
        return {'code':1,'msg':'Not Found '+Event}

def getlistT():
    time.sleep(0.1)
    return myWins.on_bds.Players

#返回在线的玩家列表
def getList() -> dict:
    '''返回在线的玩家列表
    '''
    runcmd('list')
    l = MyThread(getlistT)
    l.start()
    l.join()
    result = l.get_result()
    logger.debug(result)
    return result

#使用QQ号获取Xboxid
def getXboxID(qqid:int) -> str:
    '''使用QQ号获取xboxid
    :param qqid: QQ号
    注：未绑定为%Xboxid%
    '''
    from Library.Tools.basic import getQQlist,getQXlist,getXboxlist,getXboxid
    return getXboxid(qqid)

#获取已绑定的Xboxid
def getXboxList():
    '''已绑定的Xboxid'''
    from Library.Tools.basic import getXboxlist
    return getXboxlist()

#获取QQ和Xboxid对应
def getQ_XList():
    #获取QQ和Xboxid对应
    from Library.Tools.basic import getQQlist,getQXlist,getXboxlist,getXboxid
    return getQXlist()

#获取已绑定的QQ列表
def getQList():
    #获取已绑定的QQ列表
    from Library.Tools.basic import getQQlist,getQXlist,getXboxlist,getXboxid
    return getQQlist()


# 源信息
AUTHOR = 'HuoHua'
VERSION = '1.0.0'
INITFUNC = Init
logger = Logger()
from Plugin import *