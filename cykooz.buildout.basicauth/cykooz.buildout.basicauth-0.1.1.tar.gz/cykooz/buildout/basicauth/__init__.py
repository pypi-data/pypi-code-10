import logging
from six.moves import urllib

from setuptools import package_index
from zc.buildout.buildout import bool_option

from .credentials import Credentials
from .protected_ext import load_protected_extensions
from .download import inject_credentials, inject_urlretrieve_credentials


logger = logging.getLogger('cykooz.buildout.basicauth')


def install(buildout):
    buildout._raw.setdefault('basicauth', {})
    basicauth = buildout['basicauth']
    basicauth.setdefault('interactive', 'true')
    basicauth.setdefault('fetch-order', '\n'.join(("lovely", "buildout", "pypi", "prompt")))

    credentials = Credentials(
        buildout,
        fetchers=basicauth.get("fetch-order").split(),
        interactive=bool_option(basicauth, "interactive", True),
    )

    # Monkeypatch distribute
    logger.info('Monkeypatching setuptools to add http auth support')
    package_index.open_with_auth = inject_credentials(credentials)(package_index.open_with_auth)

    logger.info('Monkeypatching urlretrieve to add http auth support')
    urllib.request.urlretrieve = inject_urlretrieve_credentials(credentials)(urllib.request.urlretrieve)

    # Load the buildout:protected-extensions now that we have basicauth
    load_protected_extensions(buildout)
