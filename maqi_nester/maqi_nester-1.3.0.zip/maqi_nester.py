def print_lol(thelist,indent=False,level=0):
          for each_item in thelist:
                    if(isinstance (each_item,list)):
                              print_lol(each_item,indent,level+1)
                    else:
                        if indent:
                            for i in range(level):
                                print("\t",end='')
                        print(each_item)
