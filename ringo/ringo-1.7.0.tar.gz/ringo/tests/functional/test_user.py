import unittest
from ringo.tests.base import IntegrationTestBase
from ringo.tests.crud import User

from ringo.model.user import User as RingoUser


def check_create_cb(check, data, diff, response):
    """Default callback to implement checks after the action has been called.

    :check: CRUD instance
    :data: Dict with submitted data
    :diff: DictDiffer instance
    :response: Response instance

    """
    check.assertEqual(len(diff.removed_keys()), 0)
    check.assertEqual(len(diff.changed_keys(['last_login',
                                             'first_name',
                                             'last_name',
                                             'email'])), 0)
    added = diff.added_objects()
    check.assertEqual(len(added), 1)
    # remove "retype_password" from send data as this is not an
    # attribute of the user model
    del data["retype_password"]
    # remove "password" from send data as will be encrypted after the
    # user has been created.
    del data["password"]
    # remove profildata from send data.
    del data["last_name"]
    del data["first_name"]
    del data["email"]
    check.check_dict_subset(data, added[0])


def check_read_cb(check, data, diff, response):
    """Default callback to implement checks after the action has been called.

    :check: CRUD instance
    :data: Dict with submitted data
    :diff: DictDiffer instance
    :response: Response instance

    """
    check.assertEqual(len(diff.removed_keys()), 0)
    check.assertEqual(len(diff.changed_keys(['last_login'])), 0)
    added = diff.added_objects()
    check.assertEqual(len(added), 0)


def check_update_cb(check, data, diff, response):
    """Default callback to implement checks after the action has been called.

    :check: CRUD instance
    :data: Dict with submitted data
    :diff: DictDiffer instance
    :response: Response instance

    """
    check.assertEqual(len(diff.removed_keys()), 0)
    check.assertEqual(len(diff.changed_keys(['last_login',
                                             'organisation'])), 1)
    added = diff.added_objects()
    check.assertEqual(len(added), 0)


def check_delete_cb(check, data, diff, response):
    """Default callback to implement checks after the action has been called.

    :check: CRUD instance
    :data: Dict with submitted data
    :diff: DictDiffer instance
    :response: Response instance

    """
    check.assertEqual(len(diff.removed_keys()), 1)
    check.assertEqual(len(diff.changed_keys(['last_login'])), 0)
    added = diff.added_objects()
    check.assertEqual(len(added), 0)


class RingoUserTests(IntegrationTestBase):

    def test_list(self):
        self.check_list(RingoUser,
                        {},
                        user=User("admin", "secret"),
                        check_callback=check_read_cb)

    def test_create(self):
        self.check_create(RingoUser,
                          {"login": "test", "password": "test",
                           "retype_password": "test",
                           "first_name": "test",
                           "last_name": "test",
                           "email": "test@test.de"
                           },
                          user=User("admin", "secret"),
                          check_callback=check_create_cb)

    def test_read(self):
        self.check_read(RingoUser,
                        {"id": "1", "login": "admin"},
                        user=User("admin", "secret"),
                        check_callback=check_read_cb)

    def test_update(self):
        self.check_update(RingoUser,
                          {"id": "1", "login": "admin2"},
                          user=User("admin", "secret"),
                          check_callback=check_update_cb)
        self.check_update(RingoUser,
                          {"id": "1", "groups": "admin"},
                          user=User("admin2", "secret"),
                          check_callback=check_update_cb)

    def test_delete(self):
        self.check_delete(RingoUser,
                          {"id": "2", "confirmed": "1"},
                          user=User("admin", "secret"),
                          check_callback=check_delete_cb)


if __name__ == '__main__':
    unittest.main()
