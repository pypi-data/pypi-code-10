from termcolor import colored
from ievv_opensource.utils import desktopnotifications


class Logger(object):
    def __init__(self, name):
        self.name = name
        self.colors_enabled = True

    def stdout(self, line):
        print(line.rstrip())

    def stderr(self, line):
        print(line.rstrip())

    def __colorize(self, message, *args, **kwargs):
        if self.colors_enabled:
            return colored(message, *args, **kwargs)
        else:
            return message

    def __colorprint(self, message, *args, **kwargs):
        print(self.__colorize(message, *args, **kwargs))

    def info(self, message):
        self.__colorprint(message, 'blue')

    def warning(self, message):
        self.__colorprint(message, 'yellow')

    def debug(self, message):
        self.__colorprint(message, 'grey')

    def command_start(self, message):
        print()
        self.info(message)

    def __command_end(self, message, *args, **kwargs):
        self.__colorprint(message, *args, **kwargs)
        print()

    def command_error(self, message):
        self.__command_end(message, color='red', attrs=['bold'])
        desktopnotifications.show_message(
            title='ERROR - {}'.format(self.name),
            message=message)

    def command_success(self, message):
        self.__command_end(message, color='green', attrs=['bold'])
        desktopnotifications.show_message(
            title='SUCCESS - {}'.format(self.name),
            message=message)


class BuildLoggable(object):
    def get_logger_name(self):
        raise NotImplementedError()

    def get_logger(self):
        # return logging.getLogger(self.get_logger_name())
        return Logger(name=self.get_logger_name())
