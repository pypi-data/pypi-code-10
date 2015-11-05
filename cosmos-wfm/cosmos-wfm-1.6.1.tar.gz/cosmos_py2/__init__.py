from __future__ import with_statement
from __future__ import absolute_import
import os
import math

# turn SQLAlchemy warnings into errors
import warnings
from sqlalchemy.exc import SAWarning
from io import open
warnings.simplefilter(u"error", SAWarning)

opj = os.path.join

ACCEPTABLE_TAG_TYPES = (unicode, int, float, bool)

#########################################################################################################################
# Settings
#########################################################################################################################

library_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(library_path, u'VERSION'), u'r') as fh:
    __version__ = fh.read().strip()


#########################################################################################################################
# Misc
#########################################################################################################################

class ExecutionFailed(Exception): pass

#########################################################################################################################
# Signals
#########################################################################################################################
import blinker

signal_task_status_change = blinker.Signal()
signal_stage_status_change = blinker.Signal()
signal_execution_status_change = blinker.Signal()


########################################################################################################################
# Enums
########################################################################################################################
import enum


class MyEnum(enum.Enum):
    def __str__(self):
        return u"%s" % self._value_


NOOP = None


class TaskStatus(MyEnum):
    no_attempt = u'Has not been attempted',
    waiting = u'Waiting to execute',  # deprecated
    submitted = u'Submitted to the job manager',
    successful = u'Finished successfully',
    failed = u'Finished, but failed'
    killed = u'Manually killed'


class StageStatus(MyEnum):
    no_attempt = u'Has not been attempted',
    running = u'Running',
    running_but_failed = u'Running, but a task failed'
    successful = u'Finished successfully',
    failed = u'Finished, but failed'
    killed = u'Manually killed'


class ExecutionStatus(MyEnum):
    no_attempt = u'No Attempt yet',
    running = u'Running',
    successful = u'Successfully Finished',
    killed = u'Killed'
    failed_but_running = u"Running, but a task failed"
    failed = u'Failed, but finished'


class RelationshipType(MyEnum):
    one2one = u'one2one',
    one2many = u'one2many',
    many2one = u'many2one',
    many2many = u'many2many'
