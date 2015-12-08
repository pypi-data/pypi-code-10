#!/usr/bin/env python

from .constants import DEFAULT_PRIORITY


class Job(object):
    def __init__(self, conn, jid, body, reserved=True):
        self.conn = conn
        self.jid = jid
        self.body = body
        self.reserved = reserved

    def _priority(self):
        stats = self.stats()
        if isinstance(stats, dict):
            return stats['pri']
        return DEFAULT_PRIORITY

    # -- public interface --

    def delete(self):
        """Delete this job."""

        self.conn.delete(self.jid)
        self.reserved = False

    def release(self, priority=None, delay=0):
        """Release this job back into the ready queue."""

        if self.reserved:
            self.conn.release(self.jid, priority or self._priority(), delay)
            self.reserved = False

    def bury(self, priority=None):
        """Bury this job."""

        if self.reserved:
            self.conn.bury(self.jid, priority or self._priority())
            self.reserved = False

    def kick(self):
        """Kick this job alive."""

        self.conn.kick_job(self.jid)

    def touch(self):
        """Touch this reserved job, requesting more time to work on it before it expires."""

        if self.reserved:
            self.conn.touch(self.jid)

    def stats(self):
        """Return a dict of stats about this job."""

        return self.conn.stats_job(self.jid)
