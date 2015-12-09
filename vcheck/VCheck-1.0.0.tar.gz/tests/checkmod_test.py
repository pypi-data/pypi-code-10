import unittest
import vcheck


class CheckMod_test(unittest.TestCase):
    def mod_test(self):
        import vcheck as _testmod
        cmod = vcheck.CheckMod(_testmod)

        self.assertEqual(cmod.mod, _testmod)
