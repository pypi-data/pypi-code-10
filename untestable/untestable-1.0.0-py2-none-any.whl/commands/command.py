import abc


class Command(object):
    """
    Something that interacts with a user to perform some useful activity and
    is identifiable by a simple string command name property.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def can_handle(self, command):
        """
        Whether or not this command can handle the named command
        :param command: The name of the command
        :return: True if this can handle the request, False otherwise
        """
        return

    @abc.abstractmethod
    def name(self):
        """
        The name of the command
        :return: the name
        """
        return

    @abc.abstractmethod
    def run(self):
        """
        Performs the command
        :return: None
        """
        return

