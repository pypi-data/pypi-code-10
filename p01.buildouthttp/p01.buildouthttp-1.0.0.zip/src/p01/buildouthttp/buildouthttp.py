##############################################################################
#
# Copyright (c) 2015 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id:$
"""
__docformat__ = "reStructuredText"

import pkg_resources
import sys

try:
    from urllib.parse import urlparse
    from urllib.parse import urlunparse
    from urllib import HTTPError

    from urllib import request
    from urllib.request import URLopener
    from urllib.request import FancyURLopener
except ImportError:
    # Python 2
    from urlparse import urlparse
    from urlparse import urlunparse
    from urllib import urlencode
    from urllib2 import HTTPError
    import urllib2 as request
    import urllib2
    from urllib import URLopener
    from urllib import FancyURLopener


import os
import csv
import logging
import subprocess
from io import StringIO
from zc.buildout import download

log = logging.getLogger('p01.buildouthttp')

url_opener = request._opener
original_build_opener = request.build_opener


class CustomURLOpener(FancyURLopener):

    http_error_default = URLopener.http_error_default

    def __init__(self, creds, github_creds, github_repos):
        self.creds = {}
        self.github_creds = github_creds
        self.github_repos = github_repos
        for realm, uris, user, password in creds:
            # parts = urllib_parse.urlparse(uris)
            parts = urlparse(uris)
            self.creds[(parts[1], realm)] = (user, password)
        FancyURLopener.__init__(self)

    def retrieve(self, url, filename=None, reporthook=None, data=None):
        if self.github_creds and not data:
            # scheme, netloc, path, params, query, fragment = urllib_parse.urlparse(
            #     url)
            scheme, netloc, path, params, query, fragment = urlparse(url)
            if (scheme == 'https'
                and netloc.endswith('github.com')
                and isPrivate(url, self.github_repos)
               ):
                log.debug("Appending github credentials to url %r", url)
                token = self.github_creds
                # cred = urllib_parse.urlencode(dict(access_token=token))
                cred = urlencode(dict(access_token=token))
                query = '&'.join((query, cred))
            # url = urllib_parse.urlunparse((scheme, netloc, path, params,
            #                            query, fragment))
            url = urlunparse((scheme, netloc, path, params, query, fragment))
        return CustomURLOpener.retrieve(self, url, filename,
                                           reporthook, data)

    def prompt_user_passwd(self, host, realm):
        creds = self.creds.get((host, realm))
        if creds:
            return creds
        return CustomURLOpener.prompt_user_passwd(self, host, realm)


def setUpCustomURLOpener(creds, github_creds, github_repos):
    """Setup URLopener"""
    urlopener = CustomURLOpener(creds, github_creds, github_repos)


def monkeyPatchBuildOpener(*handlers):
    """Mokey patch build_opener method"""
    request.build_opener = lambda *a: original_build_opener(
        *handlers)
    request.install_opener(request.build_opener())


def get_github_credentials():

    """returns the credentials for the local git installation by using
    git config"""

    p = subprocess.Popen("git config github.accesstoken",
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    rc = p.wait()
    if rc:
        # failure to get config, so return silently
        return None
    token = p.stdout.readline().strip()
    if token:
        log.debug("Found github accesstoken %r", token)
        return token


def isPrivate(urlPath, repos):
    """Check if a URL is a private URL

    >>> isPrivate('/downloads/me/', None)
    True
    >>> isPrivate('/downloads/me/', [])
    False
    >>> isPrivate('/downloads/me/', ['me'])
    True
    >>> isPrivate('/repos/me/', ['me'])
    True
    >>> isPrivate('/downloads/me/', ['unknown'])
    False
    >>> isPrivate('/somewhere/me/', ['me'])
    False
    """
    # If provided check whitelist of Github repos in the format
    # "<userororg>/<repo>", for either API v3 or static downloads
    if repos is None:
        # for backward compatibility all repos are private if there is no
        # "github-repos" entry in the buildout section.
        return True
    # now check the whitelist
    for repo in repos:
        if not repo:
            # ignore empty entries
            continue
        api_repo = "/repos/%s/" % (repo,)
        dl_repo = "/downloads/%s/" % (repo,)
        if api_repo in urlPath or dl_repo in urlPath:
            return True
    return False


class GithubHandler(request.BaseHandler):
    """This handler creates a post request with login and token

    see http://github.com/blog/170-token-authentication for details

    With a none github url the resulting request is unchanged::

    >>> req = request.Request('http://example.com/downloads/me/')
    >>> handler = GithubHandler('--mytoken--')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'http://example.com/downloads/me/'
    >>> res is req
    True

    With a github url we get the access token::

    >>> req = request.Request('https://github.com/downloads/me/')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'https://github.com/downloads/me/?access_token=--mytoken--'

    If we provide an empty whitelist we get all github requests without a
    token::

    >>> handler = GithubHandler('--mytoken--', [])
    >>> req = request.Request('https://github.com/downloads/me/')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'https://github.com/downloads/me/'

    If the repository is in the whitelist is receives a token::

    >>> handler = GithubHandler('--mytoken--', ['me'])
    >>> req = request.Request('https://github.com/downloads/me/')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'https://github.com/downloads/me/?access_token=--mytoken--'

    >>> req = request.Request(
    ...           'https://github.com/downloads/me/?a=1&b=2')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'https://github.com/downloads/me/?a=1&b=2&access_token=--mytoken--'

    If no timeout is set in the original request, the timeout is set to 60::

    >>> hasattr(req, 'timeout')
    False
    >>> res.timeout
    60


    The timeout from the original request is preseverd in the result::

    >>> req = request.Request('https://github.com/downloads/me/?a=1&b=2')
    >>> req.timeout = 42
    >>> res = handler.https_request(req)
    >>> res.timeout
    42

    """

    def __init__(self, token, repos=None):
        self._token = token
        self._repos = repos

    def https_request(self, req):
        get_host = lambda: (req.get_host() if hasattr(req, "get_host") else req.host)
        if req.get_method() == 'GET' and get_host().endswith('github.com'):
            url = req.get_full_url()
            # scheme, netloc, path, params, query, fragment = \
            #                             urllib_parse.urlparse(url)
            scheme, netloc, path, params, query, fragment = urlparse(url)
            if isPrivate(path, self._repos):
                log.debug("Found private github url %r", (url,))
                # token = urllib_parse.urlencode(dict(access_token=self._token))
                token = urlencode(dict(access_token=self._token))
                query = '&'.join([p for p in (query, token) if p])
                # new_url = urllib_parse.urlunparse((scheme, netloc, path, params,
                #                                query, fragment))
                new_url = urlunparse((scheme, netloc, path, params, query,
                    fragment))
                timeout = getattr(req, 'timeout', 60)
                old_req = req
                req = request.Request(new_url)
                req.timeout = timeout
                # Re-add user-agent, as the GitHub API requires this for auth
                req.add_header('user-agent', old_req.get_header('user-agent',
                                                            'Python-urllib2'))
            else:
                log.debug("Github url %r blocked by buildout.github-repos" %
                          (url,))
                log.debug(self._repos)
        return req


class CredHandler(request.HTTPBasicAuthHandler):

    """This handler adds basic auth credentials to the request upon a 401

    >>> auth_handler = CredHandler()
    >>> auth_handler.add_password('myrealm', 'http://example.com',
    ...                           'user', 'password')

    >>> from six import StringIO
    >>> fp = StringIO('The error body')
    >>> req = request.Request('http://example.com')
    >>> auth_handler.http_error_401(req, fp, 401, 'msg', {})
    """

    def http_error_401(self, req, fp, code, msg, headers):
        try:
            #python 2.6 introduces this attribute and fails the request on 5
            #but since we're process global this fails on the 5th download
            #there's no reset_retry_count(), so clear it here:
            self.retried = 0
        except AttributeError:
            pass

        log.debug('getting url: %r' % req.get_full_url())
        try:
            res = request.HTTPBasicAuthHandler.http_error_401(
                self, req, fp, code, msg, headers)
        # except urllib_error.HTTPError as err:
        except HTTPError as err:
            log.error('failed to get url: %r %r', req.get_full_url(), err.code)
            raise
        except Exception as err:
            log.error('failed to get url: %r %s', req.get_full_url(), str(err))
            raise
        else:
            if res is None:
                log.error('failed to get url: %r, check your realm',
                          req.get_full_url())
            elif res.code >= 400:
                log.error('failed to get url: %r %r', res.url, res.code)
            else:
                log.debug('got url: %r %r', res.url, res.code)
            return res


def prompt_passwd(realm, user):
    from getpass import getpass
    password = getpass('>>> Password for {} - {}: '.format(realm, user))
    return password


def install(buildout=None, pwd_path=None):
    pwdsf = StringIO()
    combined_creds = []
    github_creds = None
    creds = []
    local_pwd_path = ''
    github_repos = None
    if buildout is not None:
        local_pwd_path = os.path.join(
            buildout['buildout']['directory'],
            '.httpauth')
        if 'github-repos' in buildout['buildout']:
            github_repos = buildout['buildout']['github-repos'].split('\n')
    system_pwd_path = os.path.join(
        os.path.expanduser('~'),
        '.buildout',
        '.httpauth')

    def combine_cred_file(file_path, combined_creds):
        if file_path is None or not os.path.exists(file_path):
            return
        cred_file = open(file_path)
        combined_creds += [l.strip()
                            for l in cred_file.readlines() if l.strip()]
        cred_file.close()
    # combine all the possible .httpauth files together
    combine_cred_file(pwd_path, combined_creds)
    combine_cred_file(local_pwd_path, combined_creds)
    combine_cred_file(system_pwd_path, combined_creds)
    pwdsf_len = pwdsf.write(u"\n".join(combined_creds))
    pwdsf.seek(0)
    if not pwdsf_len:
        pwdsf = None
        log.warn('Could not load authentication information')
    try:
        auth_handler = CredHandler()
        github_creds = get_github_credentials()
        new_handlers = []
        if github_creds:
            new_handlers.append(GithubHandler(github_creds, github_repos))
        if pwdsf:
            for l, row in enumerate(csv.reader(pwdsf)):
                if len(row) == 3:
                    realm, uris, user = (el.strip() for el in row)
                    password = prompt_passwd(realm, user)
                elif len(row) == 4:
                    realm, uris, user, password = (el.strip() for el in row)
                else:
                    raise RuntimeError(
                        "Authentication file cannot be parsed %s:%s" % (
                            pwd_path, l + 1))
                creds.append((realm, uris, user, password))
                log.debug('Added credentials %r, %r' % (realm, uris))
                auth_handler.add_password(realm, uris, user, password)
        if creds:
            new_handlers.append(auth_handler)
        if creds or github_creds:
            setUpCustomURLOpener(creds, github_creds, github_repos)
        if new_handlers:
            if url_opener is not None:
                handlers = url_opener.handlers[:]
                handlers[:0] = new_handlers
            else:
                handlers = new_handlers
            # monkey patch build_opener
            monkeyPatchBuildOpener(*handlers)
    finally:
        if pwdsf:
            pwdsf.close()


def unload(buildout=None):
    request.build_opener = original_build_opener
    request.install_opener(request.build_opener())
