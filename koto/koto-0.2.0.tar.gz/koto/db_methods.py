import sqlite3
import os
import sys

db_directory = '/usr/local/Library/Koto'
db_path = '/usr/local/Library/Koto/kotodb'

def firstStartupCheck():
	#if the database file exists
	if os.path.exists(db_path):
		#it is not the first time running koto
		return False
	else:
		return True

def initializeDB():
	print ('Initializing database in ' + db_path)
	db_directory = os.path.dirname(db_path)
	if not os.path.exists(db_directory):
		os.makedirs(db_directory)
		print ('Database directory created')
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS people(firstName text, lastName text, type text, email text, UNIQUE(firstName, lastName))")
	print('Database created')
	conn.close()

def initializeSettings():
	if not os.path.exists('/usr/local/Library/Koto/koto_settings.txt'):
		file = open('/usr/local/Library/Koto/koto_settings.txt', 'w')
		file.close()
	if (os.path.exists('/usr/local/Library/Koto/koto_settings.txt')):
		print('Settings file created')

def insertDB(firstName, lastName):
	print ('Inserting ' + firstName + ' ' + lastName + ' into database ' + db_path + '...')
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	# c.execute("CREATE TABLE IF NOT EXISTS people(firstName, lastName, UNIQUE(firstName, lastName))")
	c.executemany("INSERT OR IGNORE INTO people(firstName, lastName) VALUES (?, ?)", [(firstName, lastName)])
	if (c.rowcount != 0):
		print ('Successfully added ' + firstName + ' ' + lastName)
	else:
		print ('Failed to add ' + firstName + ' ' + lastName)
		#add already exists if statement error message
	conn.commit()
	conn.close()

def readAllEmails():
	print ('Reading contact emails from database ' + db_path + '...' + '\n')
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT email FROM people")
	return c.fetchall()
	conn.close()

def allNames():
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT firstName, lastName FROM people")
	return c.fetchall()
	conn.close()

def readDB(firstName):
	print ('Reading ' + firstName + ' from database ' + db_path + '...')
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT * FROM people WHERE firstName =?", [firstName])
	print (c.fetchall())
	conn.close()

def deleteDB(firstName, lastName=None):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	if (lastName):
		c.execute("DELETE FROM people WHERE firstName=? AND lastName=?", [firstName, lastName])
		if (c.rowcount != 0):
			print ('Successfully deleted ' + str(firstName) + ' ' + str(lastName))
		else:
			print ('Could not delete ' + str(firstName) + ' ' + str(lastName))
	else:

		matches = countMatches(firstName.capitalize())

		#if multiple people exist with given first name
		if (matches > 1):
			lastName = selectPerson(firstName)
			c.execute("DELETE FROM people WHERE firstName=? AND lastName=?", [firstName, lastName])
		#if only one person exists with given first name
		elif (matches == 1):
			c.execute("SELECT lastName FROM people WHERE firstName =?", [firstName])
			lastName = c.fetchone()[0]
			c.execute("DELETE FROM people WHERE firstName=? AND lastName=?", [firstName, lastName])
		elif (matches == 0):
			print ('Error: person with that name does not exist')

		if (c.rowcount == 1):
			print ('Successfully deleted ' + str(firstName) + " " + str(lastName))

	# if (c.rowcount == 1):
	# 	print ('Successfully deleted ' + str(firstName) + " " + str(lastName))
	# # elif (c.rowcount > 1):
	# # 	print(c.fetchone())
	# else:
	# 	print ('Could not delete ' + str(firstName)) # + " " + str(lastName)
	conn.commit()
	conn.close()

def readEmail(firstName, lastName=None):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	if (lastName):
		c.execute("SELECT email FROM people WHERE firstName =? AND lastName = ?", [firstName, lastName])
	else:
		c.execute("SELECT email FROM people WHERE firstName =?", [firstName])
	return (c.fetchone())
	#if multiple, specify ask which one
	conn.close()

def readName(email):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT firstName, lastName FROM people WHERE email =?", [email])
	name = c.fetchone()
	return name
	conn.close()	

def readLastName(firstName):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT lastName FROM people WHERE firstName =?", [firstName])
	lastName = c.fetchone()[0]
	return lastName
	conn.close()

def addEmail(email, firstName, lastName):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.executemany("UPDATE people SET email=? WHERE firstName=? AND lastName =?", [(email, firstName, lastName)])
	# c.executemany("INSERT INTO people (email) VALUES ? WHERE firstName = ?", [email, firstName])
	if (c.rowcount != 0):
		print ('Successfully added ' + email + ' to ' + firstName + " " + lastName)
	else:
		print ('Failed to add ' + email + ' to ' + firstName + " " + lastName)

		#add already exists if statement error message
	conn.commit()
	conn.close()

def countMatches(firstName):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT firstName, lastName FROM people WHERE firstName =?", [firstName])
	people = c.fetchall()
	return len(people)

def exit():
	sys.exit()

def selectNumber():
	try:
		ID = int(raw_input('--> '))
		return (ID)
	except ValueError:
		sys.exit("Error: expected an integer")

def selectBoolean():
	boolean = raw_input('--> ').capitalize()
	if (boolean == 'Y'):
		return True
		print('Y' + boolean)
	if (boolean == 'N'):
		return False
		print('N' + boolean)
	else:
		sys.exit("Error: expected boolean Y or N")

def importCSV():
	import csv

	conn = sqlite3.connect(db_path)
	c = conn.cursor()

	print('\nType path to file containing contacts \nFile must be in CSV format with data: full name, email, type (only name is required)')
	path = str(raw_input('--> '))
	if (os.path.exists(path)):
		with open(path, 'rb') as csvfile:
			contacts = csv.reader(csvfile, delimiter=',')
			for row in contacts:
				firstName, lastName = row[0].split()
				if (len(row) >= 2):
					email = row[1].strip()
				else:
					email = None
				if (len(row) == 3):
					contactType = row[2].strip()
				else:
					contactType = None
				c.execute("INSERT OR IGNORE into people (firstName, lastName, type, email) VALUES (?, ?, ?, ?)", [firstName, lastName, contactType, email])
				if (c.rowcount != 0):
					print ('Successfully added ' + firstName + ' ' + lastName)
				else:
					print ('Failed to add ' + firstName + ' ' + lastName)
				conn.commit()

		#add already exists if statement error message
	else:
		sys.exit('Path does not exist')

	conn.close()

#in case a query returns multiple results:
def selectPerson(firstName):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT firstName, lastName FROM people WHERE firstName =?", [firstName])
	people = c.fetchall()

	count = 0
	array = []
	print ("Multiple people found.  Select the correct person by ID number:")
	for person in people:
		print ("[" + str(count) + "]: " + str(person[0]) + " " + str(person[1]))
		array.append((count, person))
		count += 1		
	try:
		ID = int(raw_input('--> '))
		if (0 <= ID & ID <= (count - 1)):
			for person in array:
				if person[0] == ID:
					lastName = person[1][1]
					return lastName
		else:
			sys.exit("Error: integer not in ID range")
	except ValueError:
		sys.exit("Error: expected an integer")