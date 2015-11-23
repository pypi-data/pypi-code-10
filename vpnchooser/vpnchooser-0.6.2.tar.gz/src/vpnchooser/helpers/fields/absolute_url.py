# -*- encoding: utf-8 -*-

from urllib.parse import urlparse, urlunparse

from flask.ext.restful.fields import Url
from flask.helpers import url_for


class AbsoluteUrl(Url):
    def __init__(self,
                 endpoint,
                 absolute=True,
                 scheme=None,
                 data_func=None):
        super(AbsoluteUrl, self).__init__(
            endpoint=endpoint,
            absolute=absolute,
            scheme=scheme,
        )
        self.data_func = data_func

    def output(self, key, obj):
        if self.data_func:
            data = self.data_func(obj)
            o = urlparse(
                url_for(self.endpoint, _external=self.absolute, **data)
            )
            if self.absolute:
                scheme = self.scheme if self.scheme is not None else o.scheme
                return urlunparse(
                    (scheme, o.netloc, o.path, "", "", ""))
            return urlunparse(("", "", o.path, "", "", ""))
        else:
            return super(AbsoluteUrl, self).output(key, obj)


class NullableAbsoluteUrl(AbsoluteUrl):
    def output(self, key, obj):
        try:
            return super(NullableAbsoluteUrl, self).output(key, obj)
        except Exception:
            return None
