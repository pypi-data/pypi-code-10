from __future__ import absolute_import
import os
import sys


def get_last_cmd_executed():
    cmd_args = [a if u' ' not in a else u"'" + a + u"'" for a in sys.argv[1:]]
    return u' '.join([os.path.basename(sys.argv[0])] + cmd_args)


def add_execution_args(parser):
    parser.add_argument(u'-n', u'--name', help=u"A name for this execution", required=True)
    # parser.add_argument('-o', '--output_dir', type=str, help="The directory to output files to.  Path should not exist if this is a new execution.")
    parser.add_argument(u'-c', u'--max_cpus', type=int,
                        help=u"Maximum number (based on the sum of cpu_requirement) of cores to use at once.  0 means unlimited", default=None)
    parser.add_argument(u'-a', u'--max_attempts', type=int,
                        help=u"Maximum number of times to try running a Task that must succeed before the execution fails", default=1)
    parser.add_argument(u'-r', u'--restart', action=u'store_true',
                        help=u"Completely restart the execution.  Note this will delete all record of the execution in the database")
    parser.add_argument(u'-y', u'--skip_confirm', action=u'store_true',
                        help=u"Do not use confirmation prompts before restarting or deleting, and assume answer is always yes")


def pop_execution_args(kwargs):
    args = [u'name', u'max_cpus', u'max_attempts', u'restart', u'skip_confirm']
    return dict((k, kwargs[k]) for k in args), dict((k, kwargs[k]) for k in kwargs if k not in args)
