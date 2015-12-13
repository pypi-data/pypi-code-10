""" 这是"nester0.py"模块，提供名为print_lol()的函数，
这个函数作用是打印列表其中有可能包含嵌套的列表"""

def print_lol(the_item,level):
    """这个函数取一个位置参数为the_list 者可于是任何python列表
所指定的列表中的每个数据项会递归输出到屏幕上各数据项各占一行"""
    for each_item in the_item:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
		    for tab_stop in range(level)
			    print("\t",end="level")
            print(each_item)
