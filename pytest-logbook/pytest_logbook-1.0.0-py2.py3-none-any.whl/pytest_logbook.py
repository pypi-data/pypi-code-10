"""Capture logbook log messages during tests.

There are three logbook.TestHandlers used by this plugin: one for test
setup, one for test execution and one for test teardown.  Initially
the setup instance gets installed during the session start to catch
log messages emitted during early setup, session fixtures etc.
"""

import logging

import logbook
import pytest


@pytest.hookimpl
def pytest_addoption(parser):
    parser.addini(
        name='logbook_stdlib',
        help='redirect stdlib logging to logbook [true]',
        default='true',
    )


@pytest.hookimpl
def pytest_configure(config):
    config.pluginmanager.register(LogbookPlugin(), 'logbook')


class LogbookPlugin:

    def __init__(self):
        self.handler_setup = logbook.TestHandler()
        self.handler_call = logbook.TestHandler()
        self.handler_teardown = logbook.TestHandler()
        self.config = None
        self.orig_logging_handlers = None

    @pytest.hookimpl
    def pytest_configure(self, config):
        self.config = config

    def getcfg(self, name):
        if name == 'logbook_stdlib':
            raw_val = self.config.getini(name)
            return raw_val == 'true'
        else:
            raise KeyError('Unknown config name')

    @pytest.hookimpl
    def pytest_sessionstart(self):
        self.handler_setup.push_application()
        if self.getcfg('logbook_stdlib'):
            self.orig_logging_handlers = logging.root.handlers[:]
            del logging.root.handlers[:]
            redir_handler = logbook.compat.RedirectLoggingHandler()
            logging.root.addHandler(redir_handler)
            logging.root.setLevel(logging.NOTSET)

    @pytest.hookimpl
    def pytest_sessionfinish(self):
        self.handler_setup.pop_application()
        if self.getcfg('logbook_stdlib'):
            logging.root.handlers[:] = self.orig_logging_handlers

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, call):
        outcome = yield
        report = outcome.get_result()

        prev_handler = getattr(self, 'handler_' + call.when)
        if call.when == 'setup':
            if call.excinfo:
                next_handler = self.handler_teardown
            else:
                next_handler = self.handler_call
        elif call.when == 'call':
            next_handler = self.handler_teardown
        elif call.when == 'teardown':
            next_handler = self.handler_setup

        prev_handler.pop_application()
        del next_handler.records[:]
        next_handler.push_application()

        records = getattr(prev_handler, 'formatted_records', None)
        if records:
            report.sections.append(
                ('Logbook {} records'.format(call.when),
                 '\n'.join(records)))

    @pytest.fixture
    def loghandler_setup(self):
        """Access to the registerd TestHandler instance for item setup.

        This returns the logbook.TestHandler instance in use during
        fixture setup.  It will contain the log records emitted during
        item setup only, e.g. from other fixtures.
        """
        return self.handler_setup

    @pytest.fixture
    def loghandler(self):
        """Access to the registered TestHandler instance during item call.

        This returns the logbook.TestHandler instance in use during the
        execution of the test itself.  It will contain log records emitted
        during the test execution but not any emitted during test setup or
        teardown.
        """
        return self.handler_call


    @pytest.fixture
    def loghandler_teardown(self):
        """Access to the registered TestHandler instance during item teardown.

        This returns the logbook.TestHandler instance in use during
        execution of the teardown executed for the test.  It will only
        contain log records emitted during this time.
        """
        return self.handler_teardown
