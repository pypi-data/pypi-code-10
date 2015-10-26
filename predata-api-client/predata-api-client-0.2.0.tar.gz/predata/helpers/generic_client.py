import requests
from predata.config.exceptions import PredataPythonClientExeception

class PredataGenericClient():

    def __init__(self, session, hostname, api_base, max_retries):
        self.session = session
        self.HOSTNAME = hostname
        self.API_BASE = api_base
        self.MAX_RETRIES = max_retries

    def make_request(self, endpoint):
        """
        Make and paginate through results if necessary.
        """
        total_response = []
        current_endpoint = self.HOSTNAME + self.API_BASE + endpoint
        MAX_RETRIES = self.MAX_RETRIES
        retries = 0

        while current_endpoint and retries < MAX_RETRIES:

            try:
                resp = self.session.get(current_endpoint)
            except requests.exceptions.ConnectionError:
                retries += 1
                continue

            if resp.status_code == 404:
                retries += MAX_RETRIES
                break
            elif resp.status_code != 200:
                retries += 1
                continue

            retries = 0

            response_content = resp.json()
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
