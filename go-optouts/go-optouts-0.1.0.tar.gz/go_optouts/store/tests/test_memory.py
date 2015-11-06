"""
Tests for opt_out_http_api.store.memory.
"""
from zope.interface.verify import verifyClass, verifyObject
from go_optouts.store.interface import (
    IOptOutBackend, IOptOutCollection)
from go_optouts.store.memory import (
    MemoryOptOutBackend, MemoryOptOutCollection)
from twisted.trial.unittest import TestCase


class TestMemoryOptOutBackend(TestCase):
    def mk_backend(self):
        return MemoryOptOutBackend()

    def test_class_iface(self):
        self.assertTrue(verifyClass(IOptOutBackend, MemoryOptOutBackend))

    def test_instance_iface(self):
        backend = self.mk_backend()
        self.assertTrue(verifyObject(IOptOutBackend, backend))

    def test_from_config(self):
        backend = MemoryOptOutBackend.from_config({})
        self.assertTrue(isinstance(backend, MemoryOptOutBackend))

    def test_get_opt_out_collection(self):
        backend = self.mk_backend()
        collection = backend.get_opt_out_collection("owner-1")
        self.assertTrue(isinstance(collection, MemoryOptOutCollection))


class TestMemoryOptOutCollection(TestCase):
    def test_setup_class_iface(self):
        self.assertTrue(verifyClass(IOptOutCollection, MemoryOptOutCollection))

    def test_setup_instance_iface(self):
        collection = MemoryOptOutCollection()
        self.assertTrue(verifyObject(IOptOutCollection, collection))

    def test_put_and_get(self):
        store = MemoryOptOutCollection()
        opt1 = store.put("twitter_handle", "@trevor")
        self.assertEqual(len(opt1["id"]), 36)  # length of uuid-4 string
        self.assertEqual(opt1, {
            "id": opt1["id"],
            "address_type": "twitter_handle",
            "address": "@trevor"
        })
        opt2 = store.get("twitter_handle", "@trevor")
        self.assertEqual(opt2, {
            "id": opt1["id"],
            "address_type": "twitter_handle",
            "address": "@trevor"
        })

    def test_get_missing(self):
        store = MemoryOptOutCollection()
        opt3 = store.get("mxit", "praekelt_mxit")
        self.assertEqual(None, opt3)

    def test_delete_missing(self):
        store = MemoryOptOutCollection()
        opt_out_delete = store.delete("twitter_handle", "@trevor")
        self.assertEqual(None, opt_out_delete)

    def test_put_and_delete(self):
        store = MemoryOptOutCollection()
        opt_put = store.put("facebook", "trevor_fb")
        self.assertEqual(len(opt_put["id"]), 36)
        self.assertEqual(opt_put, {
            "id": opt_put["id"],
            "address_type": "facebook",
            "address": "trevor_fb"
        })

        opt_out_del = store.delete("facebook", "trevor_fb")
        self.assertEqual(opt_out_del, {
            "id": opt_put["id"],
            "address_type": "facebook",
            "address": "trevor_fb"
        })

        opt_out_get = store.get("facebook", "trevor_fb")
        self.assertEqual(opt_out_get, None)

    def test_count_zero(self):
        store = MemoryOptOutCollection()
        opt_count_zero = store.count()
        self.assertEqual(opt_count_zero, 0)

    def test_count_one(self):
        store = MemoryOptOutCollection()
        opt_count_one = store.count()
        self.assertEqual(opt_count_one, 0)
        store.put("FB", "fb_PRP")
        opt_count_one = store.count()
        self.assertEqual(opt_count_one, 1)

    def test_count_many(self):
        store = MemoryOptOutCollection()
        opt_count = store.count()
        self.assertEqual(opt_count, 0)
        store.put("facebook", "trevor_fb")
        store.put("mxit", "trevor_mxit")
        opt_count = store.count()
        self.assertEqual(opt_count, 2)
