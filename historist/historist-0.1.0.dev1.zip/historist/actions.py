import dataset
import time

# connecting to a SQLite database
db = dataset.connect('sqlite:///./db/database.db')

# get a reference to the table 'user'
table = db['actions']
#table.delete()

# Insert a new record.
table.insert(dict(name='brush', val=1, date=time.strftime("%x"), time=time.strftime("%X")))


for row in db['actions']:
   print(row)
