def printall(hype_list,indent=False,level=0):
    """user can choose his requirement and type his index"""
    for data in hype_list:
        if isinstance(data,list):
           printall(data,indent,level+1)
        else:
           if indent:
              for tab_stop in range(level):
                  print("\t"),
           print data
