from datetime import datetime
import sys

from dateutil import parser
import six
import pytz

if six.PY3:
    raw_input = None  # prevent flake8 warning
if six.PY2:
    input = raw_input

DOCKER_HUB_REGISTRY = 'https://index.docker.io/v1'
OFFICIAL_DOCKER_HUB_ORG = '_'
QUAYIO_REGISTRY = 'quay.io'
UTC_EPOCH = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)


def ask_confirmation(operation=''):  # pragma: no-cover
    resp = None
    while resp is None:
        resp = input(operation + u' "yes" or "no": ')
        if resp.lower() == 'yes':
            resp = True
        elif resp.lower() == 'no':
            resp = False
        if not isinstance(resp, bool):
            sys.stderr.write("Sorry, I didn't understand...\n")
            resp = None
    return resp


def to_timestamp(date):
    date = parser.parse(date)
    if date.tzinfo is None:
        date = date.replace(tzinfo=pytz.utc)
    seconds = (date - UTC_EPOCH).total_seconds() * 1e3
    return int(seconds)


def parse_repository(repository):
    if repository.count(":") == 1:
        name, tag = repository.rsplit(":", 1)
    else:
        name = repository
        tag = 'latest'
    repo_split = name.split('/')
    if len(repo_split) == 1:
        registry = DOCKER_HUB_REGISTRY
        org = OFFICIAL_DOCKER_HUB_ORG
    elif len(repo_split) == 2:
        org, name = repo_split
        registry = DOCKER_HUB_REGISTRY
    elif len(repo_split) == 3:
        registry, org, name = repo_split
    else:
        raise Exception('Cannot parse repository: {}'.format(repository))
    return registry, org, name, tag
