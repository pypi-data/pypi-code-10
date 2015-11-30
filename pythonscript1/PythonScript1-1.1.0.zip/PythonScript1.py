#这是一个叫做print_lol的函数，这个函数的作用是打印列表
def print_lol(the_list):
#这个函数取一个位置参数，名为”the list
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)
