import time

import requests

from predata.config.exceptions import PredataPythonClientExeception
from predata.config.logger import logger




class PredataGenericClient():

    def __init__(self, session, hostname, api_base, max_retries):
        self.session = session
        self.HOSTNAME = hostname
        self.API_BASE = api_base
        self.MAX_RETRIES = max_retries

    def make_request(self, endpoint, process_rpc=False):
        """
        Make and paginate through results if necessary.
        """
        total_response = []
        current_endpoint = self.HOSTNAME + self.API_BASE + endpoint
        MAX_RETRIES = self.MAX_RETRIES
        retries = 0

        while current_endpoint and retries < MAX_RETRIES:
            logger.info("Making request to %s", current_endpoint)

            try:
                resp = self.session.get(current_endpoint)
            except requests.exceptions.ConnectionError:
                logger.debug("Request to %s failed on ConnectionError")
                retries += 1
                continue

            if resp.status_code == 404:
                logger.debug("Request to %s failed on HTTP 404 response code")
                retries += MAX_RETRIES
                break
            elif resp.status_code != 200:
                logger.debug("Request to %s failed on HTTP non-200 response code")
                retries += 1
                continue

            retries = 0

            response_content = resp.json()

            # if it is an RPC call and progress
            if ("results" in response_content and "progress" in response_content) and process_rpc:
                logger.debug("Processing RPC to %s", current_endpoint)
                time.sleep(1.0)
                continue

            if "results" in response_content and response_content["results"] != "processing":
                total_response += response_content["results"]
                if "next" in response_content:
                    current_endpoint = response_content["next"]
                else:
                    current_endpoint = None
            else:
                total_response = response_content
                current_endpoint = None

        if retries >= MAX_RETRIES:
            raise PredataPythonClientExeception("Exceeded maximum number of retries to the server.")

        return total_response
