rent = [["401","Mr.A","1363237823","440111198707033010","2015-05-09"],
["402","Mr.B","1363237823","440111198707033010","2015-05-09"],
["403","Mr.C","1363237823","440111198707033010","2015-05-09"],
"404",
["405","Mrs.D","1363237823","440111198707033010","2015-05-09"],
"406",
["407","Mr.E","1363237823","440111198707033110","2015-05-09"],
["408","Mr.F","1363237823","440111198707033110","2015-05-09"]]
"""模块的注释"""
def print_rent(rent_list):
	"""函数内的注释"""
	for each_rent in rent_list:
		if isinstance(each_rent,list):
			print("has",end=":")
			size=len(each_rent)
			count=0
			for each_in_rent in each_rent:
				if count < size-1:
					print(each_in_rent,end=",")
					count = count+1;
				else:
					print(each_in_rent);
			
		else:
			continue;
