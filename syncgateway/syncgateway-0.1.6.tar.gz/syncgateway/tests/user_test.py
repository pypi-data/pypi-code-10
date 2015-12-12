def test_get(client, good_username):
    user = client.users.get(good_username)
    assert user['name']


def test_exists(client, good_username):
    exists = client.users.exists(good_username)
    assert exists


def test_not_exists(client, bad_username):
    exists = client.users.exists(bad_username)
    assert not exists


def test_get_list(client):
    users = client.users.get_list()
    assert len(users) > 0


def test_add_or_update(client, good_username):
    client.users.add_or_update(
        good_username,
        password='pass',
        name='bob',
        email='test')


def test_create(client, good_username):
    created = client.users.create(good_username)
    assert created


def test_delete(client, good_username):
    client.users.delete(good_username)
