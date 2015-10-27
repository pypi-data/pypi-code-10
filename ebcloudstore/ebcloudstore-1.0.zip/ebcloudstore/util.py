# -*- coding: utf-8 -*-
def is_cn_char(cnt):
    """
    判断是否串中是否含有中文
    :param cnt:
    :return:
    """
    is_cn = False
    for i in cnt:
        is_cn = 0x4e00 <= ord(i) < 0x9fa6
        if is_cn:
            break
    return is_cn


def cn2char(cnt):
    """
    中文转字符
    :param cnt:
    :return:
    """
    ret = ""
    for i in cnt:
        is_cn = 0x4e00 <= ord(i) < 0x9fa6
        if is_cn:
            ret += hex(ord(i))
        else:
            ret += i
    return ret