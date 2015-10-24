Python 3.5.0 (v3.5.0:374f501f4567, Sep 13 2015, 02:27:37) [MSC v.1900 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> def print_lol(the_list):
	for each_item in the_list:
		if isinstance (each_item,list):
			print_lol(each_item)
		else:print(each_item)

		
>>> 
