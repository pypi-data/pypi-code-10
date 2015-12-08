#coding=utf-8
'''print_lol函数主要实现打印多重列表功能，对嵌套列表展示时，如果列表中还有列表则缩进显示，主要使用递归方法， 遇到列表则调用本身函数。
   参数解释：the_list 列表，indent是否缩进，level表示缩进级别，即tab N次，fn即文件对象。'''
import sys
def print_lol(the_list,indent=False,level=0,fn=sys.stdout):
    for each_item in the_list:
            if isinstance(each_item,list):
                    print_lol(each_item,indent,level+1,fn)
            else:
                    if indent:
                            for tab_stop in range(level):
                                    fn.write('\t')
                    fn.write(each_item+'\n')

