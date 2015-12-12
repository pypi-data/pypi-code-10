def test_get(client, good_session_id):
    session = client.sessions.get(good_session_id)
    assert session['ok']


def test_get_nonexistent(client, bad_session_id):
    session = client.sessions.get(bad_session_id)
    assert not session


def test_create(client):
    session = client.sessions.create('username')
    assert session['cookie_name'] == 'SyncGatewaySession'


def test_delete(client, good_session_id):
    client.sessions.delete(good_session_id)
