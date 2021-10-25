# 如下为crontab表达式
## 请严格按照如下来书写，否则会无法解析
```python
iter = croniter('*/5 * * * *', base)  # 每5分钟执行一次
iter = croniter('2 4 * * mon,fri', base)  # 星期一和星期五的04:02
iter = croniter('2 4 1 * wed', base)  # 每周三或每月的第一天早上04:02
iter = croniter('2 4 1 * wed', base, day_or=False)  # 如果是星期三，每个月的第一天会是04:02
iter = croniter('0 0 * * sat#1,sun#2', base)  # 每月的第一个星期六和第二个星期日
iter = croniter('0 0 * * 5#3,L5', base)  # 本月3号和最后一个星期五
```