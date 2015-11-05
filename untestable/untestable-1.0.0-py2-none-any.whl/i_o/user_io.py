import abc


class UserIO(object):
    """Prompt a user for information. Display information back to a user."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def collect(self, prompt):
        """
        Prompt a user for information, return the information entered
        :param prompt: a string to display describing the information needed
        :return: the information collected as a string
        """

    @abc.abstractmethod
    def collect_sensitive(self, prompt):
        """
        Similar to collect(), except that the information being collected
        is sensitive so care should be taken to appropriately obscure/protect
        the information during display.
        :param prompt: a string to display describing the information needed
        :return: the information collected as a string
        """

    @abc.abstractmethod
    def display(self, content):
        """
        Display information to the user
        :param content: the information to display
        :return: nothing
        """
