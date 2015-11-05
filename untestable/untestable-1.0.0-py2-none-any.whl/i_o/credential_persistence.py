import abc


class CredentialPersistence(object):
    """
    Persistent access to a single set of credentials
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def persist(self, creds):
        """
        Persist the credentials to the underlying storage.
        Previously persisted credentials will be overridden
        :param creds: an untestable.i_o.credentials.Credentials
        :return: None
        """

    @abc.abstractmethod
    def retrieve(self):
        """
        Retrieve the credentials from the underlying storage
        :return: an untestable.i_o.credentials.Credentials if found,
                 otherwise raises an
                 untestable.i_o.credentials.MissingCredentials exception
        """
