import argparse
import os
import sys
import textwrap
import inspect
import imp
from cocoon.task import Task
import logging
from colorlog import ColoredFormatter
from sets import Set

stream = logging.StreamHandler(sys.stderr)
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s "
    "%(levelname)-8s [%(name)s] %(message)s %(reset)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG':    'green',
        'INFO':     'cyan',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
stream.setFormatter(formatter)
logger = logging.getLogger("cocoon")
logger.addHandler(stream)
logger.setLevel(logging.INFO)

def main():
    cui_main(sys.argv[1:])

def cui_main(argv):
    if len(argv) == 0:
        msg = """\
        cocoon workflow engine
        Type cocoon -h for the help message
        """
        print(textwrap.dedent(msg))
        return

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', metavar='loglevel', help='set loglevel (debug|info|warning|error|critical)', default='info')

    sub_parsers = parser.add_subparsers(title='sub commands', help='sub-command help')

    parser_create = sub_parsers.add_parser('create', help='create a new workflow')
    parser_create.add_argument('name', help='project folder name')
    parser_create.set_defaults(func=create)

    parser_run = sub_parsers.add_parser('run', help='run a workflow')
    parser_run.add_argument('target', nargs='*', help='target task name')
    parser_run.set_defaults(func=run)

    parser_show = sub_parsers.add_parser('show', help='show workflow tasks')
    parser_show.add_argument('file', nargs='?', help='workflow file')
    parser_show.set_defaults(func=show)

    args, unknown = parser.parse_known_args(args = argv)
    set_loglevel(args)
    args.func(args)

def set_loglevel(args):
    logger.setLevel(logging.getLevelName(str.upper(args.l)))
    logger.debug('Setting log level: ' + args.l)

def create(args):
    logger.infog("create a workflow: " + args.name)
    basedir = args.name
    logger.info("Create a directory: " + basedir)
    os.mkdir(basedir)

def load_workflow():
    logger.debug("loading workflow")
    for root, dirs, files in os.walk(".", followlinks=True):
        for f in files:
            mod_name, ext = os.path.splitext(f)
            if ext != '.py':
                continue
            logger.info("loading file: " + f + ", module name: " + mod_name)
            m = imp.load_source(mod_name, f)
            for obj in (m.__dict__.values()):
                if(isinstance(obj, Task)):
                    logger.debug("found " + obj.describe())
                    yield obj

def leaf_tasks(task_list):
    candidates = Set([t.task_id for t in task_list])
    for t in task_list:
        for d in t.dependencies():
            candidates.remove(d)
    return [x for x in candidates]

def run(args):
    logger.info("run a workflow: " + repr(args))
    tasks = list(load_workflow())

    if len(args.target) == 0:
        # run leaf tasks
        logger.info("No target is given. Run leaf tasks")
        target_tasks = leaf_tasks(tasks)
    else:
        task_ids = [t.task_id for t in tasks]
        for t in args.target:
            if t not in task_ids:
                logger.error("task {} is not found".format(t))
                return
        target_tasks = args.target

    if len(target_tasks) == 0:
        logger.warn("No task is found")
        return


    logger.info("target task: " + repr(target_tasks))


def show(args):
    logger.debug("listing workflow tasks")
    tasks = load_workflow()
    for t in tasks:
        print(t.describe())
    logger.info('done.')


if __name__ == "__main__":
    import sys
    cui_main(sys.argv[1:])


