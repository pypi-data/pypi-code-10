import abc


class BitbucketClient(object):
    """
    Access to a set of remote Bitbucket services for reading and manipulating
    Bitbucket objects
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_user(self, creds):
        """
        Get a user profile.
        See bitbucket's official documentation_ for details

        .. _documentation: https://confluence.atlassian.com/bitbucket/user-endpoint-296092264.html#userEndpoint-GETauserprofile

        :param creds: untestable.i_o.credentials.Credentials
        :return: BitbucketResponse
        """

    @abc.abstractmethod
    def get_user_repositories(self, creds):
        """
        Get a user's set of repositories.
        See bitbucket's official documentation_ for details

        .. _documentation: https://confluence.atlassian.com/bitbucket/user-endpoint-296092264.html#userEndpoint-GETalistofrepositoriesvisibletoanaccount

        :param creds: untestable.i_o.credentials.Credentials
        :return: BitbucketResponse
        """


class BitbucketResponse(object):
    """
    Encapsulates the result of a Bitbucket Service request
    """

    __slots__ = ['status_code', 'reason', 'body']

    def __init__(self, status_code, reason, body):
        self.status_code = status_code
        self.reason = reason
        self.body = body
