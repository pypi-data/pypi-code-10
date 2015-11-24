import sys;
"""A recursive traversal of a list"""
def printList(l):
	for li in l:
		if(isinstance(li,list)):
			printList(li)
		else:
			print(li)
