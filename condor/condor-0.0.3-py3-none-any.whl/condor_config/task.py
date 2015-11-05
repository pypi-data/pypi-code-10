from condor_config.watcher import Watcher

class TaskController:
    def __init__(self, logger):
        self.logger = logger
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def run(self):
        pipe_args = {}
        for task in self.tasks:
            #self.logger.log_general("Starting task {0}".format(task.name))
            if len(pipe_args.keys()) > 0:
             #   self.logger.log_general
                print("with arguments {0}".format(pipe_args))
            pipe_args = task.run(pipe_args)

class Task:
	def __init__(self, name : str, wdir : str, args : dict, using_pipe : bool = False):
		self.watchers = []
		self.action = None
		self.name = name
		self.wdir = wdir
		self.args = args
		self.using_pipe = using_pipe

	def add_action(self, action):
		if not callable(action):
			AttribureError("Action should be callable")
		self.action = action

	def add_watcher(self, watcher):
		self.watchers.append(watcher)
		watcher.register()

	def run(self, pipe_args : dict = {}):
		if self.action != None:
			if self.using_pipe:
				self.args.update({'pipe_args' : pipe_args})
			return self.action(self.args)
		else:
			return {}