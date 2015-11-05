from __future__ import division, absolute_import, with_statement
# Copyright (c) 2015 University of Louisiana at Lafayette.
# All rights reserved.

import sys
import time
import logging

from progressbar import ProgressBar, ETA, AdaptiveETA, Percentage, SimpleProgress, Timer


class EtaTimer(object):
    """ Keep track of how much processing time is left.
    Initialize object with the number of items that need to be processed.  After
    every individual item is processed, call t.tick().  This function will keep
    an internal counter of items left and every inc ticks report estimated time
    left.

    When the internal counter reaches zero, ding() is automatically
    called and final statistics are reported. The timer can manually be stopped
    by a call to ding() as well.
    """
    def __init__(self, total, name="", stream=sys.stderr, poll_period=1, eta_window=0):
        """
        Args:
            total (int): Total number of items that will need processing.
            stream (File like): File descriptor to write to
            poll_period (int): Minimum number of seconds between updates.
            eta_window (int): Number of elements to use in the sliding window that determines ETA.
                Set to 0 to use naive time estimation (default).
        """
        self.name = name
        self.eta_window = eta_window
        self.total = total
        self.poll_period = poll_period
        self.pbar = ProgressBar(max_value=total, widgets=self._default_widgets(), fd=stream)
        self.currval = 0
        # Ensure starts at 0
        self.pbar.update(self.currval)
        self.next_update = time.time() + self.poll_period

    @classmethod
    def from_file(cls, infile):
        """ Create an EtaTimer from a file object.
        If any error during timer creation, will simply return a DummyTimer.
        Args:
            infile (File): Must be seekable
        """
        timer = DummyTimer()
        try:
            infile.seek(0, 0)
        except Exception:
            log = logging.getLogger(__name__)
            log.error("Unseekable File, not using timer")
        else:
            total = sum(1 for _ in infile)
            infile.seek(0, 0)
            timer = EtaTimer(total, sys.stderr)
        return timer

    @property
    def finished(self):
        return self.pbar.finished

    @property
    def max_value(self):
        return self.pbar.max_value

    def tick(self, *args):
        """ Finished an item.
        The *args is so this can be used as an arbitrary callback
        """
        log = logging.getLogger(__name__)
        try:
            self.currval += 1
            if time.time() >= self.next_update:
                self.pbar.update(self.currval)
                self.next_update = time.time() + self.poll_period
        except ValueError:
            # Update value was too large. I don't ever want to generate an
            # error, so simply ignore it.
            log.debug("ProgressBar update called with value larger than max of %d", self.max_value)
            self.pbar.update(self.currval)

    def ding(self):
        """ Time's up. Ding! """
        self.pbar.finish()

    # progressbar2 adapted code
    def _default_widgets(self):
        if self.eta_window == 0:
            eta = ETA()
        else:
            eta = AdaptiveETA(num_samples=self.eta_window)
        return [
            Percentage(), ' (', SimpleProgress(), ') ',
            Timer(), ' ', eta,
        ]


class DummyTimer(object):
    """ A mock of timer that does nothing.
    Exists as a default argument anytime timer is user.
    Allows for easy code.  Set this as the default argument,
    then simply pretend like you always have a timer.
    """
    finished = True

    def tick(self):
        pass

    def ding(self):
        pass

    def done(self):
        return True
