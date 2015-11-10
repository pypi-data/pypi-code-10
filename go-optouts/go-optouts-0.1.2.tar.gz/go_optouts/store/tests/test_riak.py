""" Test for the Riak opt out backend. """

from twisted.internet.defer import inlineCallbacks, returnValue
from zope.interface.verify import verifyClass, verifyObject

from vumi.tests.helpers import VumiTestCase
from vumi.tests.helpers import PersistenceHelper

from go.vumitools.opt_out.models import OptOutStore

from go_optouts.store.interface import (
    IOptOutBackend, IOptOutCollection)
from go_optouts.store.riak import (
    RiakOptOutBackend, RiakOptOutCollection)


class TestRiakOptOutBackend(VumiTestCase):
    def setUp(self):
        self.persistence_helper = self.add_helper(
            PersistenceHelper(use_riak=True, is_sync=False))

    @inlineCallbacks
    def mk_backend(self):
        manager = yield self.persistence_helper.get_riak_manager()
        backend = RiakOptOutBackend(manager)
        returnValue(backend)

    def test_class_iface(self):
        self.assertTrue(verifyClass(IOptOutBackend, RiakOptOutBackend))

    @inlineCallbacks
    def test_instance_iface(self):
        backend = yield self.mk_backend()
        self.assertTrue(verifyObject(IOptOutBackend, backend))

    def test_from_config(self):
        config = self.persistence_helper.mk_config({})["riak_manager"]
        backend = RiakOptOutBackend.from_config(config)
        self.assertTrue(isinstance(backend, RiakOptOutBackend))
        self.assertEqual(
            backend.riak_manager.bucket_prefix, config["bucket_prefix"])

    @inlineCallbacks
    def test_get_opt_out_collection(self):
        backend = yield self.mk_backend()
        collection = backend.get_opt_out_collection("owner-1")
        self.assertEqual(collection.store.user_account_key, "owner-1")
        self.assertTrue(isinstance(collection, RiakOptOutCollection))


class TestRiakOptOutCollection(VumiTestCase):
    def setUp(self):
        self.persistence_helper = self.add_helper(
            PersistenceHelper(use_riak=True, is_sync=False))

    @inlineCallbacks
    def mk_collection(self, owner_id):
        manager = yield self.persistence_helper.get_riak_manager()
        store = OptOutStore(manager, owner_id)
        collection = RiakOptOutCollection(store)
        returnValue((store, collection))

    def assertStoreAndCollectionEqual(
            self, opt_store, opt_collection, message, user_account):
        store_data = opt_store.get_data()
        self.assertEqual(store_data["message"], message)
        self.assertEqual(store_data["user_account"], user_account)
        self.assertEqual(opt_collection, {
            'created_at': store_data.get('created_at'),
            'message': message,
            'user_account': user_account,
        })

    def test_class_iface(self):
        self.assertTrue(verifyClass(IOptOutCollection, RiakOptOutCollection))

    @inlineCallbacks
    def test_instance_iface(self):
        _store, collection = yield self.mk_collection("owner-1")
        self.assertTrue(verifyObject(IOptOutCollection, collection))

    @inlineCallbacks
    def test_get_opt_out_exists(self):
        store, collection = yield self.mk_collection("owner-1")
        opt_out_store = yield store.new_opt_out(
            "msisdn", "+12345", {"message_id": "dummy-id"})
        opt_out_coll = yield collection.get("msisdn", "+12345")
        self.assertStoreAndCollectionEqual(
            opt_out_store, opt_out_coll,
            message=u'dummy-id', user_account=u'owner-1')

    @inlineCallbacks
    def test_get_opt_out_absent(self):
        store, collection = yield self.mk_collection("owner-1")
        opt_out = yield collection.get("msisdn", "+12345")
        self.assertEqual(opt_out, None)

    @inlineCallbacks
    def test_put_opt_out_new(self):
        store, collection = yield self.mk_collection("owner-1")
        opt_out_coll = yield collection.put("msisdn", "+12345")
        opt_out_store = yield store.get_opt_out("msisdn", "+12345")
        self.assertStoreAndCollectionEqual(
            opt_out_store, opt_out_coll,
            message=None, user_account=u'owner-1')

    @inlineCallbacks
    def test_delete_opt_out_exists(self):
        store, collection = yield self.mk_collection("owner-1")
        opt_out_store = yield store.new_opt_out(
            "msisdn", "+12345", {"message_id": "dummy-id"})
        opt_out_coll = yield collection.delete("msisdn", "+12345")
        self.assertStoreAndCollectionEqual(
            opt_out_store, opt_out_coll,
            message=u'dummy-id', user_account=u'owner-1')

    @inlineCallbacks
    def test_delete_opt_out_absent(self):
        store, collection = yield self.mk_collection("owner-1")
        opt_out_coll = yield collection.delete("msisdn", "+12345")
        self.assertEqual(opt_out_coll, None)

    @inlineCallbacks
    def test_count_zero(self):
        _store, collection = yield self.mk_collection("owner-1")
        self.assertEqual((yield collection.count()), 0)

    @inlineCallbacks
    def test_count_one(self):
        store, collection = yield self.mk_collection("owner-1")
        yield store.new_opt_out(
            "msisdn", "+12345", {"message_id": "dummy-id"})
        self.assertEqual((yield collection.count()), 1)

    @inlineCallbacks
    def test_count_many(self):
        store, collection = yield self.mk_collection("owner-1")
        for i in range(4):
            yield store.new_opt_out(
                "msisdn", "+1234%d" % i, {"message_id": "dummy-id"})
        self.assertEqual((yield collection.count()), 4)
