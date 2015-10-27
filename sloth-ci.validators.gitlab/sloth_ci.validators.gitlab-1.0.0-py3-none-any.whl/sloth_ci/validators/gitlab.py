'''GitLab Sloth CI validator that validates the `GitLab <https://about.gitlab.com/>`_ payload against username and repo name (obtained from the Sloth app config).

Usage in the app config::

    provider:
        gitlab:
            # Repository title as it appears in the URL, i.e. slug.
            # Mandatory parameter.
            repo: sloth-ci

            # Only pushes to these branches will initiate a build.
            # Skip this parameter to allow all branches to fire builds.
            branches:
                - master
                - staging
'''


__title__ = 'sloth-ci.validators.gitlab'
__description__ = 'GitLab validator for Sloth CI'
__version__ = '1.0.0'
__author__ = 'Vladimir Akritskiy'
__author_email__ = 'lenin.lin@gmail.com'
__license__ = 'MIT'


def validate(request, validation_data):
    '''Validate GitLab payload against repo name (obtained from the Sloth app config).

    :param request_params: payload to validate
    :param validation_data: dictionary with the keys ``repo``, and ``branches``

    :returns: (status, message, list of extracted param dicts)
    '''

    from json import loads

    if request.method != 'POST':
        return (405, 'Payload validation failed: Wrong method, POST expected, got %s.' % request.method, [])

    try:
        payload = request.body.read().decode('utf8')

        parsed_payload = loads(payload)

        repo = parsed_payload['repository']['name']

        if repo != validation_data['repo']:
            return (403, 'Payload validation failed: wrong repository: %s' % repo, [])

        branch = {parsed_payload['ref'].split('/')[-1]}

        allowed_branches = set(validation_data.get('branches', branch))

        if not branch & allowed_branches:
            return (403, 'Payload validation failed: wrong branch: %s' % branch, [])

        return (200, 'Payload validated. Branch: %s' % branch, [{'branch': branch}])

    except Exception as e:
        return (400, 'Payload validation failed: %s' % e, [])
