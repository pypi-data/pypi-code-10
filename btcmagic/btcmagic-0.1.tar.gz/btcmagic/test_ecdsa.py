from unittest import TestCase
from btcmagic import convert, ecdsa, hashes
import random

class TestDeterministicGenerate(TestCase):

    def test_all(self):
        # Created with python-ecdsa 0.9
        # Code to make your own vectors:
        # class gen:
        #     def order(self): return 115792089237316195423570985008687907852837564279074904382605163141518161494337
        # dummy = gen()
        # for i in range(10): ecdsa.rfc6979.generate_k(dummy, i, hashlib.sha256, hashlib.sha256(str(i)).digest())
        test_vectors = [
            32783320859482229023646250050688645858316445811207841524283044428614360139869,
            109592113955144883013243055602231029997040992035200230706187150761552110229971,
            65765393578006003630736298397268097590176526363988568884298609868706232621488,
            85563144787585457107933685459469453513056530050186673491900346620874099325918,
            99829559501561741463404068005537785834525504175465914981205926165214632019533,
            7755945018790142325513649272940177083855222863968691658328003977498047013576,
            81516639518483202269820502976089105897400159721845694286620077204726637043798,
            52824159213002398817852821148973968315579759063230697131029801896913602807019,
            44033460667645047622273556650595158811264350043302911918907282441675680538675,
            32396602643737403620316035551493791485834117358805817054817536312402837398361
        ]

        for i, ti in enumerate(test_vectors):
            mine = ecdsa.deterministic_generate_k(hashes.sha256(convert.string_to_bytes(str(i))), i)
            self.assertEqual(
                ti,
                mine,
                "Test vector does not match. Details:\n%s\n%s" % (
                    ti,
                    mine
                )
            )

class TestSigSerialize(TestCase):
    def test_serialize(self):
        for _ in range(10):
            sig = (None, random.randrange(2**256), random.randrange(2**256))
            ser = ecdsa.serialize_sig(sig)
            sig2 = ecdsa.deserialize_sig(ser)
            self.assertEqual(sig, sig2)

class TestPrivSerialize(TestCase):
    def test_serialize(self):
        for _ in range(10):
            priv = ecdsa.random_priv()
            ser = ecdsa.serialize_priv(priv)
            priv2 = ecdsa.deserialize_priv(ser)
            self.assertEqual(priv, priv2)

class TestPubSerialize(TestCase):
    def test_serialize(self):
        for _ in range(10):
            priv = ecdsa.random_priv()
            pub = ecdsa.priv_to_pub(priv)
            self.assertEqual(pub, ecdsa.deserialize_pub(ecdsa.serialize_pub(pub, compressed=False)))
            self.assertEqual(pub, ecdsa.deserialize_pub(ecdsa.serialize_pub(pub, compressed=True)))


class TestSignVerify(TestCase):
    def test_all(self):
        for _ in range(10):
            msghash = convert.random_bytes(32)
            priv = ecdsa.random_priv()
            pub = ecdsa.priv_to_pub(priv)
            sig = ecdsa.sign(msghash, priv)
            self.assertTrue(
                ecdsa.verify(msghash, sig, pub),
                "Verification error"
            )

            self.assertEqual(
                pub,
                ecdsa.recover(msghash, sig),
                "Recovery failed"
            )
