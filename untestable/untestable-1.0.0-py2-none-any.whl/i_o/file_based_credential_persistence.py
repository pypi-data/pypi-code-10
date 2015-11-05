import os

from untestable.i_o.credentials import Credentials, MissingCredentials
from untestable.i_o.credential_persistence import CredentialPersistence


class FileBasedCredentialPersistence(CredentialPersistence):
    """
    A CredentialPersistence implementation that uses a text file to read/write
    the credentials
    """

    def __init__(self, path):
        """
        :param path: the path to the file used for storing credentials
        :return:
        """
        self._filepath = path

    def persist(self, creds):

        with open(self._filepath, "w") as fid:
            fid.write(creds.username)
            fid.write(os.linesep)
            fid.write(creds.password)

    def retrieve(self):
        try:
            with open(self._filepath, "r") as fid:
                try:
                    user, password = fid.read().splitlines()
                except ValueError:
                    raise MissingCredentials
        except IOError:
            raise MissingCredentials

        return Credentials(user, password)
