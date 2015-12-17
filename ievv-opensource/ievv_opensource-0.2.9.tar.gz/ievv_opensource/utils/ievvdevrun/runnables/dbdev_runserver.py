import sys
from django.conf import settings

from ievv_opensource.utils.ievvdevrun.runnables import base


class RunnableThread(base.ShellCommandRunnableThread):
    """
    Django-DBdev run database runnable thread.

    Examples:

        You can just add it to your Django development settings with::

            IEVVTASKS_DEVELOPRUN_THREADLIST = {
                'default': ievvdevrun.config.RunnableThreadList(
                    ievvdevrun.runnables.dbdev_runserver.RunnableThread()
                )
            }

    """

    def get_logger_name(self):
        return 'Django-dbdev database server: {!r}'.format(
            settings.DATABASES['default']
        )

    def get_command_config(self):
        return {
            'executable': sys.executable,
            'args': ['manage.py', 'dbdev_fgrunserver']
        }
