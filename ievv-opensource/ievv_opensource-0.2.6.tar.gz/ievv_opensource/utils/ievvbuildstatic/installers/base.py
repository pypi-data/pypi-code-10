from ievv_opensource.utils.ievvbuildstatic.buildloggable import BuildLoggable
from ievv_opensource.utils.ievvbuildstatic.shellcommand import ShellCommandMixin


class AbstractInstaller(BuildLoggable, ShellCommandMixin):
    name = None

    def __init__(self, app):
        self.app = app

    def get_logger_name(self):
        return '{}.{}'.format(self.app.get_logger_name(), self.name)
