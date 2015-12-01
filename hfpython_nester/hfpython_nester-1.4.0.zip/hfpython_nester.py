"""这是 "hfpython_nester.py" 模块，提供了一个名为 print_lol()的函数，这个函
数的作用是打印列表，并将列表中的数据项以一定格式输出（默认输出到屏幕）到文件中，
其中有可能包含（也可能不包含）嵌套列表。
version 1.4.0
"""

import sys


def print_lol(the_list, indent=False, level=0, fn=sys.stdout):
    """这个函数取4个位置参数，
    第一个参数名为 "the_list"，这可以是任何 Python
    列表（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归
    地）输出到屏幕上，各数据项各占一行。
    第二个参数名为 "indent"，默认值为 false 表示首行缩进功能关闭，
        传递 True 时表示打开首行缩进功能。
    第三个参数名为 "level"，默认值为 0，指定打印列表各数据项时首行缩进值。
    最后一个参数名为 "fn"，默认值为 sys.stdout，指定输出位置（默认为屏幕）。

    :param the_list:
    :param indent:
    :param level:
    :param fn:
    :return:
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, fn)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=fn)
            print(each_item, end='', file=fn)


"""
    可以使用下面代码替换 31行，32行代码
             print("\t" * level, end='', file=fn)
"""
