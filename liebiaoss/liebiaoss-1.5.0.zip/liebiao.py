import sys
def liebiaoss(item,indent=False,level=0,fh=sys.stdout):
	for each in item:
		if isinstance(each,list):
			liebiao(each,indent,level+1,fh)
		else:
			if indent:
			   for num in range(level):
				   print("\t",end='',file=fh)
			print(each,file=fh)



