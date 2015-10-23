# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""SGE batch system Tasks.

Adapted by Jake Feala (@jfeala) from
`LSF extension <https://github.com/dattalab/luigi/blob/lsf/luigi/lsf.py>`_
by Alex Wiltschko (@alexbw)
Maintained by Jake Feala (@jfeala)

SunGrid Engine is a job scheduler used to allocate compute resources on a
shared cluster. Jobs are submitted using the ``qsub`` command and monitored
using ``qstat``. To get started, install luigi on all nodes.

To run luigi workflows on an SGE cluster, subclass
:class:`luigi.contrib.sge.SGEJobTask` as you would any :class:`luigi.Task`,
but override the ``work()`` method, instead of ``run()``, to define the job
code. Then, run your Luigi workflow from the master node, assigning > 1
``workers`` in order to distribute the tasks in parallel across the cluster.

The following is an example usage (and can also be found in ``sge_tests.py``)

.. code-block:: python

    import logging
    import luigi
    from luigi.contrib.sge import SGEJobTask

    logger = logging.getLogger('luigi-interface')


    class TestJobTask(SGEJobTask):

        i = luigi.Parameter()

        def work(self):
            logger.info('Running test job...')
            with open(self.output().path, 'w') as f:
                f.write('this is a test')

        def output(self):
            return luigi.LocalTarget(os.path.join('/home', 'testfile_' + str(self.i)))


    if __name__ == '__main__':
        tasks = [TestJobTask(i=str(i), n_cpu=i+1) for i in range(3)]
        luigi.build(tasks, local_scheduler=True, workers=3)


The ``n-cpu`` parameter allows you to define different compute resource
requirements (or slots, in SGE terms) for each task. In this example, the
third Task asks for 3 CPU slots. If your cluster only contains nodes with
2 CPUs, this task will hang indefinitely in the queue. See the docs for
:class:`luigi.contrib.sge.SGEJobTask` for other SGE parameters. As for any
task, you can also set these in your luigi configuration file as shown below.
The default values below were matched to the values used by MIT StarCluster,
an open-source SGE cluster manager for use with Amazon EC2::

    [SGEJobTask]
    shared-tmp-dir = /home
    parallel-env = orte
    n-cpu = 2


