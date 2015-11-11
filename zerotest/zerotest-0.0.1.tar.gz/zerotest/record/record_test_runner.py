from __future__ import print_function

__author__ = 'Hari Jiang'

import logging

from zerotest.record.formatter import Formatter
from zerotest.response_matcher import ResponseMatcher, MatchError
from zerotest.utils import print_line_notify

LOG = logging.getLogger(__name__)


class RecordTestRunner(object):
    """
    run tests from record data
    usage: RecordTestRunner('my_record.data', ignore_headers=['server']).run()
    """

    def __init__(self, filepath, endpoint=None, ignore_headers=None, verify_ssl=False):
        self._filepath = filepath
        self._endpoint = endpoint
        self._verify_ssl = verify_ssl
        self._formatter = Formatter()
        self._response_matcher = ResponseMatcher(ignore_headers=ignore_headers)

    def run(self):
        """
        run record
        :return: all_cases, failed
        """
        i = 0
        failed = 0
        print_line_notify("Start replay test cases from {}".format(self._filepath))
        with open(self._filepath, 'r') as record_file:
            while True:
                result = self._formatter.read_record(record_file)
                if result:
                    i += 1
                    request, response = result

                    # replace request host if set endpoint option
                    if self._endpoint:
                        request.endpoint = self._endpoint
                    real_response = response.from_requests_response(request.send_request(self._verify_ssl))
                    try:
                        self._response_matcher.match_responses(response, real_response)
                    except MatchError as e:
                        failed += 1
                        print_line_notify("Test case {} failed".format(i))
                        print("error: {}".format(e))
                        print("request:")
                        print(request)
                        print("response:")
                        print(response)
                    else:
                        print(".", end='')
                else:
                    print("\n")
                    print_line_notify("Complete all {} test cases, failed {}".format(i, failed))
                    break

        return i, failed
