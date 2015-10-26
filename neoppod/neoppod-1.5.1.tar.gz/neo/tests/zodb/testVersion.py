#
# Copyright (C) 2009-2015  Nexedi SA
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from ZODB.tests.VersionStorage import VersionStorage
from ZODB.tests.TransactionalUndoVersionStorage import \
         TransactionalUndoVersionStorage
from ZODB.tests.StorageTestBase import StorageTestBase

from . import ZODBTestCase

class VersionTests(ZODBTestCase, StorageTestBase, VersionStorage,
        TransactionalUndoVersionStorage):
    pass

if __name__ == "__main__":
    suite = unittest.makeSuite(VersionTests, 'check')
    unittest.main(defaultTest='suite')

