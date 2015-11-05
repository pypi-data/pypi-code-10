from __future__ import absolute_import
import subprocess as sp
import re
import os

from .DRM_Base import DRM
from itertools import ifilter
from itertools import izip

decode_lsf_state = dict([
    (u'UNKWN', u'process status cannot be determined'),
    (u'PEND', u'job is queued and active'),
    (u'PSUSP', u'job suspended while pending'),
    (u'RUN', u'job is running'),
    (u'SSUSP', u'job is system suspended'),
    (u'USUSP', u'job is user suspended'),
    (u'DONE', u'job finished normally'),
    (u'EXIT', u'job finished, but failed'),
])


class DRM_LSF(DRM):
    name = u'lsf'

    def submit_job(self, task):
        ns = u' ' + task.drm_native_specification if task.drm_native_specification else u''
        bsub = u'bsub -o {stdout} -e {stderr}{ns} '.format(stdout=task.output_stdout_path,
                                                          stderr=task.output_stderr_path,
                                                          ns=ns)

        out = sp.check_output(u'{bsub} "{cmd_str}"'.format(cmd_str=self.jobmanager.get_command_str(task), bsub=bsub),
                              env=os.environ,
                              preexec_fn=preexec_function(),
                              shell=True)

        drm_jobID = int(re.search(u'Job <(\d+)>', out).group(1))
        return drm_jobID

    def filter_is_done(self, tasks):
        if len(tasks):
            bjobs = bjobs_all()

            def is_done(task):
                jid = unicode(task.drm_jobID)
                if jid not in bjobs:
                    # prob in history
                    # print 'missing %s %s' % (task, task.drm_jobID)
                    return True
                else:
                    return bjobs[jid][u'STAT'] in [u'DONE', u'EXIT', u'UNKWN', u'ZOMBI']

            return list(ifilter(is_done, tasks))
        else:
            return []

    def drm_statuses(self, tasks):
        u"""
        :param tasks: tasks that have been submitted to the job manager
        :returns: (dict) task.drm_jobID -> drm_status
        """
        if len(tasks):
            bjobs = bjobs_all()

            def f(task):
                return bjobs.get(unicode(task.drm_jobID), dict()).get(u'STAT', u'???')

            return dict((task.drm_jobID, f(task)) for task in tasks)
        else:
            return {}

    def kill(self, task):
        u"Terminates a task"
        raise NotImplementedError
        # os.system('bkill {0}'.format(task.drm_jobID))

    def kill_tasks(self, tasks):
        for t in tasks:
            sp.check_call([u'bkill', unicode(t.drm_jobID)])


def bjobs_all():
    u"""
    returns a dict keyed by lsf job ids, who's values are a dict of bjob
    information about the job
    """
    try:
        lines = sp.check_output([u'bjobs', u'-a']).split(u'\n')
    except (sp.CalledProcessError, OSError):
        return {}
    bjobs = {}
    header = re.split(u"\s\s+", lines[0])
    for l in lines[1:]:
        items = re.split(u"\s\s+", l)
        bjobs[items[0]] = dict(list(izip(header, items)))
    return bjobs


def preexec_function():
    # Ignore the SIGINT signal by setting the handler to the standard
    # signal handler SIG_IGN.  This allows Cosmos to cleanly
    # terminate jobs when there is a ctrl+c event
    os.setpgrp()
