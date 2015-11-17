"""
author:luocm123@gmail.com
Date:20151117
version:v2
"""

def printList(objlist,lastLevel,maxLevel):
	"""
	print nest list
	"""
	for item in objlist :
		if isinstance(item,list) :
			printList(item,++lastLevel,maxLevel)
		else:
                        
			for num in range(lastLevel):
				print("\t",end='')
			print(item)
