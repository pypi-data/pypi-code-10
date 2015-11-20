# -*- coding: utf-8 -*-

"""
检查数据
"""

import socket
import re

from gelidhttp.log import logger
from gelidhttp import Request


def http_check(url, match, proxy, headers=None, timeout=1):
    """
    确认是否可正常访问远程http网站

    :param url:
    :param match:
    :param proxy:
    :param timeout:
    :return:

    >>> _url = 'http://weixin.sogou.com/weixin?type=1&query=%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD&ie=utf8'
    >>> _match = u'中华人民共和国'
    >>> _proxy = '172.16.10.100:3128'
    >>> from gelidhttp.utils import http_headers
    >>> _headers =http_headers(_url)
    >>> _headers['Cookie'] = 'successCount=1'
    >>> http_check(url=_url, match=_match, proxy=_proxy, headers=_headers, timeout=1)


    """
    # try:
    proxy = {'http': 'http://%s' % proxy}
    logger.debug('request url:%s' % url)
    logger.debug('proxy:' % proxy)
    response = Request(url, proxy=proxy, headers=headers, timeout=timeout).response

    result = response.body_as_unicode()
    # logger.debug(response.cookies)
    # logger.debug(result)
    # if '/gzh?openid=' in result:
    #     print('ok:%s' % response.cookies)

    if re.search(re.compile(match), result):
        # logger.debug(response.cookies)
        return response
        # except Exception, e:
        #     logger.error(e)
        #     return False


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
    except Exception, e:

        logger.error('ping %s:%s, status:%s:%s' % (ip_address, port, status, e))

        return 1


def pings(ip_addresses, timeout=1):
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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
