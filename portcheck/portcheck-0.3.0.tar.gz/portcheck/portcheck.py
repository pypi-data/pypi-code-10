#!/usr/bin/python
import socket;

import MySQLdb
from multiprocessing import Pool


		
def scan(arg):
	target_ip, port, key = arg
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(2)

	try:
		sock.connect((target_ip, int(port)))
		sock.close()

		return target_ip, port,key, True
	except (socket.timeout, socket.error):
		return target_ip, port, key, False		
		
def main():
	db = MySQLdb.connect(host="localhost", # your host, usually localhost
		user="root", # your username
		passwd="", # your password
		db="test") # name of the data base
	db.autocommit(True)

	cur = db.cursor() 

	cur.execute("SELECT * FROM portcheck WHERE Status = '' ")

	addresslist = cur.fetchall()

	pool = Pool(processes=10)

	for target_ip, port, key, status in pool.imap_unordered(scan, [(row[0], row[1], row[3]) for row in addresslist]):
		print target_ip, port, 'is', 'open' if status else 'closed'
		result = "'Open'" if status else "'Closed'"

		cur.execute("UPDATE portcheck set Status = "+result+" where portcheck.Key =" +str(key) )

	

		
		
if __name__ == '__main__':
	main()
