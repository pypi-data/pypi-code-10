
import logging
import os
from subprocess import Popen, STDOUT, PIPE


class CocoonException(Exception):
    pass


class Task():

    def __init__(self, task_id):
        self.task_id = task_id
        self.task_list = []

    def depends_on(self, other):
        try:
            self.task_list = list(other)
        except TypeError as e:
            self.task_list = [other]
        for task in self.task_list:
            if not isinstance(task, Task):
                raise CocoonException('Expecting a task')

    def describe(self):
        return "[{}] Task".format(self.task_id)

    def dependencies(self):
        return [x.task_id for x in self.task_list]


class ShellTask(Task):

    def __init__(self, task_id, command):
        self.task_id = task_id
        self.command = command
        self.task_list = []

    def execute(self):
        logging.info("shell command: " + self.command)
        # Generates a shell script,
        #sp = Popen(['bash'], stdout=PIPE)

    def describe(self):
        return "[{}] ShellCommand(command={}, depends_on={})".format(self.task_id, self.command, self.dependencies())




