from egat.test_loader import TestLoader
from egat.test_runner_helpers import WorkProvider, WorkerThread, TestFunctionType
from threading import Lock
from egat.testset import ExecutionOrder
import sys
import traceback

class AutoThreadedTestRunner():
    """A class used to run TestSet tests."""
    tests = [] # Should be a list of tuples like [(class, [func1, func2]) ...]
    work_provider = None
    logger = None
    number_of_threads = None

    def __init__(self, logger, number_of_threads=1, selenium_debugging=True):
        """Initializes the AutoThreadedTestRunner. The logger should be a subclass of
        TestLogger."""
        self.number_of_threads = number_of_threads
        self.logger = logger
        self.work_provider = AutoThreadedWorkProvider()

    def add_tests(self, test_json):
        """Takes a list of tests in the format required by the configuration file 
        and adds them to the tests that this TestRunner will run."""
        tests_objs = AutoThreadedTestRunner._build_tests(test_json)
        work_nodes = TestLoader.get_work_nodes_for_tests(tests_objs)
        self.work_provider.add_nodes(*work_nodes)

    def run_tests(self):
        """Runs the tests that have been added to this AutoThreadedTestRunner."""
        self.logger.startingTests()
        workers = []

        for i in range(self.number_of_threads):
            worker = AutoThreadedWorkerThread(self.work_provider, self.logger, thread_num=i)
            worker.start()
            workers.append(worker)

        for worker in workers:
            worker.join()
        return self.logger.finishedTests()

    @staticmethod
    def _build_tests(test_obj, parent_configuration={}, parent_environment={}):
        """Takes a JSON test object like the one defined in the configuration file
        and returns a flat list of test objects in the format that add_tests
        requires. This method takes care of building out the proper configurations
        and environments for nested tests."""
        flat_tests = []
        # If tests is a test name
        # Base case
        if type(test_obj) in [str, unicode]:
            test = {}
            test['configuration'] = parent_configuration
            test['environment'] = parent_environment
            test['test'] = test_obj
            flat_tests.append(test)

        # current_tests is a test dict
        elif type(test_obj) is dict:
            current_configuration = test_obj.get('configuration', {})
            current_environments = test_obj.get('environments', {})
            current_tests = test_obj.get('tests', [])

            # Merge the parent configuration with the current configuration
            merged_configuration = parent_configuration.copy()
            for key, val in current_configuration.items():
                merged_configuration[key] = val

            if current_environments:
                for current_environment in current_environments:
                    for current_test in current_tests:
                        # Merge the parent env with the current env
                        merged_environment = parent_environment.copy()
                        for key, val in current_environment.items():
                            merged_environment[key] = val

                        # Recur
                        flat_tests += AutoThreadedTestRunner._build_tests(
                            current_test,
                            parent_configuration=merged_configuration,
                            parent_environment=merged_environment
                        )
            else:
                for subtest in current_tests:
                    flat_tests += AutoThreadedTestRunner._build_tests(
                        subtest,
                        parent_configuration=merged_configuration,
                        parent_environment=parent_environment
                    )

        return flat_tests

class AutoThreadedWorkProvider(WorkProvider):
    """A thread-safe class designed to manage WorkNodes and provide them to 
    WorkerThreads to be executed."""
    _work_nodes = None
    _lock = None
    _failed_ex_groups = None 
    _cur_resources = None
    _environments = None


    def __init__(self):
        self._work_nodes = []
        self._lock = Lock()
        self._failed_ex_groups = {}
        self._cur_resources = set()
        self._environments = []

    def add_nodes(self, *work_nodes):
        """Takes a TestSet subclass object and a list of function objects in that 
        class and adds them as a node in the AutoThreadedWorkProvider's work. The class will be 
        instantiated and the functions called as tests."""
        self._lock.acquire()
        # Add the new work nodes
        self._work_nodes += work_nodes
        # Add any new environments to self.environments
        for work_node in self._work_nodes:
            if work_node.test_env not in self._environments:
                self._environments.append(work_node.test_env)
        self._lock.release()

    def get_next_node(self):
        """Finds and returns the next available node of work and returns it. This 
        method does not lock any resources for that node, that must be done by 
        lock_resources()."""
        self._lock.acquire()
        if len(self._work_nodes):
            node = self._work_nodes.pop(0)
        else:
            node = None
        self._lock.release()
        return node

    def lock_resources(self, resources):
        """Attempts to lock the given resources. If successful, a lock is made and 
        True is returned. False is returned otherwise. Make sure to always 
        release_resources() after locking them."""
        self._lock.acquire()
        if AutoThreadedWorkProvider.resources_are_free(resources, self._cur_resources):
            self._cur_resources = self._cur_resources.union(resources)
            self._lock.release()
            return True
        else:
            self._lock.release()
            return False

    def release_resources(self, resources):
        """Releases the lock on the given resources."""
        self._lock.acquire()
        self._cur_resources = self._cur_resources.difference(resources)
        self._lock.release()

    def has_work(self):
        """Returns True if this WorkProvider still has unclaimed work, and False 
        otherwise."""
        self._lock.acquire()
        has_work = self._work_nodes
        self._lock.release()
        return has_work

    def add_failed_ex_groups(self, failed_ex_groups, environment):
        """Takes a list of Execution Groups and adds them to this WorkProvider's list
        of failed Execution Groups. Should be called if any of this WorkProvider's tests 
        with execution groups fail."""
        self._lock.acquire()
        idx = self._environments.index(environment)
        self._failed_ex_groups[idx] = self._failed_ex_groups.get(idx, set()).union(failed_ex_groups)
        self._lock.release()

    def has_failed_ex_groups(self, environment, *execution_groups):
        """Takes a variable number of execution groups and returns True if any of 
        them have failed and False otherwise."""
        idx = self._environments.index(environment)
        self._lock.acquire()
        for ex_group in execution_groups:
            if ex_group in self._failed_ex_groups.get(idx, set()):
                self._lock.release()
                return True

        self._lock.release()
        return False


    @staticmethod
    def resources_are_free(required_resources, used_resources):
        """Takes a list of required resources and returns True if none of them are 
        in the list of used_resources, and False otherwise."""
        for required_resource in required_resources:
            if required_resource in used_resources:
                return False
        return True

