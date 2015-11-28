from . import storage

class MemStorage (storage.Storage):
	def __init__ (self):
		self.db = {}

	def __getitem__(self, key):
		return self.db[key]
		
	def __setitem__(self, key, value):
		self.db[key] = value
		
	def __contains__(self, key):
		return key in self.db

	def sync (self):
		pass
