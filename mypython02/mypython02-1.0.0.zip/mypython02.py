"""这是mypython.py模块，提供一个名为print_lol（）的函数，这个函数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表"""

"""movies是示例列表"""

movies=["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
        ["Graham Chapman",["Michael Palin","John Cleese",
                           "Terry Gilliam","Eric Idle","Terry Jones"]]]


def print_lol(the_list):
    
    """这个函数取一个位置参数，名为the_list，这可以使任何python列表（可以包含嵌套列表）。所指的类表中的每个数据项会（递归的）输出到屏幕上，各数据项各占一行"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)

# print_lol(movies)
    
