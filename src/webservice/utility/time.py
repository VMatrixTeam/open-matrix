# coding=utf-8

import datetime

def timebefore(d):
    chunks = (
                   (60 * 60 * 24 * 365, u'year'),
                   (60 * 60 * 24 * 30, u'month'),
                   (60 * 60 * 24 * 7, u'week'),
                   (60 * 60 * 24, u'day'),
                   (60 * 60, u'hour'),
                   (60, u'min'),
    )
    #如果不是datetime类型转换后与datetime比较
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year,d.month,d.day)
    now = datetime.datetime.now()
    delta = now - d
    #忽略毫秒
    before = delta.total_seconds()
    #刚刚过去的1分钟
    if before <= 60:
        return "just now"
    for seconds,unit in chunks:
        count = before // seconds
        if count != 0:
            break
    if int(count) > 1: unit += "s"
    return unicode(int(count))+ " " + unit +" ago"
