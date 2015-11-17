movies = [
        "The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
        ["Graham Chapman",
         ["Micheal Palin","John Cleese","Terry Gilliam","Eric Idle","Terry Jones"]]]

"""這是asd.py模組,它提供了一個叫print_lol()的函式,
用於印出清單,不管其中有沒有包含被套疊的清單"""
def print_lol(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
"""此函數需要一個位置引數,名為"the_list",它可以是任何的Python清單,
(有可能套疊了其它清單)清單中每筆資料項會被(遞回地)顯示在螢幕上,並自成一列"""


"""This is the asd.py module and it provides one function called print_lol()
which prints lists that may or may not include nested list"""

def print_lol(the_list,level):
    """This function takes a positional argument called"the_list",which
is any Python list(of - possibly - nested lists).Each data item in the provided list
is(recursively) printed to the screen on it's own line.
A second argument called "list" is used to insert tab-stops when a nested list is encountered."""

    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='    ')
            print(each_item)
