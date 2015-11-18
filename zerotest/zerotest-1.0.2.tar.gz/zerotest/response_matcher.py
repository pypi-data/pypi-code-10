import logging


MatchError = AssertionError

LOG = logging.getLogger(__name__)

_SERIALIZABLE_CONTENT_TYPE = {'application/json': 'json'}


class ResponseMatcher(object):
    def __init__(self, ignore_headers=None, ignore_all_headers=False, ignore_fields=None):
        """
        :param ignore_headers: ignored headers when match response
        :param ignore_fields: ignored body fields, only work when response content-type is serializable type
        :return:
        """
        ignore_headers = ignore_headers or []
        self._ignore_headers = set(map(lambda h: h.upper(), ignore_headers))
        self._ignore_all_headers = ignore_all_headers
        self._ignore_fields = ignore_fields

    def _compare_status(self, r1, r2):
        assert r1.status == r2.status

    def __remove_ignore_headers(self, headers):
        return {k.upper(): headers[k] for k in headers if
                k.upper() not in self._ignore_headers}

    def _compare_headers(self, expect, real):
        if not self._ignore_all_headers:
            expect_headers = self.__remove_ignore_headers(expect.headers)
            real_headers = self.__remove_ignore_headers(real.headers)
            assert expect_headers == real_headers

    def __delete_ignore_fields(self, content):
        from zerotest.utils.data_helper import delete_path_from_dict
        for field_path in self._ignore_fields:
            if field_path in content:
                content.pop(field_path, None)
            else:
                delete_path_from_dict(content, field_path)

    def _handle_content_type_json(self, content):
        import json
        try:
            content = json.loads(content)
        except:
            LOG.error("detected json response, but raise a error in decoding")
            raise

        self.__delete_ignore_fields(content)
        return content

    def _compare_body(self, r1, r2):
        r1_content_type = r1.get_header('Content-Type')
        r2_content_type = r2.get_header('Content-Type')
        assert r1_content_type == r2_content_type
        r1_content = r1.body
        r2_content = r2.body
        content_type = _SERIALIZABLE_CONTENT_TYPE.get(r1_content_type)
        if self._ignore_fields and content_type:
            handler = getattr(self, '_handle_content_type_{}'.format(content_type))
            if handler:
                r1_content = handler(r1_content)
                r2_content = handler(r2_content)

        assert r1_content == r2_content

    def match_responses(self, expect, real):
        """
        compare requests
        :type expect: zerotest.response.Response
        :type real: zerotest.response.Response
        :return:
        """
        for attr in ('status', 'headers', 'body'):
            compare_func = '_compare_{}'.format(attr)
            getattr(self, compare_func)(expect, real)
