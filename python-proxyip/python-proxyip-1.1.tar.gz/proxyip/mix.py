# -*- coding: utf-8 -*-
# Created by lvjiyong on 15/6/29

from gelidhttp.log import logger

import scan
import data


def save_fetch(url, timeout=1, regex=scan.proxy_regex):
    """
    获取网页的IP地址并保存
    :param url:
    :param timeout:
    :param regex:
    :return:

    >>> data.clear()
    >>> save_fetch('http://www.kuaidaili.com/')
    >>> len(data.all_ips())>0
    True

    >>> data.clear()

    """
    ip_addresses = scan.fetch_active_ip(url, timeout, regex)

    logger.debug(ip_addresses)

    if ip_addresses:
        data.append(ip_addresses)


def refresh(timeout=2):
    ip_addresses = data.all_ips()
    for ip in ip_addresses:
        ip_data = ip.split(':')
        ping = scan.ping(ip_data[0],ip_data[1],timeout)
        if ping != 0:
            data.remove([ip])


if __name__ == "__main__":
    import doctest

    doctest.testmod()