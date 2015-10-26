"""This is the "movies.py" module and it provides one function called printEach()
    which prints lists that may or may not include nested lists."""

def printEach(movies):
    
    """This function takes one positional argument called "movies", which
        is any Python list (of - posiibly -nested lists). Each data item in the
        provided list is (recursively) printed to the screen on it's own line."""
    
    for each_item in movies:
        if isinstance(each_item, list):
            printEach(each_item)
        else:
            print(each_item)

    
def printEach(movies, indent=False, level=0):
    for each_item in movies:
        if isinstance(each_item, list):
            printEach(each_item,level+1)
        else:
            if indent:
                for tab in range(level):
                    print("\t", end="")
            print(each_item)

