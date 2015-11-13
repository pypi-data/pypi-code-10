""" 파이썬으로 만들었어요. """

def print_list(list_name, level=0):
	for each in list_name:	
		if isinstance(each, list):
			print_list(each, level+1)
		else:
			for tab_stop in range(level):
				print("\t", end='')	
			print(each)
