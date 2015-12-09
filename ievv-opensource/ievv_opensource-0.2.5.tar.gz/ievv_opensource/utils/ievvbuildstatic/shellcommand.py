from __future__ import unicode_literals
from __future__ import print_function
import sh


class ShellCommandError(Exception):
    """
    Raised when :meth:`.BuildLoggable.run_shell_command` fails.
    """


class ShellCommandMixin(object):
    """
    Shell command mixin - for classes that need to run shell commands.

    Requires :class:`~ievv_opensource.utils.ievvbuildstatic.buildloggable.BuildLoggable`.
    """
    def log_shell_command_stdout(self, line):
        self.get_logger().stdout(line.rstrip())

    def log_shell_command_stderr(self, line):
        self.get_logger().stderr(line.rstrip())

    def run_shell_command(self, executable, args=None, kwargs=None):
        command = sh.Command(executable)
        args = args or []
        kwargs = kwargs or {}
        try:
            command(*args,
                    _out=self.log_shell_command_stdout,
                    _err=self.log_shell_command_stderr,
                    **kwargs)
        except sh.ErrorReturnCode:
            # We do not need to show any more errors here - they
            # have already been printed by the _out and _err handlers.
            raise ShellCommandError()
