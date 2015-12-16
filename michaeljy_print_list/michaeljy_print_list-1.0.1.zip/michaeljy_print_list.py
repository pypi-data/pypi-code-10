"""这个Python中的注释"""
def print_list(the_list,level):
	for tmp in the_list:
		if isinstance(tmp,list):
			print_list(tmp,level+1)
		else:
			for tt in range(level):
				print("\t",end='')
			print(tmp)