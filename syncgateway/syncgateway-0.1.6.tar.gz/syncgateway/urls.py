from syncgateway import errors


def session_url(base_url, session_id):
    return "{sessions}/{session_id}".format(
        sessions=sessions_url(base_url),
        session_id=session_id
    )


def sessions_url(base_url):
    return "{base_url}/_session".format(
        base_url=base_url
    )


def session_delete_url(base_url, session_id=None, username=None):
    if session_id:
        return session_url(base_url, session_id)
    elif username:
        return sessions_url(user_url(base_url, username))
    else:
        raise errors.SyncGatewayError("Must specify session_id or username")


def user_url(base_url, username):
    return "{users}/{username}".format(
        users=users_url(base_url),
        username=username
    )


def users_url(base_url):
    return "{base_url}/_user".format(
        base_url=base_url
    )


def role_url(base_url, role):
    return "{roles}/{role}".format(
        roles=roles_url(base_url),
        role=role
    )


def roles_url(base_url):
    return "{base_url}/_role".format(
        base_url=base_url
    )


def base_url(url, database):
    if not database:
        raise errors.NoDatabaseSpecifiedError()

    return "{base_url}/{database}".format(
        base_url=url,
        database=database
    )
