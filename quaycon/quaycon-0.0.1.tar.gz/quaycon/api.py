import itertools
import logging
import time

import requests
from six import iteritems

from . config import load_config, save_config
from . utils import (
    ask_confirmation,
    parse_repository,
    QUAYIO_REGISTRY,
    to_timestamp,
)
from . client import QuayIOClient
from . errors import (
    MissingTokenError,
    UnknownBuildTrigger,
    UnknownOrganization,
    UnknownRepository,
)

LOGGER = logging.getLogger(__name__)


class QuayCon(object):
    def __init__(self, config=None):
        self.config = config or load_config()
        self.quay_clients = {}

    def touch(self, registry, org, name, tag, **kwargs):
        """ Simulate update of a Docker image to trigger build of its
        dependencies.

        :param str registry:
          registry of the built image

        :param str org:
          organization of the built image

        :param str tag:
          built image tag

        :keyword int wait:
          Delay in seconds between to attempts to see it build completed.
          If set to 0 and `recursive` is disabled, then do not wait for the
          build to complete. Default is 0.

        :keyword bool recursive:
          Build the entire dependency sub-tree. Default is `False`. If `wait`
          keyword is not specified, value is set to 60.
        """
        recursive = kwargs.get('recursive', False)
        if recursive and 'wait' not in kwargs:
            wait = 60
        else:
            wait = kwargs.get('wait', 0)

        repo = self.__get_repository(registry, org, name, raise_=True)
        triggers = repo.get('on_build', {}).get('tags', {}).get(tag, {})
        builds = self.__build_triggers(triggers)
        if not recursive and wait == 0:
            for build in builds:
                yield build
        build_queue = list(builds)
        while any(build_queue):
            time.sleep(wait)
            build = build_queue.pop()
            namespace = build['repository']['namespace']
            build = self._quay_client(namespace).get_build(build['repository'],
                                                           build['id'])
            phase = build['phase']
            if phase not in [u'error', u'complete']:
                build_queue.append(build)
            else:
                LOGGER.info('Build {}/{}/{} has terminated, status: {}'.format(
                    QUAYIO_REGISTRY,
                    namespace,
                    build['repository']['name'],
                    phase
                ))
                yield build
                if recursive and phase == 'complete':
                    build_queue.extend(self._fire_dependant_builds(build))

    def _fire_dependant_builds(self, build):
        builds_generators = []
        repo = self.__get_repository(
            QUAYIO_REGISTRY,
            build['repository']['namespace'],
            build['repository']['name']
        )
        if repo is None:
            LOGGER.warn('Unregistered repository')
        else:
            all_triggers = repo.get('on_build', {}).get('tags', {})
            for tag in build['tags']:
                triggers = all_triggers.get(tag, {})
                builds_generators.append(self.__build_triggers(triggers))
        return itertools.chain(*builds_generators)

    def _quay_client(self, namespace):
        quay = self.quay_clients.get(namespace)
        if quay is None:
            quay = self.quay_clients.setdefault(
                namespace,
                QuayIOClient(self.__get_token(
                    QUAYIO_REGISTRY,
                    namespace,
                    raise_=True)
                )
            )
        return quay

    def __build_triggers(self, triggers):
        if not any(triggers):
            LOGGER.warn("No build to trigger")
        for reliant, builds in iteritems(triggers):
            for build in builds:
                reliant = parse_repository(reliant)[:-1]  # get rid of tag
                build_details = self.build(reliant,
                                           build.pop('trigger_uuid', None))
                if build_details is not None:
                    yield build_details

    def build(self, repo, uuid=None):
        """
        :param tuple repo:
          tuple of 3 elements (registry, organization, name) describing
          the repository to build.
          if repository is hosted on Docker Hub,
          then `registry` should be `None`.
        """
        reg, org, name = repo
        if reg != QUAYIO_REGISTRY:
            LOGGER.warn('Cannot trigger non {} build for: {}'.format(
                QUAYIO_REGISTRY, '/'.join(filter(lambda e: e, repo))
            ))
            return
        client = self._quay_client(org)
        build_triggers = client.get_build_trigger({
            'namespace': org,
            'name': name,
        })
        if uuid:
            build_trigger = list(filter(
                lambda b: b['id'] == uuid,
                build_triggers
            ))
            if not any(build_trigger):
                raise UnknownBuildTrigger(org, name, uuid)
            build_trigger = build_trigger[0]
        else:
            build_triggers = filter(
                lambda b: b['service'] != 'custom-git',
                build_triggers
            )
            if not any(build_triggers):
                raise Exception("Cannot find non 'custom-git' build trigger")
            elif len(build_triggers) == 1:
                build_trigger = build_triggers[0]
            else:
                raise Exception("Don't know which build trigger to use")
        LOGGER.info(u'Starting build of %s/%s/%s', reg, org, name)
        return client.start_build_trigger(dict(namespace=org, name=name),
                                          build_trigger['id'])

    def discover(self, org):
        client = self._quay_client(org)
        for repository in client.list_repository(namespace=org):
            # add repository to config if missing
            self.__get_repository(QUAYIO_REGISTRY, repository['namespace'],
                                  repository['name'], create=True)
            self.__add_bases(
                repository,
                self.repository_bases(repository)
            )

    def __add_bases(self, repository, bases):
        for (trigger_id, ref), base in bases.items():
            _base = parse_repository(base)
            b = self.__get_repository(*_base[:-1], create=True)
            tags = b.setdefault('on_build', {}).setdefault('tags', {})
            tag = tags.setdefault(_base[-1], {})
            full = u'/'.join([
                QUAYIO_REGISTRY,
                repository['namespace'],
                repository['name']]
            )
            dependant_builds = tag.setdefault(full, [])
            to_add = dict(trigger_uuid=trigger_id, ref=ref)
            if to_add not in dependant_builds:
                dependant_builds.append(to_add)

    def repository_bases(self, repository):
        LOGGER.debug(u'Extracting base images of {} tags'.format(
            u'/'.join(repository))
        )
        org = repository['namespace']
        client = self._quay_client(org)

        def _last_scan():
            _repo = self.__get_repository(
                QUAYIO_REGISTRY,
                repository['namespace'],
                repository['name']
            ) or {}
            return _repo.get('last_scan')
        triggers = {}
        for build in client.get_builds(repository, since=_last_scan()):
            if build['phase'] != 'complete':
                continue
            ref = build.get('trigger_metadata', {}).get('ref')
            if ref is None:
                continue
            _build_trigger = build.get('trigger', {})
            if _build_trigger is None:
                # A build trigger that have been deleted since them
                continue
            trigger_id = _build_trigger.get('id')
            if trigger_id is None:
                continue
            started = build.get('started')
            if started is None:
                continue
            timestamp = to_timestamp(started)
            key = (trigger_id, ref)
            candidate_ts = triggers.get(key, {}).get('started_ts', 0)
            if candidate_ts < timestamp:
                build['started_ts'] = timestamp
                triggers[key] = build
        bases = {}
        for (trigger_id, ref), build in triggers.items():
            build_id = build['id']
            logs_url = client.get_build_logs(repository, build_id)
            resp = requests.get(logs_url)
            resp.raise_for_status()
            for log in resp.json()['logs']:
                if log['type'] == 'phase' and log['message'] == 'pulling':
                    tag = log['data']['base_image_tag']
                    base = log['data']['base_image']
                    bases[(trigger_id, ref)] = '{}:{}'.format(base, tag)
                    break
        return bases

    def build_trigger_bases(self, repository, trigger):
        if trigger['service'] == 'custom-git':
            return []

    def __get_token(self, registry, org, raise_=False):
        _org = self.__get_organization(registry, org, raise_=raise_)
        token = _org.get(u'token')
        if raise_ and token is None:
            raise MissingTokenError(org)
        return token

    def __get_organization(self, registry, name,
                           raise_=False, create=False):
        organizations = self.config.get('organizations', {})
        name = self._org_name(registry, name)
        if create:
            org = organizations.setdefault(name, {})
        else:
            org = organizations.get(name)
        if org is None:
            if raise_:
                raise UnknownOrganization(name)
            else:
                return None
        if org.get('repositories') is None:
            org['repositories'] = {}

        return org

    def add_organization(self, registry, name, token):
        organizations = self.config.setdefault('organizations', {})
        org = {
            'token': token,
            'repositories': {}
        }
        organizations[self._org_name(registry, name)] = org
        return org

    @classmethod
    def _org_name(cls, registry, name):
        if registry is not None and any(registry):
            return '{}/{}'.format(registry, name)
        else:
            return name

    @property
    def organizations(self):
        return self.config['organizations'].keys()

    def __get_repository(self, registry, org, name, **kwargs):
        raise_ = kwargs.get('raise_', False)
        create = kwargs.get('create', False)
        orgname = org
        org = self.__get_organization(registry, org, **kwargs)
        image = org.get(u'repositories', {}).get(name)
        if raise_ and image is None:
            raise UnknownRepository(orgname, name)
        if create and image is None:
            image = {}
            org[u'repositories'][name] = image
        return image

    def save(self, confirm=False):
        if confirm:
            if not ask_confirmation('About to save configuration'):
                return
        save_config(self.config)
