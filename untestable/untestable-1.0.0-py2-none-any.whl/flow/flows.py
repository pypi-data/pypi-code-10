import abc


class CredentialsFlow(object):
    """
    A re-usable user interaction that collects Credential information
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self):
        """
        Runs the flow
        :return: the untestable.i_o.credentials.Credentials object
                 encapsulating the data collected
        """
