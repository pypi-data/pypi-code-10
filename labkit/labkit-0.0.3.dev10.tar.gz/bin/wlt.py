#!/bin/env python
# -*- coding: utf-8 -*-


import httplib, urllib
# config parameters
'''
About ISP
0: 教育网出口(国内)
1: 电信网出口(国际,到教育网走教育网)
2: 联通网出口(国际,到教育网走教育网)
3: 电信网出口2(国际,到教育网免费地址走教育网)
4: 联通网出口2(国际,到教育网免费地址走教育网)
5: 电信网出口3(国际,到教育网走教育网,到联通走联通)
6: 联通网出口3(国际,到教育网走教育网,到电信走电信)
7: 教育网国际出口(国际,临时使用,解决近期国际访问问题)

About Time
动态:    120
1小时:    3600
4小时:    14400
11小时:    39600
14小时:    50400
永久:    0
About Time
动态:    120

'''
Login_name='lhrkkk'
password = 'vsyouk'
ISP = '7'
expire = '0'

def connect(cmd, set_cookie={}):
    headers = {"User-Agent": "Chrome/18.0.1025.168", "Host": "wlt.ustc.edu.cn", "Accept": "*/*"}
    conn = httplib.HTTPConnection("wlt.ustc.edu.cn")
    try:
        if cmd == 'login':
            conn.request("GET", "/cgi-bin/ip?cmd=login&name="+Login_name+"&password="+password, '', headers)
            ret = conn.getresponse()
            return ret
        if cmd == 'set':
            conn.request("GET", "/cgi-bin/ip?cmd=set&type="+ISP+'&exp='+expire,"",dict(headers.items()+set_cookie.items()))
            ret = conn.getresponse()
            return ret
    except httplib.HTTPException as ex:
        print ret.status, ret.reason, ex
    return None

def autoWlt():
    res = connect('login')
    if res.status != 200:
        print res.status, res.reason
        return 1
    Cookie = {"Cookie":res.getheaders()[1][1]}
    res = connect('set', Cookie)
    if res.status != 200:
        print res.status, res.reason
        return 2
    return 0
if __name__ == '__main__':
    errno = autoWlt()
    if errno == 1:
        print "login error"
    if errno == 2:
        print "set error"
