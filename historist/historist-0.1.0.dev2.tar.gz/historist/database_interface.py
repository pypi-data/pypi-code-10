import dataset
import os


_db_directory = os.path.expanduser('~')	+ "/historist_db/"	# "dbase_dir/"
_db_filename = 'mydatabase.db'
_db_url = "sqlite:///" + _db_directory + _db_filename


def get_db():
    if inspect():
        pass
    else:
        create_db()
    _db = dataset.connect(_db_url)
    # print _db_url
    return _db


def inspect():
    if os.path.exists(_db_directory) & os.path.isfile(_db_directory + _db_filename):
        return True
    else:
        return False


def create_db():
    if not os.path.exists(_db_directory):
        os.mkdir(_db_directory)
    db = dataset.connect(_db_url)
    db.create_table('actions')
    # db['actions'].create_column('action')
    # db['actions'].create_column('unit')
    db.create_table('events')
    # db['events'].create_column('action')
    # db['events'].create_column('value')
    # db['events'].create_column('date')
    # db['events'].create_column('time')
    print "tables created: %s, %s" % ('actions', 'events')


def hi():
    print "Welcome to historist-1.0.1"


if __name__ == "__main__":
    get_db()
