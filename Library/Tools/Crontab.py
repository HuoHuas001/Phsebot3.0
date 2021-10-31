from croniter import CroniterBadCronError, CroniterNotAlphaError, croniter
from Library.Tools.Logger import *
from Library.Tools.basic import *
import time
#解析cron
def crontab():
    if config['EnableCron']:
        from Library.Tools.basic import readFile
        Crontab = read_file('data/crontab.yml')
        croncomment = []
        cronl = Crontab['Crontab']
        str_time_now= datetime.now()
        for i in cronl:
            try:
                iter=croniter(i['crontab'],str_time_now)
                time = iter.get_next(datetime).strftime("%Y-%m-%d-%H-%M-%S")
                cmd = i['action']
                croncomment.append({'time':time,'cmd':cmd,'cron':i['crontab']})
            except CroniterNotAlphaError as e:
                log_debug(e)
                log_error(i['cron']+' 解析失败')
            except CroniterBadCronError as e:
                log_debug(e)
                log_error(i['cron']+' 解析失败')
        WriteYaml('Temp/crontabTemp.yml',croncomment)
        log_info('Crontab定时任务开始运行,运行时间:'+str_time_now.strftime("%Y-%m-%d %H:%M:%S"))

#运行计划任务
def runcron(bot,myWin):
    while True:
        time.sleep(0.05)
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        nowlist = now.split('-')
        timelist = []
        for i in nowlist:
            timelist.append(int(i))
        croncmd = read_file('Temp/crontabTemp.yml')

        for i in croncmd:
            crontime = []
            for t in i['time'].split('-'):
                crontime.append(int(t))
            #触发条件
            if timelist[0] >= crontime[0] and timelist[1] >= crontime[1] and \
                timelist[2] >= crontime[2] and timelist[3] >= crontime[3] and\
                    timelist[4] >= crontime[4] and timelist[5] >= crontime[5]:
                rps = replaceconsole(myWin.on_bds.Port,i['cmd'][2:])
                #群消息
                if i['cmd'][:2] == '>>':
                    for g in config['Group']:
                        bot.sendGroupMsg(g,rps)
                #控制台
                elif i['cmd'][:2] == '<<':
                    myWin.on_bds.Botruncmd(rps)
                #运行程序
                elif i['cmd'][:2] == '^^':
                    os.system('start '+cmd[2:])

                #执行完毕重新解析
                str_time_now=datetime.now()
                iter=croniter(i['cron'],str_time_now)
                times = iter.get_next(datetime).strftime("%Y-%m-%d-%H-%M-%S")
                cmd = i['cmd']
                croncmd.remove(i)
                croncmd.append({'time':times,'cmd':cmd,'cron':i['cron']})
                WriteYaml('Temp/crontabTemp.yml',croncmd)