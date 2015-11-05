from __future__ import with_statement
from __future__ import absolute_import
import subprocess as sp
import re
import os
from collections import OrderedDict
import time
from .util import div, convert_size_to_kb

from more_itertools import grouper
from .DRM_Base import DRM
from io import open
from itertools import izip


class DRM_GE(DRM):
    name = u'ge'

    def submit_job(self, task):
        for p in [task.output_stdout_path, task.output_stderr_path]:
            if os.path.exists(p):
                os.unlink(p)

        ns = u' ' + task.drm_native_specification if task.drm_native_specification else u''
        qsub = u'qsub -o {stdout} -e {stderr} -b y -cwd -S /bin/bash -V{ns} '.format(stdout=task.output_stdout_path,
                                                                                    stderr=task.output_stderr_path,
                                                                                    ns=ns)

        out = sp.check_output(u'{qsub} "{cmd_str}"'.format(cmd_str=task.output_command_script_path, qsub=qsub),
                              env=os.environ,
                              preexec_fn=preexec_function,
                              shell=True)

        drm_jobID = int(re.search(u'job (\d+) ', out).group(1))
        return drm_jobID

    def filter_is_done(self, tasks):
        if len(tasks):
            qjobs = qstat_all()
        for task in tasks:
            jid = unicode(task.drm_jobID)
            if jid not in qjobs:
                # print 'missing %s %s' % (task, task.drm_jobID)
                yield task, self._get_task_return_data(task)
            else:
                if any(finished_state in qjobs[jid][u'state'] for finished_state in [u'e', u'E']):
                    yield task, self._get_task_return_data(task)

    def drm_statuses(self, tasks):
        u"""
        :param tasks: tasks that have been submitted to the job manager
        :returns: (dict) task.drm_jobID -> drm_status
        """
        if len(tasks):
            qjobs = qstat_all()

            def f(task):
                return qjobs.get(unicode(task.drm_jobID), dict()).get(u'state', u'???')

            return dict((task.drm_jobID, f(task)) for task in tasks)
        else:
            return {}

    def _get_task_return_data(self, task):
        d = qacct(task)
        failed = d[u'failed'][0] != u'0'
        return dict(
            exit_status=int(d[u'exit_status']) if not failed else int(re.search(u'^(\d+)', d[u'failed']).group(1)),

            percent_cpu=div(float(d[u'cpu']), float(d[u'ru_wallclock'])),
            wall_time=float(d[u'ru_wallclock']),

            cpu_time=float(d[u'cpu']),
            user_time=float(d[u'ru_utime']),
            system_time=float(d[u'ru_stime']),

            avg_rss_mem=d[u'ru_ixrss'],
            max_rss_mem_kb=convert_size_to_kb(d[u'ru_maxrss']),
            avg_vms_mem_kb=None,
            max_vms_mem_kb=convert_size_to_kb(d[u'maxvmem']),

            io_read_count=int(d[u'ru_inblock']),
            io_write_count=int(d[u'ru_oublock']),
            io_wait=float(d[u'iow']),
            io_read_kb=float(d[u'io']),
            io_write_kb=float(d[u'io']),

            ctx_switch_voluntary=int(d[u'ru_nvcsw']),
            ctx_switch_involuntary=int(d[u'ru_nivcsw']),

            avg_num_threads=None,
            max_num_threads=None,

            avg_num_fds=None,
            max_num_fds=None,

            memory=float(d[u'mem']),

        )

    def kill(self, task):
        u"Terminates a task"
        raise NotImplementedError

    def kill_tasks(self, tasks):
        for group in grouper(tasks, 50):
            group = [x for x in group if x is not None]
            pids = u','.join([unicode(t.drm_jobID) for t in group])
            sp.Popen([u'qdel', pids], preexec_fn=preexec_function)


def qacct(task, timeout=600):
    start = time.time()
    with open(os.devnull, u'w') as DEVNULL:
        while True:
            if time.time() - start > timeout:
                raise ValueError(u'Could not qacct -j %s' % task.drm_jobID)
            try:
                out = sp.check_output([u'qacct', u'-j', unicode(task.drm_jobID)], stderr=DEVNULL)
                break
            except sp.CalledProcessError:
                pass
            time.sleep(1)

    def g():
        for line in out.strip().split(u'\n')[1:]:  # first line is a header
            k, v = re.split(u"\s+", line, maxsplit=1)
            yield k, v.strip()

    return OrderedDict(g())


def qstat_all():
    u"""
    returns a dict keyed by lsf job ids, who's values are a dict of bjob
    information about the job
    """
    try:
        lines = sp.check_output([u'qstat'], preexec_fn=preexec_function).strip().split(u'\n')
    except (sp.CalledProcessError, OSError):
        return {}
    keys = re.split(u"\s+", lines[0])
    bjobs = {}
    for l in lines[2:]:
        items = re.split(u"\s+", l.strip())
        bjobs[items[0]] = dict(list(izip(keys, items)))
    return bjobs


def preexec_function():
    # Ignore the SIGINT signal by setting the handler to the standard
    # signal handler SIG_IGN.  This allows Cosmos to cleanly
    # terminate jobs when there is a ctrl+c event
    os.setpgrp()
    return os.setsid
