import http.client
from expressly.errors import InvalidApiKeyError, InvalidHTMLError
from expressly.api_responses import *


class Api:
    def __init__(self, api_key, url, secure=True):
        self.api_key = api_key
        self.http_client = http.client.HTTPSConnection(url, 443, timeout=10) \
            if secure else http.client.HTTPConnection(url, 80, timeout=10)

        if self.api_key is None:
            raise InvalidApiKeyError

    def ping(self):
        return self.execute('GET', '/api/admin/ping', response_cls=PingResponse)

    def register(self, hostname):
        return self.execute('POST', '/api/v2/plugin/merchant', {
            'apiKey': self.api_key,
            'apiBaseUrl': hostname
        })

    def get_migration_popup(self, campaign_customer_uuid):
        return self.execute('GET', '/api/v2/migration/%s' % campaign_customer_uuid, authorized=True)

    def get_migration_customer(self, campaign_customer_uuid):
        return self.execute('GET', '/api/v2/migration/%s/user' % campaign_customer_uuid,
                            response_cls=MigrationCustomerResponse)

    def send_migration_status(self, campaign_customer_uuid, exists=False):
        body = {'status': 'migrated'}
        if exists:
            body = {'status': 'existing_customer'}

        return self.execute('POST', '/api/v2/migration/%s/success' % campaign_customer_uuid, body, False,
                            response_cls=MigrationStatusResponse)

    def get_banner(self, campaign_uuid, email):
        return self.execute('GET', '/api/v2/banner/%s?email=%s' % (campaign_uuid, email), response_cls=BannerResponse)

    def execute(self, method, route, body=None, authorized=False, response_cls=None):
        conn = self.http_client

        headers = {
            'Connection': 'close',
            'Content-Type': 'application/json'
        }
        if authorized is True:
            headers['Authorization'] = 'Basic %s' % self.api_key

        conn.request(method, route, json.dumps(body), headers)

        response = conn.getresponse()
        data = response.read().decode('utf-8')
        response.close()

        return ApiResponse(response.status, data, response_cls)
