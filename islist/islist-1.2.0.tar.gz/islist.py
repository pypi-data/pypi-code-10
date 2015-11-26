# Argument
# 1) the_list --> get list value (and could be include nested list)
# 2) level --> Add tap (if print value of nested list)

# You could call this method as below noted:
#	print_list(list, 0)
#
# level's default value is 0
# If list have list, increase the level value. (add tap and print nested list info)
 
def print_list(the_list, level=0):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_list(each_item, level+1)
		else:
			for tap_stop in range(level):
				print("\t", end='')
			print(each_item)
