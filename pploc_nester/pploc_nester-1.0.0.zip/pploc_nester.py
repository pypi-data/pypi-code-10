"""
This is my string parser
This function will list all string in list recursively
"""

def list_string(my_list) : 
    for each_object in my_list :
        if isinstance(each_object, list) == True : 
            nester(each_object)
        else : 
            print(each_object)
