def print_lol(thelist,level):
          for each_item in thelist:
                    if(isinstance (each_item,list)):
                              print_lol(each_item,level+1)
                    else:
                        for i in range(level):
                                print("\t",end='')
                        print(each_item)
