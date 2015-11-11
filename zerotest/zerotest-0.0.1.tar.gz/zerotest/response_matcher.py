__author__ = 'Hari Jiang'


class MatchError(RuntimeError):
    pass


class ResponseMatcher(object):
    def __init__(self, ignore_headers=None):
        ignore_headers = ignore_headers or []
        self._ignore_headers = set(map(lambda h: h.upper(), ignore_headers))

    def _compare_status(self, r1, r2):
        return r1.status == r2.status

    def _compare_headers(self, expect, real):
        expect_headers = {k.upper(): expect.headers[k] for k in expect.headers if
                          k.upper() not in self._ignore_headers}
        real_headers = {k.upper(): real.headers[k] for k in real.headers if
                        k.upper() not in self._ignore_headers}
        return expect_headers == real_headers

    def _compare_body(self, r1, r2):
        return r1.body == r2.body

    def match_responses(self, expect, real):
        """
        compare requests
        :type expect: zerotest.response.Response
        :type real: zerotest.response.Response
        :return:
        """
        for attr in ('status', 'headers', 'body'):
            compare_func = '_compare_{}'.format(attr)
            match = getattr(self, compare_func)(expect, real)
            if not match:
                raise MatchError(
                    '{} not match, expect: {}, got: {}'.format(attr, getattr(expect, attr), getattr(real, attr)))
