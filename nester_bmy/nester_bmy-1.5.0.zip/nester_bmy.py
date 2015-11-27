import sys
'''这是"nester.py"模块,提供了一个名为print_lol()的函数,这个函数的作用是打印列表。
其中有可能包含（也可能不包含）且套列表。'''
def print_lol(the_list,level = 0,indent = False, fh = sys.stdout):
        for each_item in the_list:
                """这个函数去一个位置参数,名为"the_list",这可以使任何python列表
               (也可以是包含嵌套列表的列表)所指的列表中的每个数据项会（递归的）输出到屏幕上,个数据项各占一行
               第二个参数名为"level",用来在遇到嵌套列表时插入制表符,默认为0
               第三个参数名为"indent",用来控制是否插入制表符,默认不插入
               第四个参数名为"fh",用来指定输出,默认为标准输出,即屏幕
               """
                if isinstance(each_item,list):
                        #回调函数
                        print_lol(each_item,level + 1,indent,fh)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t",end='',file = fh);
                        #打印输出
                        print(each_item, file = fh)
