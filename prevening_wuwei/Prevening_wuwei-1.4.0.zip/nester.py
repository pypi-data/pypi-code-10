"""这是“nest.py”模块，提供了一个名为print_lol()的函数，这个函数的作用
是打印列表，其中有可能包含（也可能不包含）嵌套列表。"""
import sys

def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
	"""这个函数取一个位置函数，名为“the_list”，这可以是任何python列表（也可以是包含嵌套列表的列表）。
	所指定的列表中的每个数据项会（递归地）输出到屏幕上，各项数据各占一行。
	第二个参数，名为“indent”，为False时进行缩进，为True时进行缩进。
	第三个参数，名为“level”，用于遇到嵌套列表时打印level个制表符。
	第四个参数，名为“fh”，用于指定输出。"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1,fh)
		else:
			if indent:
				for tap_stop in range(level):
					print("\t",end="",file=fh)
			print(each_item,file=fh)
