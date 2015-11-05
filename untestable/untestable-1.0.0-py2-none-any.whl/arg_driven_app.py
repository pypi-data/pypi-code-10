import abc


class ArgDrivenApp(object):
    """An app that runs given a context described by a list of arguments."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self, argv):
        """
        Run the application
        :param argv: Arguments that describe how the app should run
        :return: nothing
        """
