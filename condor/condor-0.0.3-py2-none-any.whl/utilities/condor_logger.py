from blessings import Terminal

class CondorLogger(object):
    """description of class"""

    def __init__(self):
        self.terminal = Terminal()

    def log_warning(self, message):
        print(self.terminal.yellow + 'WARNING: ' + self.terminal.normal + message)

    def log_success(self, message):
        print(self.terminal.green + 'SUCCESS: ' + self.terminal.normal + message)

    def log_error(self, message):
        print(self.terminal.red + 'ERROR: ' + self.terminal.normal + message)

    def log_general(self, message):
        print(message)
        #print(self.terminal.yellow + 'WARNING: ' + self.terminal.normal + message)



