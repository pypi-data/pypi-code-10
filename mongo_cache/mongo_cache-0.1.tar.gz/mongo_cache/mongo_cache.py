from pymongo import MongoClient
import time
class MongoCache(object):
	def __init__(self, mongo_db = MongoClient().cache_database, size=0, cache_collection="cache_collection"):
		self.cache_collection=mongo_db[cache_collection]
		#todo handle size

	def get(self, key, lmbda=None, expires_in = None, expires_at=None):
		obj = self.cache_collection.find_one({"_id": key})
		now = time.time()
		if obj and obj.get("expires_at", now + 10) > now:#valid
			return obj["value"]
		elif lmbda: # not present or expired
			return self.set(key, lmbda(), expires_in, expires_at)["value"]
		else:
			self.unset(key)

	def set(self, key, value, expires_in = None, expires_at=None):
		obj = {"_id": key, "value": value}
		if expires_at:
			obj["expires_at"] = expires_at
		elif expires_in:
			obj["expires_at"] = time.time() + int(expires_in)
		self.cache_collection.replace_one({"_id": key}, obj, upsert=True)
		return obj

	def unset(self, key):
		self.cache_collection.delete_one({"_id": key})

	def clear(self):
		self.cache_collection.drop()

	def __getitem__(self, key):
		return self.get(key)

	def __setitem__(self, key, value):
		return self.set(key, value)

