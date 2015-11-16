"""这是 "hfpython_nester.py" 模块，提供了一个名为 print_lol()的函数，这个函
数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表。
version 1.3.0
"""


def print_lol(the_list, indent=False, level=0):
    """这个函数取三个位置参数，名为 "the_list"，这可以是任何 Python
    列表（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归
    地）输出到屏幕上，各数据项各占一行。
    第二个参数，名为 "indent"，默认值为 false 表示首行缩进功能关闭，
        传递 True 时表示打开首行缩进功能。
    最后一个参数，名为 "level"，默认值为 0，指定打印列表各数据项时首行缩进值。

    :param the_list:
    :param indent:
    :param level:
    :return:
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(each_item)


"""
    可以使用下面代码替换 22行，23行代码
             print("\t" * level, end='')
"""
