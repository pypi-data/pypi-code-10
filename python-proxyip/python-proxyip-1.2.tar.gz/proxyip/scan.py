# -*- coding: utf-8 -*-
# Created by lvjiyong on 15/6/29

import socket
import re

from gelid.extractors.page import Page
from gelidhttp import http
from gelidhttp.log import logger

proxy_regex = '(_tr.*?_\s*?(\d+?\.\d+?\.\d+?\.\d+?)\s+(\d+)\s.*?_/tr.*?_)'


def ping(ip_address, port, timeout=1):
    """
    ping ip_address及端口，如果返回0，则表示没有错误，接口可用
    :param ip_address:
    :param port:
    :param timeout:
    :return:

    >>> ping('220.181.57.217',80)
    0
    >>> ping('220.181.57.210',80)
    35

    """
    status = 35
    try:
        logger.debug('ping %s:%s' % (ip_address, port))
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.settimeout(float(timeout))
        address = (str(ip_address), int(port))
        status = cs.connect_ex(address)
        cs.close()

        logger.debug('ping %s:%s, status:%s' % (ip_address, port, status))

        return status
    except:

        logger.debug('ping %s:%s, status:%s' % (ip_address, port, status))

        return 1


def pings(ip_addresses, timeout=3):
    """
    twisted批量ping地址与端口
    :param ip_addresses:
    :param timeout:
    :return:

    >>> ip_addresses = ['220.181.57.217:80','127.1.0.1:80']
    >>> pings(ip_addresses)
    ['220.181.57.217:80']
    """
    pinged_addresses = []
    for ip in ip_addresses:
        ip_data = ip.split(':')
        result = ping(ip_data[0], ip_data[1], timeout)
        if result == 0:
            pinged_addresses.append(ip)

    return pinged_addresses


def find(html, regex=proxy_regex, high_anonymous =True):
    """
    获取内容中的ip地址与端口
    :param html:
    :param regex:
    :return:
    >>> len(find(http.request_with_header(url='http://www.kuaidaili.com/', timeout=5)[0]))>0
    True
    >>> len(find(http.request_with_header(url='http://proxy.goubanjia.com/', timeout=5)[0]))>0
    True
    >>> len(find(http.request_with_header(url='http://www.proxy-ip.cn/guonei/1', timeout=5)[0]))>0
    True
    >>> len(find(http.request_with_header(url='http://www.haodailiip.com/', timeout=5)[0]))>0
    True
    >>> len(find(http.request_with_header(url='http://www.xici.net.co/', timeout=5)[0]))>0
    True
    """

    html = re.sub(re.compile('<(/?tr).*?>', re.I | re.M), ' _\g<1>_ ', html)
    html = re.sub(re.compile('</td>', re.I | re.M), ' </td> ', html)
    page = Page(html)
    # logger.debug(page.txt)

    pattern = re.compile(regex, re.I | re.M)
    findall = re.findall(pattern, page.txt)

    # findall = ['%s:%s' % (ip[1], ip[2]) for ip in findall if u'高匿' in ip[0] ]

    if high_anonymous:
        findall = ['%s:%s' % (ip[1], ip[2]) for ip in findall if u'高匿' in ip[0]]
    else:
        findall = ['%s:%s' % (ip[1], ip[2]) for ip in findall]
    # logger.debug(findall)
    return findall


def fetch(url, timeout=5, regex=proxy_regex):
    """
    从网址中获取ip地址
    :param url:
    :param timeout:
    :param regex:
    :return:

    >>> fetch('http://www.baidu.com')
    []

    >>> len(fetch('http://www.kuaidaili.com/'))>0
    True

    >>> len(fetch('http://www.kuaidaili.com/free/inha/0'))>0
    False

    >>> x = fetch('http://proxy.goubanjia.com/')



    """
    try:
        page = http.request_with_header(url=url, timeout=timeout)[0]
        if page:
            return find(page, regex=regex)
        else:
            logger.debug('request return none')
    except Exception as e:
        logger.debug(e)
        pass

    return []


def fetch_active_ip(url, timeout=1, regex=proxy_regex):
    """
    获取通过ping测试的代理ip
    :param url:
    :param timeout:
    :param regex:
    :return:

    """
    ip_addresses = fetch(url, timeout, regex)
    logger.debug(ip_addresses)
    return pings(ip_addresses)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
