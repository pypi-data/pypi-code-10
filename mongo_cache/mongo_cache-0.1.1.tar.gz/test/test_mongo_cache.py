import unittest
from mongo_cache.mongo_cache import MongoCache
import time

class TestMongoCache(unittest.TestCase):
	def setUp(self):
		self.cache = MongoCache()
		self.cache.clear()
		self.cache.set("test", 1)
		self.cache.set("test1", 2)

	def test_set_get_basic(self):
		self.assertEqual(self.cache.get("test"), 1)
		self.assertEqual(self.cache.get("test1"), 2)

	def test_unset(self):
		self.cache.unset("test1")
		self.assertEqual(self.cache.get("test1"), None)

	def test_replace(self):
		self.assertEqual(self.cache.get("test"), 1)
		self.cache.set("test", 42)
		self.assertEqual(self.cache.get("test"), 42)

	def test_get_lambda(self):
		self.assertEqual(self.cache.get("lambda"), None)
		self.assertEqual(self.cache.get("lambda", lambda : "lambda"), "lambda")
		self.assertEqual(self.cache.get("lambda"), "lambda")

	def test_expires_in(self):
		self.cache.set("set", "set", expires_in= -1)
		self.cache.get("get", lambda: "get", expires_in= -1)
		self.assertTrue(self.cache.cache_collection.find_one({"_id": "set"})) # value still present
		self.assertEqual(self.cache.get("set"), None) # value deleted due to expiry
		self.assertFalse(self.cache.cache_collection.find_one({"_id": "set"}))
		self.assertEqual(self.cache.get("get"), None)

	def test_expires_at(self):
		self.cache.set("set", "set", expires_at= time.time() -1)
		self.cache.get("get", lambda: "get", expires_at= time.time() -1)
		self.assertTrue(self.cache.cache_collection.find_one({"_id": "set"})) # value still present
		self.assertEqual(self.cache.get("set"), None) # value deleted due to expiry
		self.assertFalse(self.cache.cache_collection.find_one({"_id": "set"}))
		self.assertEqual(self.cache.get("get"), None)

	def test_complex_values(self):
		complex_obj = {"this": "is", "a": "complex object"}
		self.cache.set("complex", complex_obj)
		self.assertEqual(self.cache.get("complex"), complex_obj)

	def test_setitem_getitem(self):
		self.cache["test2"] = 1
		self.assertEqual(self.cache["test2"], 1)
		self.assertEqual(self.cache["test3"], None)

