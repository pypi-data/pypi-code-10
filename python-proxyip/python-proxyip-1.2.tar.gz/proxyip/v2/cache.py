# -*- coding: utf-8 -*-

"""
缓存数据
"""
import random

import data

ALL_IP_ADDRESS = []


def all_ip():
    global ALL_IP_ADDRESS
    if not ALL_IP_ADDRESS:
        ALL_IP_ADDRESS = data.all_ips()

    return ALL_IP_ADDRESS


def append_ips(ips):
    global ALL_IP_ADDRESS
    ALL_IP_ADDRESS.extend(ips)
    data.append(ips)


def remove_ips(ips):
    global ALL_IP_ADDRESS

    for ip in ips:
        if ip in ALL_IP_ADDRESS:
            ALL_IP_ADDRESS.remove(ip)
    data.remove(ips)


def clear_ip():
    global ALL_IP_ADDRESS
    ALL_IP_ADDRESS = []
    data.clear()


def rand_ip():
    """
    随机获取一个IP
    :return:

    >>> clear_ip()
    >>> rand_ip()
    >>> append_ips(['127.0.0.1:80'])
    >>> append_ips(['127.0.0.2:80'])
    >>> append_ips(['127.0.0.3:80'])
    >>> '127.0.0' in rand_ip()
    True

    """
    ips = all_ip()
    if ips:
        return ips[random.randint(0, len(ips) - 1)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
