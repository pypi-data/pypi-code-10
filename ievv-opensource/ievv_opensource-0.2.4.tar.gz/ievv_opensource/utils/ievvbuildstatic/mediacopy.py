import os
import sh
import shutil
from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller


class Plugin(pluginbase.Plugin):
    name = 'mediacopy'

    def __init__(self, sourcefolder='media'):
        """
        Parameters:
            sourcefolder: The folder where media files is located relative to
                the source folder of the :class:`~ievv_opensource.utils.ievvbuild.config.App`.

        """
        self.sourcefolder = sourcefolder

    def get_sourcefolder_path(self):
        return self.app.get_source_path(self.sourcefolder)

    def get_destinationfolder_path(self):
        return self.app.get_destination_path(self.sourcefolder)

    def run(self):
        destinationfolder = self.get_destinationfolder_path()
        sourcefolder = self.get_sourcefolder_path()
        if os.path.exists(destinationfolder):
            self.get_logger().info('Removing %s', destinationfolder)
            shutil.rmtree(destinationfolder)
        self.get_logger().info('Copying %s -> %s', sourcefolder, destinationfolder)
        shutil.copytree(sourcefolder, destinationfolder)

    def get_watch_folders(self):
        """
        We only watch the folder where the less sources are located,
        so this returns the absolute path of the ``sourcefolder``.
        """
        return [self.app.get_source_path(self.sourcefolder)]
