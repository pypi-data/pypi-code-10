# -*- coding: utf-8 -*-

"""Create and get profiles from a config file.

Profiles are stored in an INI file called CONFIG_FILE. To find
the location of the file, see the ``.constants`` package.

There can be many profiles in the CONFIG_FILE. Each profile is
named. For instance, suppose the file looks like this::

    [default]
    repo = jtpaasch/tabu
    token = af430ed...

    [jenkins]
    repo = jtpaasch/tabu
    token = 01cb354...

That file has two profiles, one called "default" and another called
"jenkins." Every profile needs two fields to be set: a "repo" and
a "token". The repo is the Github repo name in the form:: 

    <username>/<reponame>

The token is a Github Oauth2 token. The Github literature sometimes
calls these "Personal Access Tokens." They can be created at Github.com
under your account setings.

You can create a profile by editing the CONFIG_FILE yourself, or
by calling the ``create_profile(profile_name, repo, token)`` function.

"""

import configparser
from .constants import CONFIG_FILE


def read_profile(name):
    """Get a named profile from the CONFIG_FILE."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    profile = config[name]
    repo = profile["repo"]
    token = profile["token"]
    return {"repo": repo, "token": token}


def write_profile(name, repo, token):
    """Save a profile to the CONFIG_FILE."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    profile = {"repo": repo, "token": token}
    config[name] = profile
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
    return profile


def ephemeral_profile(repo, token):
    """Generate a profile that's not on disk anywhere."""
    profile = {"repo": repo, "token": token}
    return profile
