# -*- coding: utf-8 -*-

"""
爬取数据
"""

import re

from gelid.extractors.page import Page
from gelidhttp import http
from gelidhttp.log import logger

proxy_regex = '(_tr.*?_\s*?(\d+?\.\d+?\.\d+?\.\d+?)\s+(\d+)\s.*?_/tr.*?_)'


def find(html, regex=proxy_regex, high_anonymous=True):
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


    # >>> len( x)
    # 100


    """
    logger.debug(url)



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


if __name__ == "__main__":
    import doctest

    doctest.testmod()