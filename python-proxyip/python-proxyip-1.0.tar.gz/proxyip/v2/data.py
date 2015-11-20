# -*- coding: utf-8 -*-

"""
存储与更新数据
"""
import os

IP_FILE = 'proxy_ip_addresses'


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
    data = all_ips() or []
    for ip_address in ip_addresses:
        if ip_address not in data:
            data.append(ip_address)

    with open(IP_FILE, 'wb') as f:
        f.write('\n'.join(data) or '')


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
