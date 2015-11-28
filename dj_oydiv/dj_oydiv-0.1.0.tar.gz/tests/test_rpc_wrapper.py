from __future__ import absolute_import, unicode_literals

import mock

from django.test import TestCase

from .models import (
    TestVidyoRealRPC,
    create_test_admin,
)


class RPCWrapperFunctionalTests(TestCase):
    def test_rpc_oydiv_rpc_instantiate_rpc(self):
        with mock.patch('oydiv_rpc.user.User', autospec=True) as user:
            v = TestVidyoRealRPC(_admin_model=create_test_admin())
            v.password = 'asdfsdfsadf'
            v.portal_displayname = 'wingus'
            v.portal_name = 'dingus'
            v.portal_extension = '234234'

            # convert to string to force evaluation of SimpleLazyObject
            str(v.admin_rpc.rpc)

            self.assertEqual(user.call_count, 1)
            self.assertIn(user.call_args[0][0], 'myhost.example.com')

    def test_rpc_create(self):
        with mock.patch('oydiv_rpc.user.User.create', autospec=True), \
            mock.patch('oydiv_rpc.user.User', autospec=True) as user:
            v = TestVidyoRealRPC(_admin_model=create_test_admin())
            v.password = 'asdfsdfsadf'
            v.portal_displayname = 'wingus'
            v.portal_name = 'dingus'
            v.portal_extension = '23241'

            user.return_value.create.return_value = 1337

            v.save()

            self.assertEqual(user.method_calls.count(mock.call().create()), 1)
            self.assertEqual(v.vidyo_entity_id, 1337)

    def test_rpc_delete(self):
        with mock.patch('oydiv_rpc.user.User', autospec=True) as user:
            v = TestVidyoRealRPC(_admin_model=create_test_admin())
            v.password = 'sadfjljasldgds'
            v.portal_displayname = 'wingus'
            v.name = 'dingus'
            v.portal_extension = '234234'
            v.save()
            v.delete()
            self.assertEqual(user.method_calls.count(mock.call().delete()), 1)
