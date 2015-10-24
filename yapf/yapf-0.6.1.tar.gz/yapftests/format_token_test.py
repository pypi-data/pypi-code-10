# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for yapf.format_token."""

import unittest

from lib2to3 import pytree
from lib2to3.pgen2 import token
from yapf.yapflib import format_token


class FormatTokenTest(unittest.TestCase):

  def testSimple(self):
    tok = format_token.FormatToken(pytree.Leaf(token.STRING, "'hello world'"))
    self.assertEqual("FormatToken(name=STRING, value='hello world')", str(tok))
    self.assertTrue(tok.is_string)

    tok = format_token.FormatToken(pytree.Leaf(token.COMMENT, "# A comment"))
    self.assertEqual("FormatToken(name=COMMENT, value=# A comment)", str(tok))
    self.assertTrue(tok.is_comment)


if __name__ == "__main__":
  unittest.main()
