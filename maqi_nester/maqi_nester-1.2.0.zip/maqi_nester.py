def print_lol(thelist,level=0):
          for each_item in thelist:
                    if(isinstance (each_item,list)):
                              print_lol(each_item,level+1)
                    else:
                        for i in range(level):
                                print("\t",end='')
                        print(each_item)
