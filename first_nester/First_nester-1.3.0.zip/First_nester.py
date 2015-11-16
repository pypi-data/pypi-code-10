"""这是一个“nestpy”模块，提供了一个print_list()的函数，这个函数作用是打印列表，可能包含（也可能不包含）嵌套列表。"""
def print_list(the_list,indent=False,level=0):
       """这个函数取一个位置参数，名为the_list，这是可以在任意Python列表（也可以在包含嵌套列表的列表）。所指定的列表中的每个数据项会递归地输出到屏幕上，每个数据项各占一行。"""
       for every_one in the_list:
              if isinstance(every_one,list):
                     print_list(every_one,indent,level+1)
              else:
                     if indent:
                            for tab_stop in range(level):                                  
                                   print("\t",end='')
                     print(every_one)
                     
