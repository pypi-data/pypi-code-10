#!/usr/bin/python
import socket;
import ping
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
	except socket.error:
		return target_ip, port, key, False		
	except  socket.timeout:
		ping_result = ping(target_ip)
		return target_ip, port, key, ping_result	

		
		
		
def ping_server(address):
	try:
		ping.verbose_ping(address, count=3)
		
		return True
	except socket.error, e:
		print "Ping Error:", e
		return False

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
		if status ==  False:
			ping_result = ping_server(target_ip)
			ping_status = "'Reachable'" if ping_result else "'Unreachable'"
		else:
			ping_status = "'Reachable'"
		

		cur.execute("UPDATE portcheck set Status = "+result+", PingStatus = "+ping_status+" where portcheck.Key =" +str(key) )

	

		
		
if __name__ == '__main__':
	main()
