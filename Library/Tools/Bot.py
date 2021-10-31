import json
from json.decoder import JSONDecodeError
from re import T
import threading
from Library.Tools.basic import *
import websocket as ws
from Library.Tools.Logger import *

count = 0
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

def RecvMsg(websocket,bot,myWin):
    while True:
        time.sleep(0.1)
        try:
            j = json.loads(websocket.recv())
        except Exception as e:
            log_error('Mirai已断开连接...')
            log_debug(e)
            break

        if 'data' in j and 'type' in j['data'] and j['syncId'] != '123':
            if j['data']['type'] == "GroupMessage":
                group = j['data']["sender"]['group']['id']
                senderqq = j['data']['sender']["id"]
                sendername = j['data']['sender']["memberName"]
                Sourceid = 0
                msg = ''
                if len(j['data']["messageChain"]) == 1:
                    for i in j['data']["messageChain"]:
                        if i['type'] == 'Plain':
                            msg = i["text"]
                        elif i['type'] == 'Source':
                            Sourceid = i['id']
                else:
                    msg = ''
                    for i in j['data']["messageChain"]:
                        if i['type'] == 'Plain':
                            msg += i["text"]
                        elif i['type'] == 'At':
                            msg += str(i['target'])
                        elif i['type'] == 'Source':
                            Sourceid = i['id']
                #验证是否是管理的群
                if group in config['Group']:
                    #验证正则
                    regular = getRegular('group')
                    #print()
                    for b in regular['group']:
                        p = re.findall(b['re'],msg)
                        if p != []:
                            cmd = replaceRE(p,b['action'])
                            #发群消息
                            rps = replacegroup(myWin.on_bds.Port,cmd[2:],sendername,senderqq)
                            if b['perm'] == True:
                                if senderqq in config['Admin']:
                                    if b['action'][:2] == '>>':
                                        for g in config["Group"]:
                                            bot.sendGroupMsg(g,rps)
                                    #执行命令
                                    elif b['action'][:2] == '<<':
                                        if 'motd' in cmd[2:]:
                                            myWin.on_bds.Botruncmd(rps+' '+str(group))
                                        elif 'bindid' in cmd[2:]:
                                            myWin.on_bds.Botruncmd(rps+' '+str(group))
                                        elif 'unbind' in cmd[2:]:
                                            myWin.on_bds.Botruncmd(rps+' '+str(group))
                                        else:
                                            myWin.on_bds.Botruncmd(rps)
                                else:
                                    if Language['NoPermission'] != False:
                                        bot.sendGroupMsg(group,Language['NoPermission'])

                            else:
                                if b['action'][:2] == '>>':
                                    for g in config["Group"]:
                                        bot.sendGroupMsg(g,rps)
                                #执行命令
                                elif b['action'][:2] == '<<':
                                    if 'motd' in cmd[2:]:
                                        myWin.on_bds.Botruncmd(rps+' '+str(group))
                                    elif 'bind' in cmd[2:]:
                                        myWin.on_bds.Botruncmd(rps+' '+str(group))
                                    elif 'unbind' in cmd[2:]:
                                        myWin.on_bds.Botruncmd(rps+' '+str(group))
                                    else:
                                        myWin.on_bds.Botruncmd(rps)
                        else:
                            rt = {'Type':'None'}
                    
                    #绑定xboxid
                    if config['AtNoXboxid']['Enable']:
                        qxlist = getQXlist()
                        qlist = getQQlist()
                        xlist = getXboxlist()
                        if senderqq not in qlist:
                            #撤回消息
                            if config['AtNoXboxid']['Recall']:
                                bot.recallmsg(Sourceid)
                            bot.send_at(group,senderqq,Language['AtNotXboxid'])
            #检测改名
            elif j['data']['type'] == "MemberCardChangeEvent":
                qqid = j['data']['member']['id']
                group = j['data']['member']['group']['id']
                qxlist = getQXlist()
                qlist = getQQlist()
                xlist = getXboxlist()
                #检测是否是管理的群
                if group in config['Group']:
                    #检测是否绑定白名单
                    if qqid in qlist and qqid not in config['CheckNick']['WhiteList']:
                        for p in qxlist:
                            if p['qq'] == qqid:
                                if j['data']['current'] != p['id']:
                                    bot.changeName(qqid,group,p['id'])
                                    if Language['ChangeNick'] != False:
                                        bot.send_at(group,qqid,Language['ChangeNick'])

            #检测成员离开群聊
            elif 'MemberLeaveEventKick' == j['data']['type'] or "MemberLeaveEventQuit" == j['data']['type']:
                memberid = j['data']['member']['id']
                group = j['data']['member']['group']['id']
                #验证管理群号
                if group in config['Group'] and config['LeftRemove']:
                    qxlist = getQXlist()
                    qlist = getQQlist()
                    xlist = getXboxlist()
                    if memberid in qlist:
                        wl = read_file(config['ServerPath']+'\\whitelist.json')
                        wlrun = False
                        xboxid = r'%xboxid%'
                        for x in qxlist:
                            if x['qq'] == memberid:
                                xboxid = x['id']
                        for names in wl:
                            if names['name'] == xboxid:
                                wlrun = True
                        if wlrun:
                            if Language['LeftGroup'] != False:
                                bot.sendGroupMsg(group,Language['LeftGroup'].replace(r'%xboxid%',xboxid))
                            myWin.on_bds.Botruncmd('whitelist remove "%s"' % xboxid)
        elif 'syncId' in j and j['syncId'] == '123' and 'data' in j :
            try:
                ij = j['data']
                if ij['code'] == 0 and ij['messageId'] == -1:
                    log_warn('发送消息时可能遭到屏蔽')
            except JSONDecodeError as e:
                log_debug(e)
                log_error('出现了内部错误')

        elif  'syncId' in j and j['syncId'] == '1234' and 'data' in j:
            try:
                ij = j['data']
                if ij['code'] == 10:
                    log_warn('尝试更改名片但没有权限')
            except JSONDecodeError as e:
                log_debug(e)
                log_error('出现了内部错误')
            
        elif  'syncId' in j and j['syncId'] == '12345' and 'data' in j:
            try:
                ij = j['data']
                if ij['messageId'] == -1:
                    log_warn('发送卡片时可能遭到屏蔽')
            except JSONDecodeError as e:
                log_debug(e)
                log_error('出现了内部错误')

