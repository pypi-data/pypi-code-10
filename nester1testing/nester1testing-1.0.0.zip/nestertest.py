"""This is the standard way to include a multiple-line comment in
your code."""

def allitem(the_list):
    """This function takes a positional argument called “the_list", which is any
    Python list (of, possibly, nested lists). Each data item in the provided list
    is (recursively) printed to the screen on its own line."""
    for i in the_list:
        if isinstance(i,list):
            allitem(i)
        else:
            print(i)
            
        



  
            
