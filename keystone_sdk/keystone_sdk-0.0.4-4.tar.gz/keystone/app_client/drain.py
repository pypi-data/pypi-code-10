# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
from Queue import Queue
import thread
import sys
import time
import zmq
from ipykernel.jsonutil import json_clean

import keystone.app_client.zmq_utils as zmq_utils
import keystone.parameters
import keystone.utils
from keystone.api import keystone_class, api_method
from keystone.coordinator import KSObserver, KSCoordinator
from keystone.app_client.session import Session
from keystone.order import KSOrderEventType

class Drain(KSObserver):
	class DrainThreadStop:
		pass
	session = Session()
	context = zmq.Context()
	def __init__(self, 
		strategy_manager, 
		drain_url='tcp://127.0.0.1:55558', 
		syn_url='tcp://127.0.0.1:55559', 
		debug=False):
		self.strategy_manager = strategy_manager
		self.drain_url = drain_url
		self.syn_url = syn_url
		self.debug = debug
		self.orders = []
		self.buffer = Queue()

	def initSocket(self, drain_url=None, syn_url=None):
		if drain_url is not None:
			self.drain_url = drain_url
		if syn_url is not None:
			self.syn_url = syn_url
		self.sock = zmq_utils.create_publisher_socket(drain_url, syn_url)

	def msg(self, dt):
		msg = {
		'date_str': dt,
		'datetime': (dt - datetime(1970,1,1)).total_seconds(),
		'portfolio_value': self.strategy_manager.portfolio.value(),
		'positions': [pos.to_dict() for pos in self.strategy_manager.portfolio.positions()],
		'orders': [order.to_dict() for order in self.orders],
		}
		msg.update(self.strategy_manager.analyzers[0].value())
		return msg

	def onDataEvent(self, dataEvent):
		# generate message
		msg = self.msg(dataEvent.time())
		# clear orders
		self.orders = []
		# trigger send method
		self.send(msg)

	def onOrderEvent(self, orderEvent):
	    if orderEvent.type != KSOrderEventType.ACCEPTED and orderEvent.type != KSOrderEventType.CANCELLED:
	    	self.orders.append(orderEvent.txn)

	def send(self, msg):
		message = keystone.utils.squash_dates(msg)
		message = json_clean(message)
		# self.buffer.put(message, block = True)
		# print >>sys.stderr,"send drain message"
		# print >>sys.stderr,'===================='
		# print >>sys.stderr,message
		# print >>sys.stderr,'===================='
		self.session.send(self.sock, u'drain', content = message, ident = 'stream.drain')

	def sendMessage(self):
		count = 1
		while True:
			message = self.buffer.get(block = True)
			if isinstance(message, self.DrainThreadStop):
				return
			self.session.send(self.sock, u'drain', content = message)
			# print "send %d"%(count)
			# count += 1

	def start(self):
		thread.start_new_thread(self.sendMessage, ())

	def wait(self):
		self.buffer.put(self.DrainThreadStop())
