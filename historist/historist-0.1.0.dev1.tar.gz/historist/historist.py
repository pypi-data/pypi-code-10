import database_interface as db_if
import sys
import time


def print_table_contents(tab):
    db = db_if.get_db()
    table = db[tab]
    print "table " + tab + ":"

    for key in table.columns:
        print "{:<10}".format(key),
    print

    for row in table:
        for val in row.itervalues():
            print "{:<10}".format(val),
        print
    print


def delete_tables():
    db = db_if.get_db()
    for tab in db.tables:
        db[tab].delete()


def insert_event(activity, value):
    db = db_if.get_db()
    table = db['events']
    # table.insert(dict(name='brush', val=1, date=time.strftime("%x"), time=time.strftime("%X")))
    table.insert(dict(action=activity, value=value, date=time.strftime("%x"), time=time.strftime("%X")))
    print "successfully added"


if __name__ == "__main__":
    print "Welcome to historist-1.0.1"