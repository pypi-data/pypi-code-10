from watchdog.observers import Observer

from ievv_opensource.utils.ievvbuildstatic.buildloggable import BuildLoggable
from ievv_opensource.utils.ievvbuildstatic.watcher import EventHandler


class Plugin(BuildLoggable):
    name = None

    def __init__(self):
        self.app = None
        self.__is_running = False
        self.is_executing = False

    def install(self):
        """
        Install any packages required for this plugin.

        Should use :meth:`ievv_opensource.utils.ievvbuild.config.App.get_installer`.

        Examples:

            Install an npm package::

                def install(self):
                    self.app.get_installer(NpmInstaller).install(
                        'somepackage')
                    self.app.get_installer(NpmInstaller).install(
                        'otherpackage', version='~1.0.0')
        """

    def run(self):
        pass

    def watch(self):
        watchfolders = self.get_watch_folders()
        if not watchfolders:
            return
        watchregexes = self.get_watch_regexes()
        event_handler = EventHandler(
            plugin=self,
            regexes=watchregexes
        )
        observer = Observer()
        for watchfolder in watchfolders:
            observer.schedule(event_handler, watchfolder, recursive=True)
        self.get_logger().info('Starting watcher for folders %r with regexes %r',
                               watchfolders, watchregexes)
        observer.start()
        return observer

    def get_watch_regexes(self):
        return [r'^.*$']

    def get_watch_folders(self):
        return []

    def get_logger_name(self):
        return '{}.{}'.format(self.app.get_logger_name(), self.name)
