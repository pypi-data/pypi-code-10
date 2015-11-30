#!/usr/bin/env python3

import unittest
import netstr

class TestCase(unittest.TestCase):
  def setUp(self):
    self.junk = b'junkdata' * 10
    self.binary_data = b'12:\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x21,' + self.junk
    self.ascii_data = b'hello world!'

  def test_length(self):
    self.assertEqual(netstr.length(self.binary_data), len(self.ascii_data))

  def test_size(self):
    self.assertEqual(netstr.size(self.binary_data), len(self.binary_data) - len(self.junk))

  def test_encode(self):
    self.assertEqual(netstr.encode(self.ascii_data), self.binary_data[:-len(self.junk)])

  def test_decode(self):
    self.assertEqual(netstr.decode(self.binary_data), self.ascii_data)

  def test_bad_input(self):
    clbk1 = lambda: netstr.decode(b'-' + self.binary_data)
    clbk2 = lambda: netstr.decode(self.binary_data.replace(b',', b'.'))

    self.assertRaises(ValueError, clbk1)
    self.assertRaises(ValueError, clbk2)

  def test_validity(self):
    clbk = lambda: self.binary_data.replace(b',', b'.')

    self.assertEqual(netstr.is_valid(self.binary_data), True)
    self.assertEqual(netstr.is_valid(clbk()), False)

if __name__ == '__main__':
  unittest.main()
