"""This is the "clnester.py" module and it provides one function called print_lal()
    which prints lists that may or may not include nested lists."""

def print_lal(a,indent=False,tab=0):
    """This function takes one positional argument "a", which
       is any Phython list (of - possibly - nested lists). Each data item in the
       provided list is (recursively) printed to the screen on it's own line."""
    for a1 in a:
        if isinstance(a1, list):
            print_lal(a1, indent, tab+1)
                                 
        else:
            if indent:
                for tabb in range(tab):
                    print("\t",end='')
            print(a1)

			

