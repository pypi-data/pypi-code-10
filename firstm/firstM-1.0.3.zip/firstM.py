"""This is a modul on the book of Headfirst Python.
Im studying the book and will share this module for study."""
def print_lol(the_list,indent=False,depth=0):
  """This function is for listing data which type is list."""
  for each_item in the_list:
    if isinstance(each_item, list):
      print_lol(each_item,indent,depth+1)
    else:
      if indent:
        for num in range(depth):
          print("\t", end='')
      print(each_item)
