# -*- coding: utf-8 -*-
def is_cn_char(cnt):
    """
    check is contain chinese
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
    chinese to char
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

