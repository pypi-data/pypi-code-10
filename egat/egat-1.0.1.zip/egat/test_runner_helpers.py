from collections import deque
from threading import Thread
import sys
import traceback

class WorkProvider():
    _work_nodes = None
    _failed_ex_groups = None

    def __init__(self):
        self._work_nodes = deque()
        self._failed_ex_groups = set()

    def add_nodes(self, *work_nodes):
        """Takes a TestSet subclass object and a list of function objects in that 
        class and adds them as a node in the WorkProvider's work."""
        self._work_nodes.extend(work_nodes)

    def get_next_node(self):
        """Finds and returns the next available node of work and returns it. When 
        the work is done the 'finished_with_node' method must be called. If no work 
        is currently available, this method will return None."""
        return self._work_nodes.popleft() if self._work_nodes else None

    def finished_with_node(self, work_node):
        """Takes a work node and releases its resources. Must be called for each 
        node returned from 'get_next_node'."""
        pass

    def has_work(self):
        """Returns True if this WorkProvider still has unclaimed work, and False 
        otherwise."""
        return len(self._work_nodes) > 0

    def add_failed_ex_groups(self, failed_ex_groups, environment):
        """Takes a list of Execution Groups and adds them to this WorkProvider's list
        of failed Execution Groups. Should be called if any of this WorkProvider's tests 
        with execution groups fail.
        
        The environment dictionary is not used. It is still required so that 
        subclasses like the AuthoThreadedWorkProvider can make use of it."""
        self._failed_ex_groups = self._failed_ex_groups.union(failed_ex_groups)

    def has_failed_ex_groups(self, environment, *execution_groups):
        """Takes a variable number of execution groups and returns True if any of 
        them have failed and False otherwise."""
        for ex_group in execution_groups:
            if ex_group in self._failed_ex_groups:
                return True
        return False


class TestFunctionType():
    TEST = 0
    SETUP = 1
    TEARDOWN = 2

class WorkerThread(Thread):
    """This class draws work from the WorkProvider and executes it."""
    work_provider = None
    logger = None
    cur_node = None
    thread_num = None

    def __init__(self, work_provider, logger, thread_num=None):
        """Requires a WorkManager, a WorkProvider, and a TestLogger."""
        super(WorkerThread, self).__init__()
        self.work_provider = work_provider
        self.logger = logger
        self.thread_num = thread_num

    def run(self):
        """Called when this WorkerThread is started."""
        while self.work_provider.has_work():
            cur_node = self.work_provider.get_next_node()

            if cur_node:
                self.run_tests_for_node(cur_node)
                self.work_provider.finished_with_node(cur_node)

    def run_tests_for_node(self, node):
        """Takes a WorkNode and runs the tests it contains."""
        classname = node.test_class.__name__
        instance = node.get_test_class_instance()
        cls = node.test_class

        # if this node contains only one function, check for failed execution groups
        # and don't instatiate the class or call setup
        if len(node.test_funcs) == 1:
            func = node.test_funcs[0]
            if WorkerThread.has_failed_ex_groups(node.test_class, func, node.test_env, self.work_provider):
                self.logger.skippingTestFunction(instance, func, thread_num=self.thread_num)
                return
                
        # Try to call the class's setup method
        if hasattr(cls, 'setup') and callable(cls.setup):
            self.run_and_report(node, cls.setup, TestFunctionType.SETUP)

        # Run all the test functions
        for func in node.test_funcs:
            self.run_and_report(node, func)

        # Try to call the class's teardown method
        if hasattr(cls, 'teardown') and callable(cls.teardown):
            self.run_and_report(node, cls.teardown, TestFunctionType.TEARDOWN)

    def run_and_report(self, node, func, func_type=TestFunctionType.TEST):
        """
            Takes a node and a test function on that node and runs the test function,
            reporting appropriately to the test logger. Can also handle setup and
            teardown methods when a TestFunctionType is specified.
        """
        instance = node.get_test_class_instance()

        # Check for failed execution groups
        if WorkerThread.has_failed_ex_groups(node.test_class, func, node.test_env, self.work_provider):
            self.logger.skippingTestFunction(instance, func, func_type, thread_num=self.thread_num)
            return

        self.logger.runningTestFunction(instance, func, func_type, thread_num=self.thread_num)
        try:
            func(instance)
        except:
            e = sys.exc_info()[0]
            tb = traceback.format_exc()
            self.work_provider.add_failed_ex_groups(
                WorkerThread.get_ex_groups(node.test_class, func),
                node.test_env
            )

            self.logger.foundException(instance, func, e, tb, func_type, thread_num=self.thread_num)

        self.logger.finishedTestFunction(instance, func, func_type, thread_num=self.thread_num)

    @staticmethod
    def has_failed_ex_groups(test_class, func, env, work_provider):
        """Takes a class and a function object in that class and checks the 
        WorkProvider to see if any of the Execution Groups the function or class is a
        member of have failed. Returns True if the function is a member of a failed 
        Execution Group and False otherwise."""
        execution_groups = set(
            WorkerThread.get_ex_groups(test_class, func)
        )
        return work_provider.has_failed_ex_groups(env, *execution_groups)

    @staticmethod
    def get_ex_groups(*func_or_class):
        """Takes a variable number of objects and safely tries to get their Execution
        Groups. Returns either a flat list of all the object's Execution Groups or an 
        empty list."""
        if type(func_or_class) is tuple and len(func_or_class) > 1:
            return [g for ls in map(WorkerThread.get_ex_groups, func_or_class) for g in ls]
        elif hasattr(func_or_class[0], 'execution_groups'):
            return func_or_class[0].execution_groups
        else:
            return []

class WorkNode(object):
    """A class that represents a node in the work of a WorkPool. Each node
    represents a unit of work (tests to be run) and defines the resources it needs
    to share with other nodes (SharedResources). Each node has edges that connect
    it to other nodes that share its SharedResources and thus cannot be run at the
    same time."""
    class_resources = None # a list of SharedResource classes this class needs
    test_class = None # The class containing tests for this node
    test_funcs = None # The tests functions for this node
    test_config = None
    test_env = None
    test_class_is_setup = None
    test_class_is_torndown = None
    _test_class_inst = None # An instance of the test class

    def __init__(self, test_class, test_funcs, config={}, env={}):
        """Takes a TestSet subclass, and a list of test methods in that TestSet
        subclass."""
        self.test_class = test_class
        self.test_funcs = test_funcs
        self.test_config = config
        self.test_env = env
        self.test_class_is_setup = False
        self.test_class_is_torndown = False
        self.resources = set()

        # Add class resources
        self.class_resources = getattr(test_class, 'resources', [])

    def get_test_class_instance(self):
        """Gets an instance of the test_class, creating one if necessary."""
        if not self._test_class_inst:
            self._test_class_inst = self.test_class()
            setattr(self._test_class_inst, 'configuration', self.test_config)
            setattr(self._test_class_inst, 'environment', self.test_env)
        return self._test_class_inst
