import copy
import os

import requests
from six import iteritems

QUAYIO_BUILD_SUCCESS_EVENT = 'build_success'
QUAYIO_BUILD_FAILURE_EVENT = 'build_failure'
QUAYIO_BUILD_TRIGGER_URL_KEY = 'quayio-build-trigger-url'


class QuayIOClient(requests.Session):
    def __init__(self, token):
        requests.Session.__init__(self)
        self.headers.update({'Authorization': 'Bearer ' + token})

    def list_repository(self, limit=10, **kwargs):
        """List repositories

        :param int limit:
          number of repositories fetched per query

        :keyword str namespace:
          the namespace to look into
        :keyword bool starred:
          retrieve only starred repositories
        :keyword bool public:
          retrieve only public repositories

        At least the `namespace`, `starred`, or `public` keyword must be
        specifed in this method.


        :keyword bool popularity:
          whether to include repository popularity metric

        :keyword bool last_modified:
          whether to include when the repository was last modified.
        """
        url = self._v1('repository')
        params = copy.copy(kwargs)
        params.update(limit=limit, page=1)
        while True:
            has_repo = False
            resp = self.get(url, params=params)
            resp.raise_for_status()
            repositories = resp.json()['repositories']
            for repository in repositories:
                has_repo = True
                yield repository
            if not has_repo:
                break
            params.update(page=params['page'] + 1, limit=limit)

    def get_repository(self, namespace, repository):
        """
        :param basestring namespace:
          repository namespace. If `None`, the username is used.
        :param basestring repository:
          repository name

        :return: dictionary if repository exists, `None` otherwise.
            {
                "stats": {
                    "pulls": {
                        "thirty_day": 0,
                        "today": 0
                    },
                    "pushes": {
                        "thirty_day": 0,
                        "today": 0
                    }
                },
                "description": "",
                "tags": {},
                "namespace": "{{ namespace }}",
                "is_organization": true,
                "can_write": true,
                "status_token": "",
                "is_public": true,
                "is_starred": false,
                "can_admin": true,
                "name": "{{ repository }}"
            }

        """
        url = self._v1(u'repository/{}/{}'.format(namespace, repository))
        r = self.get(url)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    def create_repository(self, namespace, repository,
                          public=True, description=None):
        """
        :param basestring namespace:
          repository namespace. If `None`, the username is used.
        :param basestring repository:
          repository name
        :param boolean public:
          wether the repository is public or private
        :param basestring description:
          Markdown description or the repository
        :return: dictionnary upon success
            {
                "namespace": "cogniteev",
                "name": "remove-me"
            }
        """
        payload = {
            'repository': repository,
            'visibility': 'public' if public else 'private',
            'description': description or '',
        }
        if namespace is not None:
            payload.update({'namespace': namespace})
        r = self.post(self._v1('repository'), json=payload)
        r.raise_for_status()
        return r.json()

    def get_or_create_repository(self, namespace, repository, **kwargs):
        """
        :param basestring namespace:
          repository namespace
        :param basestring repository
          repository name
        :param dict kwargs:
          arguments given to the `create_repository` member method
          when the repository has to be created.
        :returns: what the `get_repository` Setup new build trigger
        :param dict repository:
          `dict` as returned by `get_repository` or `get_or_create_repository`
          member methods.
        """
        url = 'repository/{namespace}/{repository}'
        url = url.format(
            namespace=namespace,
            repository=repository
        )
        r = self.get(self._v1(url))
        if r.status_code == 404:
            self.create_repository(namespace, repository, **kwargs)
            r = self.get(self._v1(url))
        r.raise_for_status()
        return r.json()

    def get_build_logs(self, repository, build_uuid):
        """Retrieve URL of a build logs

        :param dict repository:
          `dict` as returned by `get_repository` or `get_or_create_repository`
          member methods.
        :param string build_uuid:
          Quay build identifier

        :return: URL to the specified logs
        :rtype: basestring
        """
        url = 'repository/{namespace}/{repository}/build/{build_uuid}/logs'
        url = url.format(
            namespace=repository['namespace'],
            repository=repository['name'],
            build_uuid=build_uuid
        )
        r = self.get(self._v1(url))
        r.raise_for_status()
        return r.json()['logs_url']

    def get_build_trigger(self, repository):
        """
        :param dict repository:
          `dict` as returned by `get_repository` or `get_or_create_repository`
          member methods.
        """
        url = 'repository/{namespace}/{repository}/trigger/'
        url = url.format(
            namespace=repository['namespace'],
            repository=repository['name']
        )
        r = self.get(self._v1(url))
        r.raise_for_status()
        return r.json()['triggers']

    def start_build_trigger(self, repository, uuid, **payload):
        url = 'repository/{namespace}/{repository}/trigger/{uuid}/start'
        url = url.format(
            namespace=repository['namespace'],
            repository=repository['name'],
            uuid=uuid
        )
        r = self.post(self._v1(url), json=payload)
        r.raise_for_status()
        return r.json()

    def get_build(self, repository, build_uuid):
        """
        :param dict repository:
          `dict` as returned by `get_repository` or `get_or_create_repository`
          member methods

        :param str uuid:
          build identifier
        """
        url = 'repository/{namespace}/{repository}/build/{build_uuid}'
        url = url.format(
            namespace=repository['namespace'],
            repository=repository['name'],
            build_uuid=build_uuid
        )
        r = self.get(self._v1(url))
        r.raise_for_status()
        return r.json()

    def get_builds(self, repository, **kwargs):
        """
        :param dict repository:
          `dict` as returned by `get_repository` or `get_or_create_repository`
          member methods.

        :keyword int since:
          returns build since given UNIX timestamp
        :keyword int limit:
          maximum number of builds to returns.
          default is 0, meaning all.
        """
        params = dict((k, v) for k, v in iteritems(kwargs) if v)
        params.setdefault('limit', 0)
        url = 'repository/{namespace}/{repository}/build/'
        url = url.format(
            namespace=repository['namespace'],
            repository=repository['name']
        )
        r = self.get(self._v1(url), params=kwargs)
        r.raise_for_status()
        return r.json()['builds']

    def add_repository_user_permission(self, repository, user, role):
        """
        :param basestring role:
          Either "read", "write", or "admin"
        """
        url = 'repository/{namespace}/{repository}/permissions/user/{user}'
        url = url.format(
            namespace=repository['namespace'],
            repository=repository['name'],
            user=user
        )
        payload = {
            'role': role,
        }
        r = self.put(self._v1(url), json=payload)
        r.raise_for_status()

    def add_repository_team_permission(self, repository, team, role):
        """
        :param basestring role:
          Either "read", "write", or "admin"
        """
        url = 'repository/{namespace}/{repository}/permissions/team/{team}'
        url = url.format(
            namespace=repository['namespace'],
            repository=repository['name'],
            team=team
        )
        payload = {
            'role': role,
        }
        r = self.put(self._v1(url), json=payload)
        r.raise_for_status()

    def get_or_add_notification(self, repository, title,
                                event, method, config):
        """
        :param dict repository:
          `dict` as returned by `get_repository` or `get_or_create_repository`
          member methods.
        """
        url = 'repository/{namespace}/{repository}/notification/'
        url = url.format(
            namespace=repository['namespace'],
            repository=repository['name']
        )
        r = self.get(self._v1(url))
        r.raise_for_status()
        for notif in r.json().get('notifications', []):
            if notif['method'] == method and \
                    notif['event'] == event and \
                    notif.get('config', {}) == config:
                return notif['uuid']
        payload = {
            'title': title,
            'config': config,
            'event': event,
            'method': method,
        }
        r = self.post(self._v1(url), json=payload)
        r.raise_for_status()
        return r.json()['uuid']

    def add_member_to_team(self, organization, team, member):
        url = "organization/{org}/team/{team}/members/{member}"
        url = url.format(org=organization, team=team, member=member)
        r = self.put(self._v1(url))
        r.raise_for_status()

    # def create_team(self, organization, team, **kwargs):
    #     """
    #     :param basestring role:
    #       Can be either "member", "creator", or "admin"
    #     """
    #     url = "organization/{organization}/team/{team}/members"
    #     url.format(organization=organization, team=team)
    #     r = self.get(self._v1(url))
    #     if r.status_code() == 404:
    #         return self.create_team(organization, team, **kwargs)
    #     r.raise_for_status()
    #     return r.json()
    #
    # def create_team(self, organization, team, role="member",
    #                 description=None):
    #     url = "organization/{organization}/team/{team}"
    #     url.format(organization=organization, team=team)
    #     payload = {
    #         'role': role,
    #         'description': description or ''
    #     }
    #     r = self.put(self._v1(url), json=payload)
    #     r.raise_for_status()
    #     return r.json()

    def get_or_add_webhook_notification(self, repository, title, event, url):
        """
        :param dict repository:
          `dict` as returned by `get_repository` or `get_or_create_repository`
          member methods.
        """
        return self.get_or_add_notification(
            repository, title, event, 'webhook', {'url': url}
        )

    def get_or_add_slack_notification(self, repository, title,
                                      slack_webhook_url, event):
        """
        :param dict repository:
          `dict` as returned by `get_repository` or `get_or_create_repository`
          member methods.
        :param basestring title:
          Notification title
        :param basestring slack_webhook_url:
          Slack incoming webhook where is pushed to event
        :param basestring event:
          Quay.io event: either "build_failure", "build_success", FIXME
        """
        return self.get_or_add_notification(
            repository, title, event, 'slack', {'url': slack_webhook_url}
        )

    def get_team_members(self, organization, team):
        url = 'organization/{org}/team/{team}/members'.format(
            org=organization, team=team
        )
        r = self.get(self._v1(url))
        r.raise_for_status()
        return r.json().get('members', [])

    def update_team(self, org, team, permission, description=None):
        url = 'organization/{org}/team/{team}'.format(org=org, team=team)
        r = self.put(self._v1(url), json={
            'role': permission,
            'description': description or ''
        })
        r.raise_for_status()

    def _v1(self, url):
        return 'https://quay.io/api/v1/' + url


if os.environ.get('VCR_REBUILD_CASSETTE'):
    class QuayIOClientNoSession(QuayIOClient):
        def __init__(self, *args, **kwargs):
            super(QuayIOClientNoSession, self).__init__(*args, **kwargs)

        def get(self, url, **kwargs):
            return requests.get(url, headers=self.headers, **kwargs)

        def post(self, url, **kwargs):
            return requests.post(url, headers=self.headers, **kwargs)

        def put(self, url, **kwargs):
            return requests.put(url, headers=self.headers, **kwargs)

        def delete(self, url, **kwargs):
            return requests.delete(url, headers=self.headers, **kwargs)
    QuayIOClient = QuayIOClientNoSession
