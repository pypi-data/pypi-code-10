from __future__ import division
from __future__ import absolute_import
import os
import re
from .DRM_Base import DRM
from cosmos.api import only_one
from .util import div, convert_size_to_kb


class DRM_DRMAA(DRM):
    name = u'drmaa'
    _session = None

    def __init__(self, *args, **kwargs):
        super(DRM_DRMAA, self).__init__(*args, **kwargs)

    @property
    def session(self):
        if self._session is None:
            import drmaa

            self._session = drmaa.Session()
            self._session.initialize()
        return self._session

    def submit_job(self, task):
        jt = self.session.createJobTemplate()
        # jt.workingDirectory = settings['working_directory']
        jt.remoteCommand = task.output_command_script_path
        # jt.args             = cmd.split(' ')[1:]
        # jt.jobName          = jobAttempt.task.stage.name
        jt.outputPath = u':' + task.output_stdout_path
        jt.errorPath = u':' + task.output_stderr_path
        jt.jobEnvironment = os.environ

        jt.nativeSpecification = task.drm_native_specification or u''

        drm_jobID = self.session.runJob(jt)

        # prevents memory leak
        self.session.deleteJobTemplate(jt)

        return drm_jobID

    def filter_is_done(self, tasks):
        import drmaa

        jobid_to_task = dict((t.drm_jobID, t) for t in tasks)
        # Keep yielding jobs until timeout > 1s occurs or there are no jobs
        while len(jobid_to_task):
            try:
                # disable_stderr() #python drmaa prints whacky messages sometimes.  if the script just quits without printing anything, something really bad happend while stderr is disabled
                extra_jobinfo = self.session.wait(jobId=drmaa.Session.JOB_IDS_SESSION_ANY, timeout=1)._asdict()
                # enable_stderr()
            except drmaa.errors.InvalidJobException, e:
                # There are no jobs left to wait on!
                raise AssertionError(u'Should not be waiting on non-existant jobs.')
            except drmaa.errors.ExitTimeoutException:
                # Kobs are queued, but none are done yet.  Exit loop.
                # enable_stderr()
                break

            extra_jobinfo[u'successful'] = extra_jobinfo is not None and int(extra_jobinfo[u'exitStatus']) == 0 and extra_jobinfo[u'wasAborted'] == False and \
                                          extra_jobinfo[u'hasExited']
            yield jobid_to_task.pop(int(extra_jobinfo[u'jobId'])), parse_extra_jobinfo(extra_jobinfo)

    def drm_statuses(self, tasks):
        import drmaa

        def get_status(task):
            try:
                return self.decodestatus[self.session.jobStatus(unicode(task.drm_jobID))]
            except drmaa.errors.InvalidJobException:
                return u'?'

        return dict((task.drm_jobID, get_status(task)) for task in tasks)

    def kill(self, task):
        u"Terminates a task"
        import drmaa

        self.session.control(unicode(task.drm_jobID), drmaa.JobControlAction.TERMINATE)

    def kill_tasks(self, tasks):
        for t in tasks:
            self.kill(t)

    @property
    def decodestatus(self):
        import drmaa

        return {drmaa.JobState.UNDETERMINED: u'process status cannot be determined',
                drmaa.JobState.QUEUED_ACTIVE: u'job is queued and active',
                drmaa.JobState.SYSTEM_ON_HOLD: u'job is queued and in system hold',
                drmaa.JobState.USER_ON_HOLD: u'job is queued and in user hold',
                drmaa.JobState.USER_SYSTEM_ON_HOLD: u'job is queued and in user and system hold',
                drmaa.JobState.RUNNING: u'job is running',
                drmaa.JobState.SYSTEM_SUSPENDED: u'job is system suspended',
                drmaa.JobState.USER_SUSPENDED: u'job is user suspended',
                drmaa.JobState.DONE: u'job finished normally',
                drmaa.JobState.FAILED: u'job finished, but failed'}


def div(n, d):
    if d == 0.:
        return 1
    else:
        return n / d


def parse_extra_jobinfo(extra_jobinfo):
    d = extra_jobinfo[u'resourceUsage']
    return dict(
        exit_status=int(extra_jobinfo[u'exitStatus']),

        percent_cpu=div(float(d[u'cpu']), float(d[u'ru_wallclock'])),
        wall_time=float(d[u'ru_wallclock']),

        cpu_time=float(d[u'cpu']),
        user_time=float(d[u'ru_utime']),
        system_time=float(d[u'ru_stime']),

        avg_rss_mem=d[u'ru_ixrss'],
        max_rss_mem_kb=convert_size_to_kb(d[u'ru_maxrss']),
        avg_vms_mem_kb=None,
        max_vms_mem_kb=convert_size_to_kb(d[u'maxvmem']),

        io_read_count=int(float(d[u'ru_inblock'])),
        io_write_count=int(float(d[u'ru_oublock'])),
        io_wait=float(d[u'iow']),
        io_read_kb=float(d[u'io']),
        io_write_kb=float(d[u'io']),

        ctx_switch_voluntary=int(float(d[u'ru_nvcsw'])),
        ctx_switch_involuntary=int(float(d[u'ru_nivcsw'])),

        avg_num_threads=None,
        max_num_threads=None,

        avg_num_fds=None,
        max_num_fds=None,

        memory=float(d[u'mem']),

    )
