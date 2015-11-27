import binascii
import shelve
import socket
import random
from pycoin.tx import Tx #remove this
from io import BytesIO
from threading import Thread, Lock, Timer
from . import clients
from . import networks
from . import serializers
from . import log


class NodeClient (clients.ChainClient):
	def __init__ (self, socket, chain, node):
		self.node = node
		super (NodeClient, self).__init__ (socket, chain)

	def handle_block(self, message_header, message):
		self.node.handle_block (message_header, message)

	def handle_inv(self, message_header, message):
		getdata = clients.GetData()
		getdata_serial = clients.GetDataSerializer()
		getdata.inventory = message.inventory
		self.send_message(getdata)

	def handle_mempool (self, message_header, message):
		self.node.handle_mempool (self, message_header, message)

	def handle_getdata (self, message_header, message):
		self.node.handle_getdata (self, message_header, message)

# Todo remove transaction from mempool after confirmation
class Node:
	def __init__ (self, chain, dbfile, lastblockhash = None, lastblockheight = None, logger=None, maxpeers=15):
		if not networks.isSupported (chain):
			raise networks.UnsupportedChainException ()

		if logger == None:
			self.logger = log.DummyLogger ()
		else:
			self.logger = logger

		self.maxpeers = maxpeers
		self.chain = chain
		self.dbfile = dbfile
		self.db = shelve.open (dbfile)
		self.sockets = []
		self.clients = []
		self.threads = []
		self.peers = []
		self.blockFilter = lambda b: b
		self.synctimer = None
		self.mempooltimer = None
		self.postblocks = {}

		# Create mempool
		#if not 'mempool' in self.db:
		self.db['mempool'] = {}

		# Set current block
		if ('lastblockheight' in self.db) and (self.db ['lastblockheight'] > lastblockheight):
			pass
		elif lastblockheight != None and lastblockhash != None:
			self.db ['lastblockheight'] = int (lastblockheight)
			self.db ['lastblockhash'] = lastblockhash
		else:
			self.db ['lastblockheight'] = 0
			self.db ['lastblockhash'] = networks.GENESIS[chain]


	# Contact the seed nodes for retrieving a peer list, also load a file peer list
	def bootstrap (self):
		for seed in networks.SEEDS [self.chain]:
			try:
				(hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex (seed)
				for ip in ipaddrlist:
					self.peers.append ((ip, networks.PORTS[self.chain]))

			except Exception as e:
				pass

		#print (self.peers)
		if len (self.peers) == 0:
			raise Exception ()

		random.shuffle (self.peers)
		self.peers = self.peers [0:self.maxpeers]
		self.logger.debug ('Bootstrap done')


	def connect (self):
		for peer in self.peers:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout (3.0)
				sock.connect (peer)
				sock.settimeout (None)
				pcc = NodeClient (sock, self.chain, self)
				pcc.handshake ()
				self.sockets.append (sock)
				self.clients.append (pcc)
			except:
				pass

		if len (self.clients) == 0:
			raise Exception ()

		self.synctimer = Timer (0.0, self.sync)
		self.synctimer.start ()


	def sync (self):
		if len (self.clients) == 0:
			return

		r = random.randint(0, len (self.clients) - 1)
		p = self.clients [r]
		try:
			getblock = clients.GetBlocks ([int (self.db['lastblockhash'], 16)])
			p.send_message (getblock)
		except:
			self.clients.remove (p)

		self.synctimer.cancel ()
		self.synctimer = Timer (0.1, self.sync)
		self.synctimer.start ()


	def innerLoop (self, cl):
		try:
			cl.loop ()
		except:
			self.clients.remove (cl)

	def loop (self):
		self.mempooltimer = Timer (1.0, self.announceTransactions)
		self.mempooltimer.start ()

		# Start the loop in each client as a new thread
		for cl in self.clients:
			t = Thread (target=self.innerLoop, args=(cl,))
			t.start ()
			self.threads.append (t)

	def stop (self):
		for cl in self.clients:
			cl.stop ()

		for t in self.threads:
			t.join ()


	def announceTransactions (self, txid = None):
		if txid != None or len (self.db['mempool']) != 0:
			inv = clients.InventoryVector()
			inv_serial = clients.InventoryVectorSerializer()

			if txid != None:
				sinv = clients.Inventory ()
				sinv.inv_hash = int (txid, 16)
				inv.inventory = [ sinv ]
			else:
				inv.inventory = []
				for txid in self.db['mempool']:
					sinv = clients.Inventory ()
					sinv.inv_hash = int (txid, 16)
					inv.inventory.append (sinv)

			#self.logger.debug ('Announcing %d transactions', len (inv.inventory))
			for cl in self.clients:
				try:
					cl.send_message (inv)
				except Exception as e:
					print (e)

		self.mempooltimer.cancel ()
		self.mempooltimer = Timer (2.0, self.announceTransactions)
		self.mempooltimer.start ()


	def handle_mempool (self, client, message_header, message):
		pass

	def handle_getdata (self, client, message_header, message):
		for inv in message.inventory:
			txhash = str (hex (inv.inv_hash))[2:]
			if txhash in self.db['mempool']:
				tx = self.db['mempool'][txhash]
				txhex = tx.as_hex ()

				try:
					client.send_tx (txhex)
				except Exception as e:
					pass

	def handle_block (self, message_header, message):
		if message.previous_block_id () == self.db['lastblockhash']:
			try:
				b = self.blockFilter (message)
			except Exception as e:
				print (e)

			# Serialize block
			hash = message.id ()
			self.db[str (int (self.db['lastblockheight']) + 1)] = hash
			self.db[hash] = b
			self.db['lastblockheight'] += 1
			self.db['lastblockhash'] = hash
			self.logger.debug ('%d %s', self.db['lastblockheight'], self.db['lastblockhash'])

			if hash in self.postblocks:
				self.handle_block (None, self.prevblocks[hash])
				#self.logger.debug ('PREVBLOCK found')
				del self.postblocks[hash]

			self.db.sync ()

			self.synctimer.cancel ()
			self.synctimer = Timer (0.1, self.sync)
			self.synctimer.start ()
		else:
			hash = message.previous_block_id ()
			if not hash in self.db:
				self.postblocks [hash] = message


	def getLastBlockHeight (self):
		return self.db['lastblockheight']

	def getBlockHash (self, index):
		if str(index) in self.db:
			return self.db[str(index)]
		else:
			return None

	def getBlockByHash (self, bhash):
		if bhash in self.db:
			return self.db[bhash]
		else:
			return None

	def broadcastTransaction (self, transaction):
		#print (transaction)
		t = Tx.tx_from_hex (transaction)
		h = t.id ()
		#print ('BROADCAST:', t.id ())

		if not h in self.db['mempool']:
			mp = self.db['mempool']
			mp[h] = t
			self.db['mempool'] = mp
			self.db.sync ()

		self.mempooltimer = Timer (1.0, self.announceTransactions)
		self.mempooltimer.start ()

		return h
