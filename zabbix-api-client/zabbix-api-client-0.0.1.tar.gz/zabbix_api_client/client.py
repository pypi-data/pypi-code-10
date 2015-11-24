import requests
import json
import logging
import jsonschema
import dateutil.parser


class Borg(object):
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Client(Borg):
    """Zabbix API"""

    def __init__(self, **kwargs):
        """ Client instance Constructor

        :param host: zabbix host name
        :param user: access user
        :param password: access user's password
        :param log_level: log level
        """
        Borg.__init__(self)
        if not hasattr(self, 'logger') or not self.logger:
            self.logger = logging.getLogger(__name__)
            if 'log_level' not in kwargs:
                log_level = 'WARNING'
            else:
                log_level = kwargs['log_level'].upper()
            loglevel_obj = getattr(logging, log_level)
            self.logger.setLevel(loglevel_obj)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            self.logger.addHandler(ch)
        if not hasattr(self, 'logger') or not self.logger:
            self.logger = logging.getLogger(__name__)
        self.logger.info('Start initializing')
        if not hasattr(self, 'host') or not self.host:
            self.host = kwargs['host'] + '/zabbix/api_jsonrpc.php'
        self.request_id = 1
        if not hasattr(self, 'auth') or not self.auth:
            self.auth = self.request('user.login', {
                'user': kwargs['user'],
                'password': kwargs['password']
            })

    def request(self, method, params):
        self.request_id += 1
        headers = {"Content-Type": "application/json-rpc"}
        data = json.dumps({
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'auth': (self.auth if hasattr(self, 'auth') else None),
            'id': self.request_id
        })
        self.logger.info('URL:%s\tMETHOD:%s\tPARAM:%s',
                         self.host, method, str(params))
        r = requests.post(self.host, data=data, headers=headers)
        if 'error' in r.json():
            error = r.json()['error']
            self.logger.error('MESSAGE:%s', error)
            raise Exception(error)
        self.logger.info('STATUS_CODE:%s', r.status_code)
        return r.json()['result']

    def validate(self, params, schema):
        jsonschema.validate(params, schema)

    def unixtime(self, datetime):
        return int(dateutil.parser.parse(datetime).timestamp())
