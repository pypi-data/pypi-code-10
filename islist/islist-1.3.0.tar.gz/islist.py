# Argument
# 1) the_list --> get list value (and could be include nested list)
# 2) isTap (Optional) --> Default value is False (Not using level)
# 3) level (Optional) --> Default value is 0 (level means add tap if include list in list)

# You could call this method as below noted:
#	print_list(list)
#	 or print_list(list, True)
 
def print_list(the_list, isTap=False, level=0):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_list(each_item, isTap, level+1)
		else:
			if isTap:
				for tap_stop in range(level):
					print("\t", end='')
			
			print(each_item)
