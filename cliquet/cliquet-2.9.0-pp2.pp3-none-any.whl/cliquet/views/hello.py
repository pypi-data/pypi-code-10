from pyramid.security import NO_PERMISSION_REQUIRED

from cliquet import Service

hello = Service(name="hello", path='/', description="Welcome")


@hello.get(permission=NO_PERMISSION_REQUIRED)
def get_hello(request):
    """Return information regarding the current instance."""
    settings = request.registry.settings
    project_name = settings['project_name']
    data = dict(
        hello=project_name,
        version=settings['project_version'],
        url=request.route_url(hello.name),
        documentation=settings['project_docs']
    )

    eos = get_eos(request)
    if eos:
        data['eos'] = eos

    data['settings'] = {}
    public_settings = request.registry.public_settings
    # Public settings will be prefixed with project name, unless explicitly
    # specified with cliquet. (for retrocompability of clients for example).
    for setting in list(public_settings):
        if setting.startswith('cliquet.'):
            unprefixed = setting.replace('cliquet.', '', 1)
            value = settings[unprefixed]
        elif setting.startswith(project_name + '.'):
            unprefixed = setting.replace(project_name + '.', '')
            value = settings[unprefixed]
        else:
            value = settings[setting]
        data['settings'][setting] = value

    prefixed_userid = getattr(request, 'prefixed_userid', None)
    if prefixed_userid:
        data['userid'] = prefixed_userid

    return data


def get_eos(request):
    return request.registry.settings['eos']
