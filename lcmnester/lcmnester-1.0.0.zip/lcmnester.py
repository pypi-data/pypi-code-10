"""
author:luocm123@gmail.com
Date:20151116
version:v1
"""

def printList(objlist):
	"""
	print nest list
	"""
	for item in objlist :
		if isinstance(item,list) :
			printList(item)
		else:
			print(item)
