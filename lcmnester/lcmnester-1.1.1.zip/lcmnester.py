"""
author:luocm123@gmail.com
Date:20151117
version:v2
"""

def printList(objlist,lastLevel=0,maxLevel=0):
	"""
	print nest list
	"""
	for item in objlist :
		if isinstance(item,list) :
			printList(item,lastLevel+1,maxLevel)
		else:
			if lastLevel>maxLevel :
				lastLevel=maxLevel
			for num in range(lastLevel):
				print("\t",end='')
			print(item)
