""" This is the standrad way to include a multiple-line comment in your code."""
def print_lol(the_list, indent=False, level=0, fh=Sys.stdout ):
	""" 这个函数第一个位置参数，名为“the list",则可以是任何python列表（也可以是包含嵌套列表的列表）。
    indent则是表示是否需要根据嵌套来缩进，默认为False，不需要缩进。
    level是为了控制缩进，默认为无嵌套列表则不缩进，每处理一个嵌套列表，则缩进一个制表符。
    fh则用来标识将把数据写入哪个位置，缺省值为sys.stdout,如果没有调用这个函数时没有指定文件对象则会依然写至屏幕。
	所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项各占一行。"""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, indent, level+1, fh)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t", end='', file=fh)
			print(each_item, file=fh)