"""


# This extension is modeled after the hadoop.py approach.
#
# Implementation notes
# The procedure:
# - Pickle the class
# - Construct a qsub argument that runs a generic runner function with the path to the pickled class
# - Runner function loads the class from pickle
# - Runner function hits the work button on it

import os
import subprocess
import time
import sys
import logging
import random
import shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

import luigi
import luigi.hadoop
from luigi.contrib import sge_runner

logger = logging.getLogger('luigi-interface')
logger.propagate = 0

POLL_TIME = 5  # decided to hard-code rather than configure here


def _clean_task_id(task_id):
    """Clean the task ID so qsub allows it as a "name" string."""
    for c in ['\n', '\t', '\r', '/', ':', '@', '\\', '*', '?', ',', '=', ' ', '(', ')']:
        task_id = task_id.replace(c, '-')
    return task_id


def _parse_qstat_state(qstat_out, job_id):
    """Parse "state" column from `qstat` output for given job_id

    Returns state for the *first* job matching job_id. Returns 'u' if
    `qstat` output is empty or job_id is not found.

    """
    if qstat_out.strip() == '':
        return 'u'
    lines = qstat_out.split('\n')
    # skip past header
    while not lines.pop(0).startswith('---'):
        pass
    for line in lines:
        if line:
            job, prior, name, user, state = line.strip().split()[0:5]
            if int(job) == int(job_id):
                return state
    return 'u'


def _parse_qsub_job_id(qsub_out):
    """Parse job id from qsub output string.

    Assume format:

        "Your job <job_id> ("<job_name>") has been submitted"

    """
    return int(qsub_out.split()[2])


def _build_qsub_command(cmd, job_name, outfile, errfile, pe, n_cpu):
    """Submit shell command to SGE queue via `qsub`"""
    qsub_template = """echo {cmd} | qsub -o ":{outfile}" -e ":{errfile}" -V -r y -pe {pe} {n_cpu} -N {job_name}"""
    return qsub_template.format(
        cmd=cmd, job_name=job_name, outfile=outfile, errfile=errfile,
        pe=pe, n_cpu=n_cpu)


class SGEJobTask(luigi.Task):

    """Base class for executing a job on SunGrid Engine

    Override ``work()`` (rather than ``run()``) with your job code.

    Parameters:

    - n_cpu: Number of CPUs (or "slots") to allocate for the Task. This
          value is passed as ``qsub -pe {pe} {n_cpu}``
    - parallel_env: SGE parallel environment name. The default is "orte",
          the parallel environment installed with MIT StarCluster. If you
          are using a different cluster environment, check with your
          sysadmin for the right pe to use. This value is passed as {pe}
          to the qsub command above.
    - shared_tmp_dir: Shared drive accessible from all nodes in the cluster.
          Task classes and dependencies are pickled to a temporary folder on
          this drive. The default is ``/home``, the NFS share location setup
          by StarCluster

    """

    n_cpu = luigi.IntParameter(default=2, significant=False)
    shared_tmp_dir = luigi.Parameter(default='/home', significant=False)
    parallel_env = luigi.Parameter(default='orte', significant=False)

    def _fetch_task_failures(self):
        if not os.path.exists(self.errfile):
            logger.info('No error file')
            return []
        with open(self.errfile, "r") as f:
            errors = f.readlines()
        if errors == []:
            return errors
        if errors[0].strip() == 'stdin: is not a tty':  # SGE complains when we submit through a pipe
            errors.pop(0)
        return errors

    def _init_local(self):

        # Set up temp folder in shared directory (trim to max filename length)
        base_tmp_dir = self.shared_tmp_dir
        random_id = '%016x' % random.getrandbits(64)
        folder_name = _clean_task_id(self.task_id) + '-' + random_id
        self.tmp_dir = os.path.join(base_tmp_dir, folder_name)
        max_filename_length = os.fstatvfs(0).f_namemax
        self.tmp_dir = self.tmp_dir[:max_filename_length]
        logger.info("Tmp dir: %s", self.tmp_dir)
        os.makedirs(self.tmp_dir)

        # Dump the code to be run into a pickle file
        logging.debug("Dumping pickled class")
        self._dump(self.tmp_dir)

        # Make sure that all the class's dependencies are tarred and available
        logging.debug("Tarballing dependencies")
        # Grab luigi and the module containing the code to be run
        packages = [luigi] + [__import__(self.__module__, None, None, 'dummy')]
        luigi.hadoop.create_packages_archive(packages, os.path.join(self.tmp_dir, "packages.tar"))

    def run(self):
        self._init_local()
        self._run_job()
        # The procedure:
        # - Pickle the class
        # - Tarball the dependencies
        # - Construct a qsub argument that runs a generic runner function with the path to the pickled class
        # - Runner function loads the class from pickle
        # - Runner class untars the dependencies
        # - Runner function hits the button on the class's work() method

    def work(self):
        """Override this method, rather than ``run()``,  for your actual work."""
        pass

    def _dump(self, out_dir=''):
        """Dump instance to file."""
        self.job_file = os.path.join(out_dir, 'job-instance.pickle')
        if self.__module__ == '__main__':
            d = pickle.dumps(self)
            module_name = os.path.basename(sys.argv[0]).rsplit('.', 1)[0]
            d = d.replace('(c__main__', "(c" + module_name)
            open(self.job_file, "w").write(d)

        else:
            pickle.dump(self, open(self.job_file, "w"))

    def _run_job(self):

        # Build a qsub argument that will run sge_runner.py on the directory we've specified
        runner_path = sge_runner.__file__
        if runner_path.endswith("pyc"):
            runner_path = runner_path[:-3] + "py"
        job_str = 'python {0} "{1}"'.format(runner_path, self.tmp_dir)  # enclose tmp_dir in quotes to protect from special escape chars

        # Build qsub submit command
        self.outfile = os.path.join(self.tmp_dir, 'job.out')
        self.errfile = os.path.join(self.tmp_dir, 'job.err')
        submit_cmd = _build_qsub_command(job_str, self.task_family, self.outfile,
                                         self.errfile, self.parallel_env, self.n_cpu)
        logger.debug('qsub command: \n' + submit_cmd)

        # Submit the job and grab job ID
        output = subprocess.check_output(submit_cmd, shell=True)
        self.job_id = _parse_qsub_job_id(output)
        logger.debug("Submitted job to qsub with response:\n" + output)

        self._track_job()

        # Now delete the temporaries, if they're there.
        if self.tmp_dir and os.path.exists(self.tmp_dir):
            logger.info('Removing temporary directory %s' % self.tmp_dir)
            shutil.rmtree(self.tmp_dir)

    def _track_job(self):
        while True:
            # Sleep for a little bit
            time.sleep(POLL_TIME)

            # See what the job's up to
            # ASSUMPTION
            qstat_out = subprocess.check_output(['qstat'])
            sge_status = _parse_qstat_state(qstat_out, self.job_id)
            if sge_status == 'r':
                logger.info('Job is running...')
            elif sge_status == 'qw':
                logger.info('Job is pending...')
            elif 'E' in sge_status:
                logger.error('Job has FAILED:\n' + '\n'.join(self._fetch_task_failures()))
                break
            elif sge_status == 't' or sge_status == 'u':
                # Then the job could either be failed or done.
                errors = self._fetch_task_failures()
                if not errors:
                    logger.info('Job is done')
                else:
                    logger.error('Job has FAILED:\n' + '\n'.join(errors))
                break
            else:
                logger.info('Job status is UNKNOWN!')
                logger.info('Status is : %s' % sge_status)
                raise Exception("job status isn't one of ['r', 'qw', 'E*', 't', 'u']: %s" % sge_status)


class LocalSGEJobTask(SGEJobTask):
    """A local version of SGEJobTask, for easier debugging.

    This version skips the ``qsub`` steps and simply runs ``work()``
    on the local node, so you don't need to be on an SGE cluster to
    use your Task in a test workflow.
    """

    def run(self):
        self.work()
