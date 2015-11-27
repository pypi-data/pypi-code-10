import sys;
"""A recursive traversal of a list"""
def printList(l, level):
    for li in l:
        if(isinstance(li,list)):
                level = level + 1
                printList(li, level)
        else:
                for stop in range(level):
                        print("\t",end='')
                print(li)
            
