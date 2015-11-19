"""This is the "cltabbnester.py" module and it provides one function called print_lal()
    which prints lists that may or may not include nested lists."""

def print_cltab(a, tab):
    """This function takes one positional argument "a", which
       is any Phython list (of - possibly - nested lists). Each data item in the
       provided list is (recursively) printed to the screen on it's own line."""
    for a1 in a:
        if isinstance(a1, list):
            for a2 in a1:
                if isinstance(a2, list):
                    for a3 in a2:
                        print("\t"*tab,end='')
                        print(a3)
                else:
                    print("\t"*tab,end='')
                    print(a2)
        else:
            print("\t"*tab,end='')
            print(a1)

			

