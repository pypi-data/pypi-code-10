#!/usr/bin/python
from egat.loggers.simple_text_logger import SimpleTextLogger
from egat.loggers.html_logger import HTMLLogger
from egat.auto_threaded_test_runner import AutoThreadedTestRunner
from egat.user_threaded_test_runner import UserThreadedTestRunner
from egat.parse import ArgumentParser
import sys

def run():
    """The command-line interface for the TestRunner class."""
    # Parse arguments
    parser = ArgumentParser()
    args = parser.parse_args()
    test_json = {
        "tests": args.tests,
        "configuration": getattr(args, 'configuration', {}),
        "environments": getattr(args, 'environments', []),
    }
    log_level = args.log_level

    # Set up the TestRunner and TestLogger
    if args.log:
        logger = HTMLLogger(log_dir=args.log, css_path=args.css_path)
    else:
        logger = SimpleTextLogger()
    logger.set_log_level(log_level)

    if args.user_defined_threads:
        runner = UserThreadedTestRunner(logger)
    else:
        runner = AutoThreadedTestRunner(
            logger, 
            args.number_of_threads, 
        )

    runner.add_tests(test_json) 

    # Run the tests
    exit_code = runner.run_tests()

    sys.exit(exit_code)
