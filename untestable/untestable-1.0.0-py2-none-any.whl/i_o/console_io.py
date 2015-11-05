import getpass

from untestable.i_o.user_io import UserIO


class ConsoleIO(UserIO):
    """
    IO to the system console
    """

    def __init__(self):
        return

    def collect(self, prompt):
        return raw_input(prompt)

    def collect_sensitive(self, prompt):
        return getpass.getpass(prompt)

    def display(self, content):
        print content
