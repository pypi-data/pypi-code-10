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
		return target_ip, port,key, True, True
	except (socket.error,  socket.timeout):
		pingstatus = verbose_ping(target_ip)
		return target_ip, port, key, False, pingstatus			



def verbose_ping(dest_addr, timeout = 2, count = 4):
	"""
	Send >count< ping to >dest_addr< with the given >timeout< and display
	the result.
	"""
	for i in xrange(count):
		print "ping %s..." % dest_addr,
	try:
		delay  =  ping.do_one(dest_addr, timeout)
	except socket.gaierror, e:
		print "failed. (socket error: '%s')" % e[1]
		return False

	if delay  ==  None:
		print "failed. (timeout within %ssec.)" % timeout
		return False

	else:
		delay  =  delay * 1000
		print "get ping in %0.4fms" % delay
		return True

	print		




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

	for target_ip, port, key, status, pingstatus in pool.imap_unordered(scan, [(row[0], row[1], row[3]) for row in addresslist]):
		print target_ip, port, 'is', 'open' if status else 'closed'
		result = "'Open'" if status else "'Closed'"
		pingstatus_result = "'Reachable'" if pingstatus else  "'Unreachable'"
		
	
		cur.execute("UPDATE portcheck set Status = "+result+", PingStatus = "+pingstatus_result+" where portcheck.Key =" +str(key) )

	

		
		
if __name__ == '__main__':
	main()
