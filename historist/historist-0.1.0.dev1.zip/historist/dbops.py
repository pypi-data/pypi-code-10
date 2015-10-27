import dataset
import time

# connecting to a SQLite database
db = dataset.connect('sqlite:///./db/database.db')

def printTables():
    for tab in db.tables:
        print "Table: " + tab + "\n=========="
    table = db[tab]
    for key in table.columns:
        print "{:<10}".format(key),
    print

    for row in table:
        for val in row.itervalues():
            print "{:<10}".format(val),
        print "  "
    print " "

def deleteTables():
    for tab in db.tables:
        db[tab].delete()

def addItem(activity, value):
	# get a reference to the table 'actions'
	table = db['actions']

	# Insert a new record.
	#table.insert(dict(name='brush', val=1, date=time.strftime("%x"), time=time.strftime("%X")))
	table.insert(dict(name=activity, val=value, date=time.strftime("%x"), time=time.strftime("%X")))
	print "successfuly added"


def add(a, b):
    print "ADDING %d + %d" % (a, b)
    return a + b	
	