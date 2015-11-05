class Credentials(object):
    """
    A set of credentials for authenticating access to things.
    """

    __slots__ = ['username', 'password']

    def __init__(self, username, password):
        """
        Initializes Credentials
        :param username: A username defining a unique identity
        :param password: A password authenticating an identity
        :return: Credentials
        """
        self.username = username
        self.password = password


class MissingCredentials(Exception):
    """
    Credentials weren't found
    """