class AutoThreadedWorkerThread(WorkerThread):
    def run_tests_for_node(self, node):
        """Takes a WorkNode and runs the tests it contains. If some of the node's 
        resources are in use, the node may be returned to the work_provider."""
        # Try to get a lock on the class resources
        resources_locked = self.work_provider.lock_resources(node.class_resources)
        if not resources_locked:
            self.work_provider.add_nodes(node)
            return

        cls = node.test_class
        instance = node.get_test_class_instance()

        # if this node contains only one function, check for failed execution groups
        # and don't instatiate the class or call setup
        if len(node.test_funcs) == 1:
            func = node.test_funcs[0]
            if WorkerThread.has_failed_ex_groups(cls, func, node.test_env, self.work_provider):
                self.logger.skippingTestFunction(instance, func, thread_num=self.thread_num)
                self.work_provider.release_resources(node.class_resources)
                return

        # Try to call the class's setup method
        if not node.test_class_is_setup:
            if hasattr(cls, 'setup') and callable(cls.setup):
                success = self.acquire_resources_and_run(node, cls.setup, TestFunctionType.SETUP)
                if not success:
                    return

        # Run all the test functions
        for func in list(node.test_funcs): # copy the list so we don't remove items while iterating
            success = self.acquire_resources_and_run(node, func)
            if not success:
                return


        # Try to call the class's teardown method
        if not node.test_class_is_torndown:
            if hasattr(cls, 'teardown') and callable(cls.teardown):
                success = self.acquire_resources_and_run(node, cls.teardown, TestFunctionType.TEARDOWN)
                if not success:
                    return

        self.work_provider.release_resources(node.class_resources)

    def acquire_resources_and_run(self, node, func, func_type=TestFunctionType.TEST):
        """
        Tries to acquire resources for a function and run it, reporting
        appropriately to the TestLogger. Takes care of returning nodes to the work
        provider if resources cannot be locked.

        :param node: The WorkNode containing the function you wish to run.
        :param func: The function you wish to execute
        :param func_type: The TestFunctionType of the function
        :return: True if the function was successfully run, False otherwise
        """
        instance = node.get_test_class_instance()

        # Check for failed execution groups
        if WorkerThread.has_failed_ex_groups(node.test_class, func, node.test_env, self.work_provider):
            self.logger.skippingTestFunction(instance, func, func_type, thread_num=self.thread_num)
            return True

        # Try to lock this function's resources
        func_resources = getattr(func, 'resources', [])
        func_resources_locked = self.work_provider.lock_resources(func_resources)
        if not func_resources_locked:
            self.work_provider.release_resources(node.class_resources)
            self.work_provider.add_nodes(node)
            return False

        # Execute the function
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

        # Cleanup
        if func_type == TestFunctionType.SETUP:
            node.test_class_is_setup = True
        elif func_type == TestFunctionType.TEARDOWN:
            node.test_class_is_torndown = True
        else:
            node.test_funcs.remove(func)
        self.logger.finishedTestFunction(instance, func, func_type, thread_num=self.thread_num)
        self.work_provider.release_resources(func_resources)
        return True