class Bot():
    def __init__(self) -> None:
        self.reconnect_N = 0

    def login(self,sb,win):
        try:
            self.bot = sb
            self.win = win
            key = config['Key']
            url = config['BotURL']
            uri = url+'/all?verifyKey=%s&qq=%i' % (key,config['Bot'])
            self.ws = ws.create_connection(uri)
            self.connect = True
            log_info('%i %s' % (config['Bot'],'登录成功'))
            if config['EnableGroup']:
                self.recvThread = threading.Thread(target=RecvMsg,args=(self.ws,self.bot,self.win,))
                self.recvThread.setDaemon(True)
                self.recvThread.setName('Recive message')
                self.recvThread.start()
            return True
        except Exception as e:
            self.connect = False
            log_debug(e)
            return False

    def send_at(self,group,senderqq,msg):
        try:
            msgjson = {
                "target":group,
                "messageChain":[{"type": "At", "target": senderqq, "display": ""}]
            }
            if msg != False:
                msgjson['messageChain'].append({"type":"Plain", "text":msg})

            mj = {
                "syncId": 1234,
                "command": "sendGroupMessage",
                "subCommand": None,
                "content": msgjson
            }
            self.ws.send(json.dumps(mj))
        except Exception as e:
            log_debug(e)


    def recallmsg(self,Sourceid):
        try:
            recjson = {
                "target":Sourceid
            }
            mj = {
                "syncId": 12345,
                "command": "recall",
                "subCommand": None,
                "content": recjson
            }
            self.ws.send(json.dumps(mj))
        except Exception as e:
            log_debug(e)

    #修改群名
    def changeName(self,member,group,name):
        try:
            namejson = {
                "target": group,
                "memberId": member,
                "info": {
                    "name": name,
                }
            }
            mj = {
                "syncId": 1234,
                "command": "memberInfo",
                "subCommand": 'update',
                "content": namejson
            }
            self.ws.send(json.dumps(mj))
        except Exception as e:
            log_debug(e)

    def sendGroupMsg(self,group,text):
        try:
            msgjson = {
            "target":group,
            "messageChain":[
                { "type":"Plain", "text":text.replace('\\n','\n')},
            ]
        }
            mj = {
            "syncId": 123,
            "command": "sendGroupMessage",
            "subCommand": None,
            "content": msgjson
        }
            self.ws.send(json.dumps(mj))
        except Exception as e:
            log_debug(e)
            
    #发送卡片
    def send_app(self,group,code):
        try:
            msgjson = {
                "target":group,
                "messageChain":[{
            "type": "App",
            "content": code
        }]
            }
            mj = {
                "syncId": 12345,
                "command": "sendGroupMessage",
                "subCommand": None,
                "content": msgjson
            }
            self.ws.send(json.dumps(mj))
        except Exception as e:
            log_debug(e)

    def tReconnect(self):
        rec = threading.Thread(target=self.reconnect)
        rec.setDaemon(True)
        rec.setName('Reconnect')
        rec.start()

    def reconnect(self):
        self.reconnect_N = 0
        self.disconnect()
        log_info('重连中...')
        if self.reconnect_N < 10:
            while self.reconnect_N <= 10:
                if self.login(self.bot,self.win):
                    self.reconnect_N = 0
                    break
                else:
                    log_error('连接失败！剩余尝试次数:'+str(10-self.reconnect_N)+'/10')
                    self.reconnect_N += 1
            else:
                log_error('尝试连接无果，请检查后手动重试')
        

    def disconnect(self):
        try:
            self.ws.close(0)
        except AttributeError:
            pass
