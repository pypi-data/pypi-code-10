from untestable.flow.flows import CredentialsFlow
from untestable.i_o.credentials import Credentials, MissingCredentials


class SimpleCredentialsCollectionFlow(CredentialsFlow):
    """
    Solicits credentials from the user, returns them
    """

    def __init__(self, io, cred_persistence):
        self._io = io
        self._cred_persistence = cred_persistence

    def run(self):
        """
        Runs the flow
        :return: an untestable.i_o.Credentials object
        """

        # See if there are any stored credentials to use
        try:
            creds = self._cred_persistence.retrieve()

        except MissingCredentials:
            # Collect them
            creds = Credentials(self._io.collect("Username: "),
                                self._io.collect_sensitive("Password: "))

            # See if the user would like them persisted for use next time
            if self._io.collect("Remember [y/n]: ") == "y":
                self._cred_persistence.persist(creds)

        return creds
