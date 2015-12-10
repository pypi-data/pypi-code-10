from termcolor import colored
from ievv_opensource.utils import desktopnotifications


class Logger(object):
    """
    Logger class used by :class:`.BuildLoggable`.
    """
    def __init__(self, name):
        """
        Parameters:
            name: The name of the logger.
        """
        self.name = name
        self.colors_enabled = True

    def stdout(self, line):
        """
        Use this to redirecting sys.stdout when running shell commands.
        """
        print(line.rstrip())

    def stderr(self, line):
        """
        Use this to redirecting sys.stderr when running shell commands.
        """
        print(line.rstrip())

    def __colorize(self, message, *args, **kwargs):
        if self.colors_enabled:
            return colored(message, *args, **kwargs)
        else:
            return message

    def __colorprint(self, message, *args, **kwargs):
        print(self.__colorize(message, *args, **kwargs))

    def info(self, message):
        """
        Log an info message.
        """
        self.__colorprint(message, 'blue')

    def warning(self, message):
        """
        Log a warning message.
        """
        self.__colorprint(message, 'yellow')

    def debug(self, message):
        """
        Log a debug message.
        """
        self.__colorprint(message, 'grey')

    def command_start(self, message):
        """
        Log the start of a command. This should be used in the beginning
        of each :meth:`ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin.run`.
        """
        print()
        self.info(message)

    def __command_end(self, message, *args, **kwargs):
        self.__colorprint(message, *args, **kwargs)
        print()

    def command_error(self, message):
        """
        Log failing end of a command. This should be used in
        :meth:`ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin.run`
        when the task fails.
        """
        self.__command_end(message, color='red', attrs=['bold'])
        desktopnotifications.show_message(
            title='ERROR - {}'.format(self.name),
            message=message)

    def command_success(self, message):
        """
        Log successful end of a command. This should be used in
        :meth:`ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin.run`
        when the task succeeds.
        """
        self.__command_end(message, color='green', attrs=['bold'])
        desktopnotifications.show_message(
            title='SUCCESS - {}'.format(self.name),
            message=message)


class BuildLoggable(object):
    """
    Mixin class that takes care of logging for all the classes
    in the ``ievvbuildstatic`` package.

    Subclasses must override :meth:`.~BuildLoggable.get_logger_name`,
    and use :meth:`.~BuildLoggable.get_logger`.
    """
    def get_logger_name(self):
        raise NotImplementedError()

    def get_logger(self):
        """
        Get an instance of :meth:`.Logger` with :meth:`.get_logger_name`
        as the logger name.
        """
        return Logger(name=self.get_logger_name())
