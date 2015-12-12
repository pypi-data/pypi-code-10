import pytest
import requests
import requests_mock

from syncgateway.client import Client


def mock_session():
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(url(), adapter)
    add_session_endpoint(adapter)
    add_user_endpoint(adapter)
    add_role_endpoint(adapter)
    return session


def add_session_endpoint(adapter):
    get_body = {
        "authentication_handlers": ["default", "cookie"],
        "ok": True,
        "userCtx": {
            "channels": {},
            "name": "chef123"
        }
    }
    adapter.register_uri(
        'GET',
        database_url() + '/_session/' + good_session_id(),
        json=get_body,
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )
    adapter.register_uri(
        'GET',
        database_url() + '/_session/' + bad_session_id(),
        status_code=404,
        headers={'Content-Type': 'application/json'}
    )

    post_body = {
        "cookie_name": "SyncGatewaySession",
        "expires": "2014-11-07T16:42:11.675519255-08:00",
        "session_id": "c2425fa7d734bc8c3f6c507854166bef56a5fbc6"
    }
    adapter.register_uri(
        'POST',
        database_url() + '/_session',
        status_code=200,
        json=post_body,
        headers={'Content-Type': 'application/json'}
    )

    adapter.register_uri(
        'DELETE',
        database_url() + '/_session/' + good_session_id(),
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )
    adapter.register_uri(
        'DELETE',
        database_url() + '/_session/' + bad_session_id(),
        status_code=404,
        headers={'Content-Type': 'application/json'}
    )
    adapter.register_uri(
        'DELETE',
        (database_url() + '/_user/' +
         good_username() + '/_session'),
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )


def add_user_endpoint(adapter):
    list_body = ["chef123", "zack", "adam", "pasin"]
    adapter.register_uri(
        'GET',
        database_url() + '/_user',
        json=list_body,
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

    user_body = {
        "name": "chef123",
        "admin_channels": ["admin_events"],
        "all_channels": ["!", "events", "admin_events"]
    }
    adapter.register_uri(
        'GET',
        database_url() + '/_user/' + good_username(),
        json=user_body,
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )
    adapter.register_uri(
        'GET',
        database_url() + '/_user/' + bad_username(),
        status_code=404,
        headers={'Content-Type': 'application/json'}
    )

    adapter.register_uri(
        'POST',
        database_url() + '/_user',
        status_code=201,
        headers={'Content-Type': 'application/json'}
    )

    adapter.register_uri(
        'PUT',
        database_url() + '/_user/' + good_username(),
        json=user_body,
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

    adapter.register_uri(
        'DELETE',
        database_url() + '/_user/' + good_username(),
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )


def add_role_endpoint(adapter):
    list_body = ["moderator", "chef", "san francisco"]
    adapter.register_uri(
        'GET',
        database_url() + '/_role',
        json=list_body,
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

    role_body = {
        "name": "moderator",
        "all_channels": ["!", "recipes-in-progress"]
    }
    adapter.register_uri(
        'GET',
        database_url() + '/_role/' + good_role(),
        json=role_body,
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )
    adapter.register_uri(
        'GET',
        database_url() + '/_role/' + bad_role(),
        status_code=404,
        headers={'Content-Type': 'application/json'}
    )

    adapter.register_uri(
        'POST',
        database_url() + '/_role',
        status_code=201,
        headers={'Content-Type': 'application/json'}
    )

    adapter.register_uri(
        'PUT',
        database_url() + '/_role/' + good_role(),
        json=role_body,
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

    adapter.register_uri(
        'DELETE',
        database_url() + '/_role/' + good_role(),
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )


@pytest.fixture(scope="module")
def client():
    return Client(
        admin_url=url(),
        database=database_name(),
        session=request_session()
    )


@pytest.fixture(scope="module")
def request_session():
    return mock_session()


@pytest.fixture(scope="module")
def database_name():
    return "db"


@pytest.fixture(scope="module")
def url():
    return "http://cb-admin.com"


@pytest.fixture(scope="module")
def database_url():
    return url() + '/' + database_name()


@pytest.fixture(scope="module")
def good_session_id():
    return "sess_id"


@pytest.fixture(scope="module")
def bad_session_id():
    return "bad_sess_id"


@pytest.fixture(scope="module")
def good_username():
    return "user"


@pytest.fixture(scope="module")
def bad_username():
    return "bad_user"


@pytest.fixture(scope="module")
def good_role():
    return "role"


@pytest.fixture(scope="module")
def bad_role():
    return "bad_role"
