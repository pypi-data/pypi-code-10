# -*- coding: utf-8 -*-
import json
import unittest

from ebcloudstore.client import EbStore


class EbStoreTest(unittest.TestCase):
    def setUp(self):
        self.tclass = EbStore("562e18936f43f6597cecb9d4")

    def tearDown(self):
        pass

    def testupload_by_filename(self):
        filepath = "/home/tsengdavid/Pictures/001OgTcAgy6Mkij36BC0c&690.jpg"
        self.assertIsInstance(self.tclass.upload(filepath), str, "result error")

    def testunsupported(self):
        filepath = "/home/tsengdavid/Documents/Test/my.xmind"
        self.assertIsInstance(self.tclass.upload(filepath), str, "result error")

    def testupload_by_bytes(self):
        filepath = "/home/tsengdavid/Pictures/001OgTcAgy6Mkij36BC0c&690.jpg"
        file = open(filepath, "rb")
        r = self.tclass.upload(file, filename="my.jpg", file_type="image/jpeg")
        ret = json.loads(r)
        print(r)
        self.assertEqual(ret["code"], 0, "result error")


if __name__ == '__main__':
    unittest.main()