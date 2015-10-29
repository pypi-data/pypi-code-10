from egat.test_loader import TestLoader
from egat.test_runner_helpers import WorkProvider
from egat.test_runner_helpers import WorkerThread

class UserThreadedTestRunner():
    """ A class used to run TestSet tests."""
    work_providers = None
    logger = None

    def __init__(self, logger, selenium_debugging=True):
        """Initializes the TestRunner. The logger should be a subclass of
        TestLogger."""
        self.logger = logger
        self.work_providers = []

    def add_tests(self, test_json):
        """Takes a list of tests in the format required by the configuration file 
        and adds them to the tests that this TestRunner will run."""
        configuration = test_json['configuration']
        for thread in test_json['tests']:
            work_provider = WorkProvider() 
            work_nodes = []
            for test in thread:
                test_obj = {
                    'test': test,
                    'configuration': configuration,
                    'environment': {},
                }
                work_nodes.extend(TestLoader.get_work_nodes_for_test(test_obj))

            work_provider.add_nodes(*work_nodes)
            self.work_providers.append(work_provider)

    def run_tests(self):
        """Runs the tests that have been added to this TestRunner and reports the
        results to the given TestLogger."""
        self.logger.startingTests()
        workers = []

        for i in range(len(self.work_providers)):
            work_provider = self.work_providers[i]
            worker = WorkerThread(work_provider, self.logger, thread_num=i)
            worker.start()
            workers.append(worker)

        for worker in workers:
            worker.join()
        return self.logger.finishedTests()
