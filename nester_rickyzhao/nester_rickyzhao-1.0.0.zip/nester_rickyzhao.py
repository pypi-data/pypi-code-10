""" This is the standrad way to include a multiple-line comment in your code."""
def print_lol(the_list):
	""" 这个函数去一个位置参数，名为“the list",则可以是任何python列表（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项各占一行。"""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)
