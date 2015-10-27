from dbops import *
import sys

if len(sys.argv) > 1:
	if sys.argv[1] == '-a':
		addItem(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == '-s':
		printTables()
		raw_input()
	else:
		print "Error: Unknown argument commands"
else:
	print "usage: historist [command] [arg1] [arg2]"
	print "commands:"
	print "\t-a\tadd item to table; historist -a pushup 8"
	print "\t-s\tprint database tables; historist -s"
	
