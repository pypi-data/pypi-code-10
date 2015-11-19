#这是“testing”模块，提供了一个名为print_lol的函数，这个函数的作用是打印列表，其中有可能包含嵌套列表
def print_lol(the_list,indent=false，level=0):
        for each_item in the_list:
                #这个函数取一个位置参数，名为“the_list”，这可以是任何Python列表。所指定的列表中的每个数据项会输出到列表屏幕上，各数据项各占一行。第二个参数，名为“indent”，用来控制实现缩进的代码。第三个参数，名为“level”，用来在遇到嵌套列表时插入制表
                if isinstance (each_item,list):
                        print_lol(each_item,indent,level+1)
                else:
                        if indent :
                                for tab_stop in range(level):
                                        print ("\t",end='')
                        print (each_item)
