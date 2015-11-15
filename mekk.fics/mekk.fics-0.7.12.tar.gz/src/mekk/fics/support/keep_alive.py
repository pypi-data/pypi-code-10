# -*- coding: utf-8 -*-

"""
Periodical calling of unnecessary command to avoid timeouts.
"""

import logging
import time
from twisted.internet import defer, task, reactor
import six

logger = logging.getLogger("fics.lib")

###########################################################################

# TODO: if we use activate_timeout_checker on block deferreds,
# checking the commands here for timeout looks like
# duplicating the effort. Still, as keepalive command
# is simple, shorter timeout may be used than used there.

class KeepAliveExecutor(object):
    """
    Calling some „keepalive” command (for example - „date”) at regular
    intervals to ensure connection is not dropped due to inactivity.
    Also - monitors whether the reply is obtained in reasonable time,
    if not, reports the problem.

    To be used in context of Twisted reactor.

    Example usage::

    keep_alive = KeepAliveExecutor(
        command = lambda: protocol.run_command("date"),
        on_failure = protocol.on_keepalive_failure,
        label = "Worker 3",
        frequency = 10 * 60,
        timeout = 2 * 60)

    (and it will just work until the object is deleted, or .stop() is called)
    """

    ############################################################
    # Standardowe API użytkowe
    ############################################################

    def __init__(self, label, frequency, timeout,
                 command, on_failure, on_critical_failure = None, on_success = None,
                 start_immediately = False):
        """
        Initializes and starts the keepalive monitoring.

        :param label: text label for logging (like worker/connection name)
        :param frequency: how often is keepalive executed - in seconds, fractions like 0.5 can be used
            (in FICS connection context sensible values
            are from a 120-180 (2-3 minutes) - when fast detection of connection freeze is necessery - to
            1800-2400 (30-45 minutes) - when our only concern is to avoid disconnection due to inactivity
        :param timeout: max time (in seconds, floats acceptable) we wait for keepalive reply. Can be 0 or None,
             then we check whether the reply appeared before issuing the next keepalive
        :param command: callable called to execute keepalive command. Gets no parameters,
            should return Deferred called when command gets reply (or erred when it fails)
        :param on_failure: callable called in case keepalive command fails. Gets no parameters.
        :param on_critical_failure: callable called in case some gross error happens. In such case the
            object is no longer guaranteed to work sensibly and the process is likely in bad shape.
            By default executes reactor.stop() to finish the process.
        :param on_success: callable called in case of successful keepalive. Can be (and is by default) None,
            then nothing is called.
        :param start_immediately: should we make first call straight away (True),
            or after frequency passes (False, default)
        """
        def default_on_critical_failure():
            if reactor.running:
                reactor.stop()

        self._command = command
        self._on_failure = on_failure
        self._on_success = on_success
        if on_critical_failure:
            self._on_critical_failure = on_critical_failure
        else:
            self._on_critical_failure = default_on_critical_failure
        self._label = label
        self._frequency = frequency
        if (timeout > 0) and (timeout < 0.8 * frequency):
            self._timeout = timeout
        else:
            self._timeout = 0

        # call no. Used to identify calls
        self._call_no = 0
        # pending (not yet finished) calls. Map deferred → the time it was issued
        self._pending = dict()
        # Twisted object responsible for waking us up at appropriate moments.
        self._task = task.LoopingCall(self._wakeup)

        # Call statistics
        self._ok_count = 0
        self._fail_count = 0  # failed + timed out

        logger.info("%s: Activating keepalive tracking, frequency %d, timeout %d" % (self._label, frequency, self._timeout))
        self._task.start(frequency, now=start_immediately)

    def __del__(self):
        self.stop()

    def stop(self):
        """
        Stops the object, immediately cancels any monitoring efforts (also done automatically in the destructor).
        """
        if self._task:
            logger.info("%s: Stopping keepalive counter after %d calls. Successes: %d, failures/timeouts: %d" % (
                self._label, self._call_no, self._ok_count, self._fail_count))
            self._task.stop()
            self._task = None
            #self._pending = dict()
            #self._ok_count = 0
            #self._fail_count = 0
            #self._call_no = 0

    ############################################################
    # Internal methods
    ############################################################

    def _wakeup(self):
        """
        Keepalive wakeup. Calls test command, registers callbacks
        to store the result and to verify result arrival.
        """
        try:
            # If we use no separate timeout, we check for prev results here
            if not self._timeout:
                self._verify_result_arrival()
            # Maybe we are already stopped?
            if not self._task:
                return

            self._call_no += 1
            logger.info("%s: Executing keepalive call no %d" % (self._label, self._call_no))
            now = time.time()
            dfr = self._command()
            assert( isinstance(dfr, defer.Deferred) )
            self._pending[self._call_no] = now

            def _callback(dt, call_no):
                if call_no in self._pending:
                    del self._pending[call_no]
                    self._ok_count += 1
                    logger.info("%s: Keepalive call %d succeded, output %s" % (self._label, call_no, dt))
                    if self._on_success:
                        self._on_success()
                else:
                    logger.info("%s: Keepalive call %d succeded but arrived too late, output %s" % (self._label, call_no, dt))
            def _errback(failure, call_no):
                if call_no in self._pending:
                    del self._pending[call_no]
                else:
                    logger.info("%s: Keepalive call %d failed and arrived too late" % (self._label, call_no))
                logger.error(failure)
                self._on_failure()
            dfr.addCallback(_callback, self._call_no)
            dfr.addErrback(_errback, self._call_no)

            if self._timeout:
                reactor.callLater(self._timeout, self._verify_result_arrival)
        
        except Exception as e:
            #logger.error("%s: Exception during keepalive wakeup: %s" % (self._label, str(e)))
            logger.exception("%s: Exception during keepalive wakeup: %s" % (self._label, str(e)))
            self._on_critical_failure()

        return None

    def _verify_result_arrival(self):
        """
        Called 'timeout' after keepalive call, checks whether issued command finished on time and reports
        problem in case it did not.
        """
        now = time.time()
        if self._timeout:
            time_limit = now - self._timeout
        else:
            time_limit = now - self._frequency

        # In case of heavy load there is some likelihood this callback is delayed and we see „new”,
        # not yet timeouted one request. Therefore we check whether the time really passed.
        lagging_items = [ (call_no, issued)
                            for call_no, issued in six.iteritems(self._pending)
                            if issued <= time_limit ]
        for call_no, _ in lagging_items:
            del self._pending[call_no]
        if lagging_items:
            self._fail_count += len(lagging_items)
            if len(lagging_items) == 1:
                issued = lagging_items[0][1]
                logger.fatal(
                    "%s: No reply to previous keepalive command issued at %s (%s sec. ago). Frozen connection?" % (
                        self._label, time.ctime(issued), str(now-issued)))
            else:
                logger.fatal(
                    "%s: No reply to %d previous keepalive commands issued at %s. Frozen connection?" % (
                        self._label,
                        len(lagging_items),
                        ", ".join(str(issued) for _, issued in lagging_items)
                        ))
            # Just one callback, no need to notify many times if we happen to see many delayed calls
            self._on_failure()
