"""
In order to support most means of downloading things via buildout, we need to
monkeypatch zc.buildout.download with a custom 401 handler, and add a custom
handler to urllib2.opener.handlers.
"""
import logging
import time
from six.moves import urllib
from six import StringIO, BytesIO

from zc.buildout import UserError


logger = logging.getLogger(__name__)


def strip_auth(url):
    scheme, netloc, path, params, query, frag = urllib.parse.urlparse(url)
    if scheme in ('http', 'https'):
        auth, host = urllib.parse.splituser(netloc)
        return urllib.parse.urlunparse((scheme, host, path, params, query, frag))
    return url


def _inject_credentials(url, username=None, password=None):
    """Used by `inject_credentials` decorators to actually do the injecting"""

    if username and password:
        scheme, netloc, path, params, query, frag = urllib.parse.urlparse(url)
        if scheme in ('http', 'https'):
            auth_part, host_part = urllib.parse.splituser(netloc)
            if not auth_part:  # If the URL doesn't have credentials in it already
                netloc = '%s:%s@%s' % (
                    urllib.parse.quote(username, ''),
                    urllib.parse.quote(password, ''),
                    host_part,
                )
                url = urllib.parse.urlunparse((scheme, netloc, path, params, query, frag))
    return url


class AuthError(Exception):
    pass


class NotFoundError(Exception):
    pass


class AuthAdaptor(object):
    ATTEMPTS = 3

    def __init__(self, credentials):
        self.credentials = credentials

    def call(self, *args, **kwargs):
        raise NotImplementedError(self.call)

    def attempt(self, url, *args, **kwargs):
        for i in range(self.ATTEMPTS):
            try:
                return self.call(url, *args, **kwargs)
            except AuthError:
                raise
            except NotFoundError:
                raise
            except Exception as e:
                logger.error("Attempt to access resource %s, failed. Will try again in %d seconds: %s", url, i, e)
                time.sleep(i)

        self.broken(url)

    def broken(self, url=''):
        raise UserError("Despite multiple attempts buildout was unable to access a remote resource %s" % url)

    def forbidden(self):
        raise UserError("Forbidden")

    def not_found(self):
        raise UserError("Resource not found")

    def __call__(self, url, *args, **kwargs):
        logger.debug('Downloading URL %s' % strip_auth(url))

        for username, password, cache in self.credentials.search(url):
            new_url = _inject_credentials(url, username, password)
            try:
                res = self.attempt(new_url, *args, **kwargs)

            except AuthError:
                logger.debug('Could not authenticate %s.' % (url,))

            except NotFoundError:
                self.not_found()

            else:
                self.credentials.success(url, username, password, cache)
                return res

        self.forbidden()


class addinfourl(urllib.response.addinfourl):

    def __init__(self, fp, headers, url, code=None):
        try:
            urllib.response.addinfourl.__init__(self, fp, headers, url, code)
        except TypeError:
            urllib.response.addinfourl.__init__(self, fp, headers, url)
            self.code = code


def inject_credentials(credentials):
    def decorator(auth_func):
        class SetuptoolsAdaptor(AuthAdaptor):
            def not_found(self):
                raise urllib.error.HTTPError('', 404, "Not found", {}, StringIO(""))

            def call(self, *args, **kwargs):
                try:
                    r = auth_func(*args, **kwargs)
                    fp = BytesIO(r.read())
                    resp = addinfourl(fp, r.headers, r.url, r.code)
                    return resp
                except Exception as e:
                    code = getattr(e, 'code', 'unknown')
                    if code in (401, 403):
                        raise AuthError
                    elif code == 404:
                        raise NotFoundError
                    else:
                        raise

        return SetuptoolsAdaptor(credentials)

    return decorator


def inject_urlretrieve_credentials(credentials):
    def decorator(auth_func):
        class UrlRetrieveAdaptor(AuthAdaptor):
            def call(self, *args, **kwargs):
                try:
                    res = auth_func(*args, **kwargs)
                    return res
                except IOError as e:
                    code = e.args[1]
                    if code in (401, 403):
                        raise AuthError
                    elif code == 404:
                        raise NotFoundError
                    else:
                        raise

        return UrlRetrieveAdaptor(credentials)

    return decorator
