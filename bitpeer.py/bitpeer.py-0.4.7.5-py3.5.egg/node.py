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
from . import storage

MAX_CLIENT_FAILURES = 5

class NodeClient (clients.ChainClient):
	def __init__ (self, socket, chain, node, host):
		self.node = node
		self.host = host
		self.failures = 0
		super (NodeClient, self).__init__ (socket, chain)


	def reconnect (self):
		self.failures += 1

		if self.failures < MAX_CLIENT_FAILURES:
			try:
				self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.socket.settimeout (3.0)
				self.socket.connect (self.host)
				self.socket.settimeout (None)
				self.handshake ()
			except:
				return False
			return True
		else:
			return False


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

	#def handle_version (self, message_header, message):
	#	print (message.start_height)


class Node:
	def __init__ (self, chain, storagedb, lastblockhash = None, lastblockheight = None, logger=None, maxpeers=15):
		if not networks.isSupported (chain):
			raise networks.UnsupportedChainException ()

		if logger == None:
			self.logger = log.DummyLogger ()
		else:
			self.logger = logger

		if type (storagedb) == str:
			self.db = storage.shelve.ShelveStorage (storagedb)
		else:
			self.db = storagedb

		self.maxpeers = maxpeers
		self.minpeers = 4
		self.chain = chain
		self.clients = []
		self.threads = []
		self.peers = []
		self.blockFilter = lambda b: b
		self.synctimer = None
		self.mempooltimer = None
		self.boottimer = None
		self.postblocks = {}
		self.newblocklock = Lock ()

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

		self.logger.debug ('Starting sync from block %d %s', self.db['lastblockheight'], self.db['lastblockhash'])


	# Contact the seed nodes for retrieving a peer list, also load a file peer list
	def bootstrap (self):
		self.peers = []
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
		#self.peers = self.peers [0:self.maxpeers]
		self.logger.debug ('Bootstrap done with %s peers', len (self.peers))

	def isConnected (self, peer):
		for x in self.clients:
			if x.host == peer:
				return True
		return False

	def connect (self):
		for peer in self.peers:
			if self.isConnected (peer):
				return

			if len (self.clients) == self.maxpeers:
				break

			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout (3.0)
				sock.connect (peer)
				sock.settimeout (None)
				pcc = NodeClient (sock, self.chain, self, peer)
				pcc.handshake ()
				self.clients.append (pcc)
			except:
				pass

		if len (self.clients) == 0:
			raise Exception ()

		self.logger.debug ('Connected to %s peers', len (self.clients))
		self.synctimer = Timer (5.0, self.sync)
		self.synctimer.start ()


	def reboot (self):
		self.logger.debug ('Bootstrapping clients...')
		self.boottimer.cancel ()
		self.bootstrap ()
		self.connect ()

	def sync (self):
		if len (self.clients) == 0:
			self.logger.debug ('No clients available, bootstrapping...')
			self.reboot ()
			return

		if len (self.clients) < self.minpeers:
			self.logger.debug ('Available clients are less than minpeers, bootstrapping...')

			if self.boottimer != None:
				self.boottimer.cancel ()

			self.boottimer = Timer (5.0, self.reboot)
			self.boottimer.start ()


		for p in self.clients:
			#r = random.randint(0, len (self.clients) - 1)
			#p = self.clients [r]
			try:
				#print (self.db['lastblockhash'])
				getblock = clients.GetBlocks ([int (self.db['lastblockhash'], 16)])
				p.send_message (getblock)
			except Exception as e:
				#self.logger.error ('Node fail.')
				if not p.reconnect ():
					self.logger.debug ('Removed unreachable peer %s (%s)', str (p.host), e)
					self.clients.remove (p)
					self.logger.debug ('Available peers: %d', len (self.clients))


		self.synctimer.cancel ()
		self.synctimer = Timer (5.0, self.sync)
		self.synctimer.start ()


	def innerLoop (self, cl):
		try:
			cl.loop ()
		except Exception as e:
			#self.logger.error ('Node loop failure.')
			if not cl.reconnect ():
				self.logger.debug ('Removed unreachable peer %s (%s)', str (cl.host), e)
				self.clients.remove (cl)
				self.logger.debug ('Available peers: %d', len (self.clients))

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
					#self.logger.debug ('Transaction announce failure: %s', str (e))
					pass

		self.mempooltimer.cancel ()
		self.mempooltimer = Timer (30.0, self.announceTransactions)
		self.mempooltimer.start ()


	def handle_mempool (self, client, message_header, message):
		pass

	def handle_getdata (self, client, message_header, message):
		for inv in message.inventory:
			txhash = str (hex (inv.inv_hash))[2:]
			#print (txhash)
			if txhash in self.db['mempool']:
				tx = self.db['mempool'][txhash]
				txhex = tx.as_hex ()
				#print (txhex)
				try:
					client.send_tx (txhex)
				except Exception as e:
					pass #logger.debug ('Send transaction failure: %s', str (e))

	def handle_block (self, message_header, message):
		self.newblocklock.acquire ()
		#print ('in')
		if message.previous_block_id () == self.db['lastblockhash']:
			try:
				b = self.blockFilter (message)
			except Exception as e:
				#print ('fout', e)
				self.newblocklock.release ()
				logger.debug ('BlockFilter failure: %s', str (e)) 
				return

			# Serialize block
			try:
				hash = message.id ()
				self.db[str (int (self.db['lastblockheight']) + 1)] = hash
				self.db[hash] = b
				self.db['lastblockheight'] += 1
				self.db['lastblockhash'] = hash
				self.logger.debug ('New block: %d %s', self.db['lastblockheight'], self.db['lastblockhash'])

				if hash in self.postblocks:
					self.newblocklock.release ()
					self.handle_block (None, self.postblocks[hash])
					#self.logger.debug ('PREVBLOCK found')
					self.neblocklock.acquire ()
					del self.postblocks[hash]

				self.db.sync ()
			except:
				pass

			#print ('out')
			self.newblocklock.release ()

			self.synctimer.cancel ()
			self.synctimer = Timer (0.5, self.sync)
			self.synctimer.start ()
		else:
			hash = message.previous_block_id ()
			if not hash in self.db:
				self.postblocks [hash] = message
			#print ('oout')
			self.newblocklock.release ()


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
		t = Tx.from_hex (transaction)
		h = t.id ()

		if not h in self.db['mempool']:
			mp = self.db['mempool']
			mp[h] = t
			self.db['mempool'] = mp
			self.db.sync ()

		self.mempooltimer = Timer (1.0, self.announceTransactions)
		self.mempooltimer.start ()

		return h
