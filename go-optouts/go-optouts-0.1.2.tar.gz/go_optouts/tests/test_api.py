from twisted.web.server import Site
from twisted.internet.defer import inlineCallbacks

from vumi.tests.helpers import VumiTestCase

from go_optouts.api import API
from go_optouts.auth import RequestHeaderAuth
from go_optouts.store.memory import MemoryOptOutBackend
from go_optouts.tests.utils import SiteHelper


class TestApi(VumiTestCase):
    @inlineCallbacks
    def setUp(self):
        self.owner_id = "owner-1"
        self.backend = MemoryOptOutBackend()
        self.auth = RequestHeaderAuth()
        self.collection = self.backend.get_opt_out_collection(self.owner_id)
        self.app = API(self.backend, self.auth)
        self.site = Site(self.app.app.resource())

        self.site_helper = yield self.add_helper(
            SiteHelper(self.site, self.owner_header))

    def owner_header(self, owner=True, **kw):
        if owner:
            kw.setdefault("headers", {})
            kw["headers"]["X-Owner-ID"] = self.owner_id
        return kw

# Tests

    @inlineCallbacks
    def test_no_owner(self):
        resp = yield self.site_helper.get("/count", owner=False)
        self.assertEqual(resp.code, 401)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 401,
                "reason": "Owner ID not valid.",
            },
        })

    @inlineCallbacks
    def test_opt_out_found(self):
        existing_opt_out = yield self.collection.put("msisdn", "+273121100")
        resp = yield self.site_helper.get("/msisdn/+273121100")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": existing_opt_out["id"],
                "address_type": "msisdn",
                "address": "+273121100",
            },
        })

    @inlineCallbacks
    def test_opt_out_not_found(self):
        resp = yield self.site_helper.get("/mxit/+369963")
        self.assertEqual(resp.code, 404)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 404,
                "reason": "Opt out not found.",
            },
        })

    @inlineCallbacks
    def test_opt_out_created(self):
        resp = yield self.site_helper.put("/msisdn/+273121100")
        created_opt_out = yield self.collection.get("msisdn", "+273121100")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": created_opt_out["id"],
                "address_type": "msisdn",
                "address": "+273121100"
            },
        })

    @inlineCallbacks
    def test_opt_out_conflict(self):
        yield self.collection.put("msisdn", "+273121100")
        response = yield self.site_helper.put("/msisdn/+273121100")
        self.assertEqual(response.code, 409)
        data = yield response.json()
        self.assertEqual(data, {
            "status": {
                "code": 409,
                "reason": "Opt out already exists."
            },
        })

    @inlineCallbacks
    def test_opt_out_deleted(self):
        delete_opt_out = yield self.collection.put("whatsapp", "@whatsup")
        resp = yield self.site_helper.delete("/whatsapp/@whatsup")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": delete_opt_out["id"],
                "address_type": "whatsapp",
                "address": "@whatsup"
            },
        })

    @inlineCallbacks
    def test_opt_out_nothing_to_delete(self):
        response = yield self.site_helper.delete("/whatsapp/+2716230199")
        self.assertEqual(response.code, 404)
        data = yield response.json()
        self.assertEqual(data, {
            "status": {
                "code": 404,
                "reason": "There\'s nothing to delete."
            },
        })

    @inlineCallbacks
    def test_opt_out_count_zero_opt_out(self):
        resp = yield self.site_helper.get("/count")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "opt_out_count": 0,
            "status": {
                "code": 200,
                "reason": "OK"
            },
        })

    @inlineCallbacks
    def test_opt_out_count_two_opt_outs(self):
        yield self.collection.put("slack", "@slack")
        yield self.collection.put("twitter_handle", "@trevor_october")
        resp = yield self.site_helper.get("/count")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "opt_out_count": 2,
            "status": {
                "code": 200,
                "reason": "OK"
            },
        })

    @inlineCallbacks
    def test_opt_out_count_three_opt_outs(self):
        yield self.collection.put("whatsapp", "+27782635432")
        yield self.collection.put("mxit", "@trevor_mxit")
        yield self.collection.put("facebook", "fb")
        resp = yield self.site_helper.get("/count")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "opt_out_count": 3,
            "status": {
                "code": 200,
                "reason": "OK"
            },
        })
