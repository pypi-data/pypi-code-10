"""
tctalker.py
~~~~~~~~~~~~~~~~~
usage: tctalker.py [-h]
                   [--conf json-config-file]
                   [--verbose]
                   {cancel,rerun,report_completed} $taskId1 $taskId2

config-file must be a JSON object following this structure:
{
    "credentials": {
        "clientId": "...",
        "accessToken": "...",
        "certificate": {
            "version": 1,
            "scopes": ["...",
                       "...."
                       "...."],
            "start": 1448386098347,
            "expiry": 1448646198347,
            "seed": "...",
            "signature":"..."
        }
    }
}

This script is to be used to perform various operations against Taskcluster API
(e.g. rerun, cancel, reportCompleted)
"""

import os
import json
import logging
import argparse
import taskcluster

# Default configuration
_defaultConfig = {
    'credentials': {
        'clientId': os.environ.get('TASKCLUSTER_CLIENT_ID'),
        'accessToken': os.environ.get('TASKCLUSTER_ACCESS_TOKEN'),
        'certificate': os.environ.get('TASKCLUSTER_CERTIFICATE'),
    },
}


log = logging.getLogger(__name__)


def _load_json(name):
    with open(os.path.join(os.path.dirname(__file__), name), "rb") as f:
        return json.load(f)


class TCTalker(object):
    """The base TCTalker class"""

    def __init__(self, options=None):
        o = dict()
        o.update(_defaultConfig)
        if options:
            o.update(options)
        certificate = o['credentials']['certificate']
        try:
            json.loads(certificate)
        except TypeError:
            o['credentials']['certificate'] = json.dumps(certificate)

        self.options = o
        self.queue = taskcluster.Queue(self.options)

    def _get_job_status(self, task_id):
        """Private quick method to retrieve json describing the job"""
        return self.queue.status(task_id)

    def _get_last_run_id(self, task_id):
        """Private quick method to retrieve the last run_id for a job"""
        curr_status = self._get_job_status(task_id)
        return curr_status['status']['runs'][-1]['runId']

    def _claim_task(self, task_id):
        """Method to call whenever a task operation needs claiming first"""
        curr_status = self._get_job_status(task_id)
        run_id = curr_status['status']['runs'][-1]['runId']
        log.debug("Run id is %s", run_id)
        payload = {
            "workerGroup": curr_status['status']['workerType'],
            "workerId": "TCTalker",
        }
        self.queue.claimTask(task_id, run_id, payload)
        return run_id

    def cancel(self, task_id):
        """Map over http://docs.taskcluster.net/queue/api-docs/#cancelTask"""
        return self.queue.cancelTask(task_id)

    def rerun(self, task_id):
        """Map over http://docs.taskcluster.net/queue/api-docs/#rerunTask"""
        return self.queue.rerunTask(task_id)

    def report_completed(self, task_id):
        """Map http://docs.taskcluster.net/queue/api-docs/#reportCompleted"""
        run_id = self._get_last_run_id(task_id)
        return self.queue.reportCompleted(task_id, run_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["cancel", "rerun",
                                           "report_completed"],
                        help="action to be performed")
    parser.add_argument("taskIds", metavar="$taskId1 $taskId2 ....",
                        nargs="+", help="task ids to be processed")
    parser.add_argument("--conf", metavar="json-config-file", dest="config_file",
                        help="Config file containing login information for TC")
    parser.add_argument("--verbose", help="Increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    FORMAT = "(tctalker) - %(levelname)s - %(message)s"
    logging.basicConfig(format=FORMAT, level=loglevel)
    logging.getLogger(__name__).setLevel(logging.WARN)

    action, task_ids = args.action, args.taskIds
    taskcluster_config = None
    if hasattr(args, 'config_file') and args.config_file:
        taskcluster_config = _load_json(args.config_file)

    tct = TCTalker(taskcluster_config)
    func = getattr(tct, action)
    for _id in task_ids:
        ret = func(_id)
        log.info("Status returned for %s is %s", _id, str(ret))


if __name__ == "__main__":
    main()
