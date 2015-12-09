import json
from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller
from ievv_opensource.utils.ievvbuildstatic.shellcommand import ShellCommandMixin
from ievv_opensource.utils.ievvbuildstatic.shellcommand import ShellCommandError


class Plugin(pluginbase.Plugin, ShellCommandMixin):
    name = 'bowerinstall'

    def __init__(self, packages):
        """
        """
        self.packages = packages

    def get_bowerjson_path(self):
        return self.app.get_source_path('bower.json')

    def create_bowerjson(self):
        packagedata = {
            'name': self.app.appname,
            'version': self.app.version,
            "private": True,
            "interactive": False,
            "analytics": False,
            "devDependencies": self.packages
        }
        open(self.get_bowerjson_path(), 'wb').write(
            json.dumps(packagedata, indent=2).encode('utf-8'))

    def get_bower_version(self):
        return None

    def install(self):
        self.app.get_installer(NpmInstaller).queue_install(
            'bower', version=self.get_bower_version())

    def run(self):
        self.get_logger().command_start('Running bower install for {}'.format(
            self.app.get_source_path()))
        self.create_bowerjson()
        bower_executable = self.app.get_installer(NpmInstaller).find_executable('bower')
        try:
            self.run_shell_command(bower_executable,
                                   args=['install'],
                                   kwargs={
                                       '_cwd': self.app.get_source_path()
                                   })
        except ShellCommandError:
            self.get_logger().command_error('bower install failed.')
            raise SystemExit()
        else:
            self.get_logger().command_success('bower install succeeded!')
