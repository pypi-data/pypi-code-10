def test_get(client, good_role):
    role = client.roles.get(good_role)
    assert role['name']


def test_get_list(client):
    roles = client.roles.get_list()
    assert len(roles) > 0


def test_add_or_update(client, good_role):
    client.roles.add_or_update(
        good_role,
        admin_channels=['channel']
    )


def test_create(client, good_role):
    created = client.roles.create(good_role)
    assert created


def test_delete(client, good_role):
    client.roles.delete(good_role)
