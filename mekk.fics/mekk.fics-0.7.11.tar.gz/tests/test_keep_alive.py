# -*- coding: utf-8 -*-

from twisted.trial import unittest
from twisted.internet import task, reactor, defer
from mekk.fics.support import keep_alive
import logging, time

logger = logging.getLogger("test")

class KeepAliveExecutorTestCase(unittest.TestCase):

    # Time after which methods below fake reply arrival
    #TIME_TO_REPLY = 0.05
    TIME_TO_REPLY = 0.01

    def setUp(self):
        self._successful = 0
        self._failed = 0
        self._critical = 0
    def _run_command(self):
        d = defer.Deferred()
        #noinspection PyUnresolvedReferences
        reactor.callLater(self.TIME_TO_REPLY, d.callback, "some output at %s" % time.time())
        return d
    def _run_failing_command(self):
        d = defer.Deferred()
        reactor.callLater(self.TIME_TO_REPLY, d.errback, Exception("some failure at %s" % time.time()))
        return d
    def _on_success(self):
        self._successful += 1
    def _on_failure(self):
        self._failed += 1
    def _on_critical(self):
        self._critical += 1

    @defer.inlineCallbacks
    def test_with_separate_timeout_ok(self):
        FREQUENCY = 4 * self.TIME_TO_REPLY
        TIMEOUT = 2 * self.TIME_TO_REPLY
        kpl_exec = keep_alive.KeepAliveExecutor(
            command = self._run_command,
            on_failure = self._on_failure,
            on_success = self._on_success,
            label = "UTST",
            frequency = FREQUENCY,
            timeout = TIMEOUT,
        )
        #logger.info("Before: %s", time.time())
        yield task.deferLater(reactor, 5.5*FREQUENCY, lambda: 0)
        #logger.info("After: %s", time.time())
        kpl_exec.stop()
        self.failUnlessEqual(self._failed, 0)
        self.failUnlessEqual(self._successful, 5)

    @defer.inlineCallbacks
    def test_with_separate_timeout_timeout(self):
        FREQUENCY = 4 * self.TIME_TO_REPLY
        TIMEOUT = self.TIME_TO_REPLY / 3
        kpl_exec = keep_alive.KeepAliveExecutor(
            command = self._run_command,
            on_failure = self._on_failure,
            on_success = self._on_success,
            label = "UTST",
            frequency = FREQUENCY,
            timeout = TIMEOUT,
        )
        #logger.info("Before: %s", time.time())
        yield task.deferLater(reactor, 5.5*FREQUENCY, lambda: 0)
        #logger.info("After: %s", time.time())
        kpl_exec.stop()
        self.failUnlessEqual(self._failed, 5)
        self.failUnlessEqual(self._successful, 0)

    @defer.inlineCallbacks
    def test_with_separate_timeout_failing_command(self):
        FREQUENCY = 4 * self.TIME_TO_REPLY
        TIMEOUT = 2 * self.TIME_TO_REPLY
        kpl_exec = keep_alive.KeepAliveExecutor(
            command = self._run_failing_command,
            on_failure = self._on_failure,
            on_success = self._on_success,
            label = "UTST",
            frequency = FREQUENCY,
            timeout = TIMEOUT,
        )
        yield task.deferLater(reactor, 5.5*FREQUENCY, lambda: 0)
        kpl_exec.stop()
        self.failUnlessEqual(self._failed, 5)
        self.failUnlessEqual(self._successful, 0)


    def test_without_optional_params_ok(self):
        FREQUENCY = 4 * self.TIME_TO_REPLY
        # no timeout, no on_success
        kpl_exec = keep_alive.KeepAliveExecutor(
            command = self._run_command,
            on_failure = self._on_failure,
            label = "UTST",
            frequency = FREQUENCY,
            timeout = None,
        )
        yield task.deferLater(reactor, 5.5 * FREQUENCY, lambda: 0)
        kpl_exec.stop()
        self.failUnlessEqual(self._failed, 0)
    def test_without_optional_params_failing_command(self):
        FREQUENCY = 4 * self.TIME_TO_REPLY
        # no timeout, no on_success
        kpl_exec = keep_alive.KeepAliveExecutor(
            command = self._run_failing_command,
            on_failure = self._on_failure,
            label = "UTST",
            frequency = FREQUENCY,
            timeout = None,
        )
        yield task.deferLater(reactor, 5.5 * FREQUENCY, lambda: 0)
        kpl_exec.stop()
        self.failUnlessEqual(self._failed, 5)
    def test_without_optional_params_timeout(self):
        FREQUENCY = self.TIME_TO_REPLY / 3
        # no timeout, no on_success
        kpl_exec = keep_alive.KeepAliveExecutor(
            command = self._run_command,
            on_failure = self._on_failure,
            label = "UTST",
            frequency = FREQUENCY,
            timeout = 0,
        )
        yield task.deferLater(reactor, 55*FREQUENCY, lambda: 0)
        kpl_exec.stop()
        self.failUnlessEqual(self._failed, 55)
    def test_critical_failure(self):
        FREQUENCY = 2 * self.TIME_TO_REPLY
        def crash():
            raise Exception("Crashing exception inside failure handler")
        kpl_exec = keep_alive.KeepAliveExecutor(
            command = self._run_failing_command,
            on_failure = crash,
            on_critical_failure = self._on_critical,
            label = "UTST",
            frequency = FREQUENCY,
            timeout = FREQUENCY / 10,
        )
        yield task.deferLater(reactor, 5.5*FREQUENCY, lambda: 0)
        kpl_exec.stop()
        self.failUnlessEqual(self._critical, 5)
        self.failUnlessEqual(self._failed, 5)


