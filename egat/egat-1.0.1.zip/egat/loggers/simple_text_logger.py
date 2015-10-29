import sys
import datetime
import os
from egat.loggers.test_logger import TestLogger
from egat.loggers.test_logger import LogLevel
from egat.test_runner_helpers import TestFunctionType
from Queue import Queue
from Queue import Empty
from threading import Thread
from multiprocessing import Lock

class _Printer(Thread):
    """A class used by the SimpleTextLogger to print test output. The _Printer reads
    from a synchronized queue so that output from tests running in multiple threads
    does not overlap."""
    tests_running = False

    def __init__(self, output_queue, out):
        super(_Printer, self).__init__()
        self.output_queue = output_queue
        self.out = out
        self.tests_running = True

    def run(self):
        while True:
            try:
                (func_str, msg, traceback) = self.output_queue.get_nowait()
                if traceback:
                    self.out.write("%s %s\n%s" % (func_str, msg, traceback))
                else:
                    self.out.write("%s %s\n" % (func_str, msg))
            except Empty:
                if not self.tests_running:
                    break

class SimpleTextLogger(TestLogger):
    """A very simple logger that writes the test method names and tracebacks in 
    plain text."""
    failure_msg = "Failure"
    success_msg = "Success"
    skipped_msg = "Skipped"
    output_queue = None
    current_tests = None
    failed_test_count = None
    lock = None

    def startingTests(self):
        if self.log_dir:
            # Set up the log file
            start_time = datetime.datetime.now().strftime("%m-%d-%y %H.%M.%S")
            self.log_dir = self.log_dir.rstrip(os.sep)
            self.log_dir += "%sTest Run %s" % (os.sep, start_time)
            os.mkdir(self.log_dir)
            log_name = "%s%slog.txt" % (self.log_dir, os.sep)
            self.out = open(log_name, 'w')
        else:
            self.out = sys.stdout

        self.failed_test_count = 0
        self.current_tests = {}
        self.lock = Lock()

        # Set up the printer
        self.output_queue = Queue()
        self.printer = _Printer(self.output_queue, self.out)
        self.printer.start()
    
    def finishedTests(self):
        self.printer.tests_running = False
        self.printer.join()
        return self.failed_test_count

    def runningTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        current_test = {
            'func_failed': False,
            'exception': None,
            'traceback': None,
        }
        with self.lock:
            self.current_tests[(class_instance, func, thread_num)] = current_test

    def finishedTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        with self.lock:
            current_test = self.current_tests.pop((class_instance, func, thread_num))

        # Only print output if this was a test function, or if the function failed
        if func_type == TestFunctionType.TEST or current_test['func_failed']:
            func_str = TestLogger.format_function_name(class_instance, func)
            if current_test['func_failed']:
                msg = self.failure_msg
            else:
                msg = self.success_msg

            self.output_queue.put(
                (func_str, msg, current_test['traceback'])
            )

        if self.log_level >= LogLevel.DEBUG:
            self.log_debug_info(class_instance, func)

    def skippingTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        func_str = TestLogger.format_function_name(class_instance, func)
        # Only print output if this was a test function
        if func_type == TestFunctionType.TEST:
            self.output_queue.put((func_str, self.skipped_msg, None))

    def foundException(self, class_instance, func, e, tb, func_type=TestFunctionType.TEST, thread_num=None):
        with self.lock:
            self.failed_test_count += 1
            current_test = self.current_tests[(class_instance, func, thread_num)]

        current_test['func_failed'] = True
        current_test['exception'] = e
        current_test['traceback'] = tb
        if self.log_level >= LogLevel.INFO:
            self.log_debug_info(class_instance, func)




