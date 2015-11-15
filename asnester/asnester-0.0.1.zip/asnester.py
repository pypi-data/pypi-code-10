def print_recur(li):
	for item in li:
		if isinstance(item, list):
			print_recur(item)
		else:
			print(item)

