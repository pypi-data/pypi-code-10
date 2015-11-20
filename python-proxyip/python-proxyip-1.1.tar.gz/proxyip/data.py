# -*- coding: utf-8 -*-
# Created by lvjiyong on 15/6/29
import os
import random

IP_FILE = 'proxy_ip_addresses'


def clear():
    """
    清除所有数据
    :return:
    >>> clear()
    >>> append(['127.0.0.1:80'])
    >>> len(all_ips())
    1
    >>> clear()
    >>> os.path.exists(IP_FILE)
    False

    """
    if os.path.exists(IP_FILE):
        os.remove(IP_FILE)


def append(ip_addresses):
    """
    增加IP地址
    :param ip_addresses:
    :return:
    >>> clear()
    >>> append(['127.0.0.1:80'])
    >>> append(['127.0.0.2:80'])
    >>> append(['127.0.0.3:80'])
    >>> append(['127.0.0.1:80'])
    >>> append(['127.0.0.2:80'])
    >>> append(['127.0.0.3:80'])
    >>> len(all_ips())
    3

    >>> clear()
    """
    data = all_ips()
    for ip_address in ip_addresses:
        if ip_address not in data:
            data.append(ip_address)

    with open(IP_FILE, 'wb') as f:
        f.write('\n'.join(data))


def remove(ip_addresses):
    """
    删除IP地址
    :param ip_addresses:
    :return:
    >>> clear()
    >>> append(['127.0.0.1:80'])
    >>> append(['127.0.0.2:80'])
    >>> append(['127.0.0.3:80'])
    >>> len(all_ips())
    3
    >>> remove(['127.0.0.1:80'])
    >>> all_ips()
    ['127.0.0.2:80', '127.0.0.3:80']

    >>> clear()
    """
    data = all_ips()
    for ip_address in ip_addresses:
        if ip_address in data:
            data.remove(ip_address)

    with open(IP_FILE, 'wb') as f:
        f.write('\n'.join(data))


def rand_ip():
    """
    随机获取一个IP
    :return:

    >>> clear()
    >>> rand_ip()
    >>> append(['127.0.0.1:80'])
    >>> append(['127.0.0.2:80'])
    >>> append(['127.0.0.3:80'])
    >>> '127.0.0' in rand_ip()
    True

    """
    data = all_ips()
    count = len(data)
    if count > 0:
        return data[random.randint(0, count - 1)]


def all_ips():
    """
    返回所有数据
    :return:

    >>> clear()
    >>> all_ips()
    []

    >>> append(['127.0.0.1:80'])
    >>> append(['127.0.0.2:80'])
    >>> append(['127.0.0.3:80'])
    >>> len(all_ips())
    3

    >>> clear()

    """
    if os.path.exists(IP_FILE):
        with open(IP_FILE, 'rb') as f:
            data = f.read().split('\n')
    else:
        data = []
    return data

if __name__ == "__main__":
    import doctest

    doctest.testmod()