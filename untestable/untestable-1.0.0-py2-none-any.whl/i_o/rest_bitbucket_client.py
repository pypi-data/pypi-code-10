import json
import pkgutil

import requests
from requests.auth import HTTPBasicAuth

from untestable.i_o.bitbucket_client import BitbucketClient
from untestable.i_o.bitbucket_client import BitbucketResponse


class RestBitBucketClient(BitbucketClient):
    """
    A BitBucketClient that uses the requests API to serve needed requests.
    """

    def __init__(self):
        # Load the config from the json file using pkgutil
        # One would likely check the validity of the config here as well.
        self.config = json.loads(pkgutil.get_data('untestable.i_o',
                                                  'rest_bitbucket_client_config.json'))

    def get_user(self, creds):
        resp = requests.get(self.config["user"],
                            auth=HTTPBasicAuth(creds.username, creds.password))
        return self.build_bb_response(resp)

    def get_user_repositories(self, creds):
        resp = requests.get(self.config["repositories"],
                            auth=HTTPBasicAuth(creds.username, creds.password))
        return self.build_bb_response(resp)

    @staticmethod
    def build_bb_response(resp):
        """
        Translates a response requests.Response object to a
        untestable.i_o.rest_bitbucket_client.BitbucketResponse.  This appropriately accounts for the
        variation of the format of the response body as the HTTP status code varies

        :param resp: a requests.Response object resulting from a call to a Bitbucket REST API
        :return: an equivalent untestable.i_o.rest_bitbucket_client.BitbucketResponse
        """
        if resp.status_code == 200:
            return BitbucketResponse(status_code=resp.status_code,
                                     reason=resp.reason,
                                     body=resp.json())
        else:
            return BitbucketResponse(status_code=resp.status_code,
                                     reason=resp.reason,
                                     body=resp.text)
