# -*- coding: utf-8 -*-

"""Create and retreive profiles from a CONFIG_FILE.

Profiles are stored in an INI file CONFIG_FILE. To find the location
of that file, see the ``.constants`` package.

There can be many profiles in the CONFIG_FILE. Each profile is
named. For instance, suppose the file looks like this::

    [default]
    repo = jtpaasch/simplygithub
    token = af430ed...

    [jenkins]
    repo = jtpaasch/otherrepo
    token = 01cb354...

That file has two profiles, one called "default" and another called
"jenkins."

You can retrieve either of those profiles with the ``read_profile(name)``
function.

Notice that every profile has two values: a "repo" and a "token". The repo
is the Github repo name in the form::

    <username>/<reponame>

The token is a personal access token. Tokens can be created from your
Github page, under your account settings. See
https://help.github.com/articles/creating-an-access-token-for-command-line-use

You can create a profile by editing the CONFIG_FILE yourself, or
by calling the ``write_profile(profile_name, repo, token)`` function.

If you don't need to store the profile anywhere, you can instead use the
``ephemeral_profile(repo, token)`` function, which will create a profile
object in memory that you can use to connect to Github, but it will not
write anything to disk.

"""

import configparser
import errno
import os

from .constants import (CONFIG_FOLDER, CONFIG_FILE)


def make_sure_folder_exists(path):
    """Make sure a path exists."""
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def read_profile(name):
    """Get a named profile from the CONFIG_FILE.

    Args:

        name
            The name of the profile to load.

    Returns:
        A dictionary with the profile's ``repo`` and ``token`` values.

    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    profile = config[name]
    repo = profile["repo"]
    token = profile["token"]
    return {"repo": repo, "token": token}


def write_profile(name, repo, token):
    """Save a profile to the CONFIG_FILE.

    After you use this method to save a profile, you can load it anytime
    later with the ``read_profile()`` function defined above.

    Args:

        name
            The name of the profile to save.

        repo
            The Github repo you want to connect to. For instance,
            this repo is ``jtpaasch/simplygithub``.

        token
            A personal access token to connect to the repo. It is
            a hash that looks something like ``ff20ae42dc...``

    Returns:
        A dictionary with the profile's ``repo`` and ``token`` values.

    """
    make_sure_folder_exists(CONFIG_FOLDER)
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    profile = {"repo": repo, "token": token}
    config[name] = profile
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
    return profile


def ephemeral_profile(repo, token):
    """Generate a profile that's not saved on disk anywhere.

    This simply returns a profile dictionary with ``repo`` and ``token``
    values. It does not get saved on disk anywhere.

    Args:

        repo
            The Github repo you want to connect to. For instance,
            this repo is ``jtpaasch/simplygithub``.

        token
            A personal access token to connect to the repo. It is
            a hash that looks something like ``ff20ae42dc...``

    Returns:
        A dictionary with the profile's ``repo`` and ``token`` values.

    """
    profile = {"repo": repo, "token": token}
    return profile
