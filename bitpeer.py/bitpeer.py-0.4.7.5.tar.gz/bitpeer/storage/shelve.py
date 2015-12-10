from . import storage
import shelve

class ShelveStorage (storage.Storage):
	def __init__ (self, f):
		self.shelve = shelve.open (f)

	def __getitem__(self, key):
		return self.shelve[key]
		
	def __setitem__(self, key, value):
		self.shelve[key] = value
		
	def __contains__(self, key):
		return key in self.shelve

	def sync (self):
		return self.shelve.sync ()

    
