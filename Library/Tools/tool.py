from Library.Tools.motd import *
from Library.Tools.basic import *

def WriteYaml(file,dic):
    with open(file,'w',encoding='UTF8') as f:
        f.write(yaml.dump(dic))

def motdServer(bot,ip,port,group):
    motd = Server(ip,int(port))
    jmotd = motd.motd()
    if jmotd['status'] == 'online':
        if Language['MotdSuccessful'] != False:
            sendmsg = Language['MotdSuccessful'].replace(r'%ip%',jmotd['ip']).replace(r'%port%',str(jmotd['port'])).replace(r'%motd%',jmotd['name'])\
            .replace(r'%agreement%',jmotd['protocol']).replace(r'%version%',jmotd['version']).replace(r'%delay%',str(jmotd['delay'])+'ms')\
                .replace(r'%online%',jmotd['online']).replace(r'%max%',jmotd['upperLimit']).replace(r'%gamemode%',jmotd['gamemode'])

            bot.sendGroupMsg(group,sendmsg.replace('\\n','\n'))
    else:
        if Language['MotdFaild'] != False:
            bot.sendGroupMsg(group,Language['MotdFaild'])

def bind(bot,qqid,name,group):
    from Library.Tools.basic import changeFile,getQXlist,getQQlist,getXboxid,getXboxlist,Xboxid,Language,config,Regular
    qxlist = getQXlist()
    qlist = getQQlist()
    xlist = getXboxlist()

    #检测QQ是否绑定
    if qqid in qlist:
        for i in qxlist:
            if qqid == i['qq']:
                if Language['QQBinded'] != False:
                    bot.sendGroupMsg(group,Language['QQBinded'].replace(r'%xboxid%',i['id']))
                return False

    #检测Xboid是否绑定
    if name in xlist:
        for i in qxlist:
            if name == i['id']:
                if Language['XboxIDBinded'] != False:
                    bot.sendGroupMsg(group,Language['XboxIDBinded'].replace(r'%binderqq%',str(i['qq'])))
                return False

    #全部都不符合自动绑定
    XboxDic = Xboxid
    XboxDic['Xbox'].append({'name':name,'qq':qqid,'group':group})
    changeFile('Xboxid',XboxDic)
    #发群消息
    if Language['BindSuccessful'] != False:
        bot.sendGroupMsg(group,Language['BindSuccessful'].replace(r'%xboxid%',name))
    #更改群名片
    if config['AtNoXboxid']['Rename']:
        bot.changeName(qqid,group,name)

#获取cpu状态
cpup = 0
def getcpupercent():
    global cpup
    while True:
        psutil.cpu_percent(None)
        time.sleep(0.5)
        cpup = str(psutil.cpu_percent(None))
        time.sleep(2)



#解除绑定
def unbind(bot,qqid,group):
    from Library.Tools.basic import changeFile,getQXlist,getQQlist,getXboxid,getXboxlist,Xboxid,Language,config,Regular
    qxlist = getQXlist()
    qlist = getQQlist()
    xlist = getXboxlist()
    #检测是否绑定
    if qqid in qlist:
        for i in qxlist:
            if i['qq'] == qqid:
                XboxDic = Xboxid
                for i in XboxDic['Xbox']:
                    if i['qq'] == qqid:
                        XboxDic['Xbox'].remove(i)
                changeFile('Xboxid',XboxDic)
                if Language['unBindSuccessful'] != False:
                    bot.sendGroupMsg(group,Language['unBindSuccessful'].replace(r'%xboxid%',i['id']))
                if config['AtNoXboxid']['Rename']:
                    bot.changeName(qqid,group,'')
    else:
        if Language['NotFoundXboxID'] != False:
            bot.sendGroupMsg(group,Language['NotFoundXboxID'])