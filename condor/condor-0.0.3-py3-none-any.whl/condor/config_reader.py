from task import Task, TaskController
from watcher import Watcher, WatcherController
import sys

watcher_controller = WatcherController()
task_controller = TaskController()

def setup(name, wdir, task):

    print(sys.argv)

    print("Setting up Condor for {0}".format(name))

    for t in task:
        print("Creating task {0}".format(t['name']) )

        condor_task = Task(t['name'], wdir, t['args'], t['pipe'])
        if 'watch' in t.keys() and 'action' in t.keys():
            raise AttributeError("Task should not contain both action and watchers")
        if 'action' in t.keys():
            condor_task.add_action(t['action'])
        if 'watch' in t.keys():
            for w in t['watch']:
                condor_watcher = Watcher(wdir + w['path'], w['pattern'], w['action'], watcher_controller)
                condor_task.add_watcher(condor_watcher)
                print("Added watcher for task {0} for {1}".format(condor_task.name, condor_watcher.path + condor_watcher.pattern))
        task_controller.add_task(condor_task)

    watcher_controller.start()

    print("Condor is set up and now running...")

    task_controller.run()


