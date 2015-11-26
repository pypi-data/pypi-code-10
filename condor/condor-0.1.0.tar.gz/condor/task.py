from condor.watcher import Watcher
import sys, traceback

class TaskController:
    def __init__(self, logger):
        self.logger = logger
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def find_task(self, name):
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def replace_names_with_tasks(self):
        for task in self.tasks:

            for action in task.actions:
                if isinstance(action, str):
                    task_to_insert = self.find_task(action)
                    if task_to_insert != None:
                        task.actions.extend(task_to_insert.actions)
                        self.logger.log_warning("Replaced action name {0} with action {1}".format(action, task_to_insert))
                    else:
                        self.logger.log_warning("Cannot find definition for {0} - skipped".format(action))
                    
            print(task.actions)
            task.actions = [action for action in task.actions if callable(action) == True]
            print(task.actions)

    def run(self):
        self.replace_names_with_tasks()
        pipe_args = {}
        for task in self.tasks:
            task_to_run = task
            self.logger.log_general("Starting task {0}".format(task_to_run.name))
            if len(pipe_args.keys()) > 0:
                self.logger.log_general("with arguments {0}".format(pipe_args))
            try:
                pipe_args = task_to_run.run(pipe_args)
                self.logger.log_success("Finished")
            except Exception:
                exception_info = sys.exc_info()
                self.logger.log_error("Aborted due to errors/warnings:")
                traceback.print_exc()
            
class Task:
    def __init__(self, name : str, wdir : str, args : dict, using_pipe : bool = False):
        self.watchers = []
        self.actions = []
        self.name = name
        self.wdir = wdir
        self.args = args
        self.using_pipe = using_pipe

    def add_action(self, action):
        self.actions.append(action)

    def add_watcher(self, watcher):
        self.watchers.append(watcher)
        watcher.register()

    def run(self, pipe_args : dict = {}):
        self.args.update({'pipe_args' : pipe_args})

        for action in self.actions:
            if callable(action):
                return_value = action(self.args)
                if isinstance(return_value, dict):
                    self.args.update(return_value)
            else:
                raise AttributeError("Action should be method or function")

        return self.args