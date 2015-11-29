#unit tests for rooster

import unittest
from rooster.parsedata import *
from rooster.hashfunc import *
from rooster import *

#tests for parsing file value data to data structs
class parsertests(unittest.TestCase):

    def int_test(self):
        self.assertEqual(parse_data('99'), 99)
    def int_test2(self):
        self.assertEqual(parse_data('088'), 88)
    def list_test(self):
        self.assertEqual(parse_data('[1, 2, 3]'), [1, 2, 3])
    def set_test(self):
        self.assertEqual(parse_data('{4, 5, 6, 7, 8}'), {4, 5, 6, 7, 8})
    def tuple_test(self):
        self.assertEqual(parse_data('(9, 9, 8, 7)'), (9, 9, 8, 7))
    def dict_test(self):
        self.assertEqual(parse_data("{'yes':44, 'nope':[1, 2]}"), {'yes':44, 'nope':[1, 2]})
    def str_test(self):
        self.assertEqual(parse_data("[1, 2, 5, 6"), "[1, 2, 5, 6")
    def str_test2(self):
        self.assertEqual(parse_data("{1, 2, 5, 6"), "{1, 2, 5, 6")

class hashtests(unittest.TestCase):

    def isstr_test(self):
        self.assertIsInstance(do_hash('33'), str)
    def collision_test01(self):
        self.assertNotEqual(do_hash('34'), do_hash('your'))
    def collision_test02(self):
        self.assertNotEqual(do_hash('46'), do_hash('apple'))
    def collision_test03(self):
        self.assertNotEqual(do_hash('pear'), do_hash('pears'))
    def collision_test04(self):
        self.assertNotEqual(do_hash('yes'), do_hash('sey'))
    def collision_test05(self):
        self.assertNotEqual(do_hash('who'), do_hash('wh'))
    def same_output_test(self):
        self.assertEqual(do_hash('777'), do_hash('777'))
    def same_output_test2(self):
        self.assertEqual(do_hash('66'), 'b5hl3l4kbkfkvkmk')
    def difference_key_test(self):
        self.assertNotAlmostEqual(do_hash('666'), do_hash('665'))
    def difference_key_test2(self):
        self.assertNotAlmostEqual(do_hash('you'), do_hash('your'))
    def difference_key_test3(self):
        self.assertNotAlmostEqual(do_hash('blue'), do_hash('clue'))
    def difference_key_test4(self):
        self.assertNotAlmostEqual(do_hash('fast'), do_hash('last'))

class get_set_tests(unittest.TestCase):

    def set_key_test01(self):
        set_rooster('yes', 5686, 'roost')
        self.assertTrue(check_key('yes', 'roost'))
    def set_key_test02(self):
        set_rooster('baseball', [1, 2, 3], 'roost')
        self.assertTrue(check_key('baseball', 'roost'))
    def set_key_test03(self):
        set_rooster('basketball', 'bloopers', 'roost')
        self.assertTrue(check_key('basketball', 'roost'))
    def get_key_test01(self):
        self.assertEqual(get_rooster('yes', 'roost'), 5686)
    def get_key_test02(self):
        self.assertEqual(get_rooster('baseball', 'roost'), [1, 2, 3])
    def get_key_test03(self):
        self.assertEqual(get_rooster('basketball', 'roost'), 'bloopers')
    def set_dict_test(self):
        self.assertTrue(set_dict({'red':44, 'blue':33, 'green':22}))



if __name__ == '__main__':
    unittest.main()
