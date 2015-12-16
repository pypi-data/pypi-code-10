"""这个Python中的注释"""
def print_list(the_list):
	for tmp in the_list:
		if isinstance(tmp,list):
			print_list(tmp)
		else:
			print(tmp)