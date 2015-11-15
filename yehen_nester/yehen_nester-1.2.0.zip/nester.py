"""这是"nester.py"模块，提供了一个名为print_lol()的函数，这个函数
的作用是打印列表，其中有可能包含（也肯能不包含）嵌套列表"""
def print_lol(the_list,indent=False,level=0):
        """This function takes one positional argument called "the_list",which
is any Python list(of-possibly-nested lsits).Each data item in the provided
list is (recursivley printed to the screen on it's onw line"""
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,indent,level+1)
                else:
                        if indent:
                                for tn in range(level):
                                        print("\t",end="")
                        
                        print(each_item)
                        
                        
