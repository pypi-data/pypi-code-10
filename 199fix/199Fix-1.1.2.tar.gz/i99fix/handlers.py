import logging
import traceback
try:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import Request, urlopen, HTTPError
import json
from i99fix import __version__


_DEFAULT_API_URL = 'https://199fix.com/api/logger/'
_DEFAULT_ENV_VARIABLES = ['DJANGO_SETTINGS_MODULE', ]
_DEFAULT_META_VARIABLES = ['HTTP_USER_AGENT', 'REMOTE_ADDR',
                           'SERVER_NAME', 'SERVER_SOFTWARE', ]


class I99FixHandler(logging.Handler):
    '''
    Error logger for 199fix.com
    '''

    def __init__(self, api_key, env_name, api_url=_DEFAULT_API_URL,
                 timeout=30, env_variables=_DEFAULT_ENV_VARIABLES,
                 meta_variables=_DEFAULT_META_VARIABLES):
        logging.Handler.__init__(self)
        self.api_key = api_key
        self.api_url = api_url
        self.env_name = env_name
        self.env_variables = env_variables
        self.meta_variables = meta_variables
        self.timeout = timeout

    def emit(self, record):
        try:
            message = self.generate_json(record)
            self._sendMessage(message)
        except Exception:
            return None

    def generate_json(self, record):
        '''
        generate json
        from data
        '''
        exn = None
        trace = None
        data = {}
        if record.exc_info:
            _, exn, trace = record.exc_info

        message = record.getMessage()
        if exn:
            message = "{0}: {1}".format(message, str(exn))

        if hasattr(record, 'request'):
            request = record.request
            cgi_data = []
            for key, value in request.META.items():
                if key in self.meta_variables:
                    '''more data'''
                    cgi_data.append({key: value})
        data['cgi_data'] = cgi_data
        data['exception'] = exn.__class__.__name__ if exn else ''
        data['message'] = message
        data['level'] = record.levelname

        trace_data = []
        try:
            if trace is None:
                trace_data = {'file': record.pathname,
                              'number': str(record.lineno),
                              'method': record.funcName
                              }
            else:
                for pathname, lineno, funcName, text in traceback.extract_tb(trace):
                    trace_data = {'file': pathname,
                                  'number': str(lineno),
                                  'method': '%s: %s' % (funcName, text)
                                  }
        except Exception:
            pass

        try:
            '''
            request url
            '''
            data['url'] = request.build_absolute_uri()
        except Exception:
            pass

        data['backtrace'] = trace_data
        return data

    def _sendHttpRequest(self, message={}):
        '''
        send json request to url
        '''
        try:
            '''initial values'''
            message['__version__'] = __version__
            message['api-key'] = self.api_key
            message['environment-name'] = self.env_name
            req = Request(self.api_url)
            req.add_header('Content-Type', 'application/json')
            response = urlopen(req, json.dumps(message), timeout=self.timeout)
            status = response.getcode()
        except HTTPError as e:
            status = e.code
        return status

    def _sendMessage(self, message):
        '''
        send message
        '''
        status = self._sendHttpRequest(message)
        if status == 200:
            return

        if status == 403:
            exceptionMessage = "Invalid API credentials"
        elif status == 422:
            exceptionMessage = "Invalid Json sent: {0}".format(message)
        elif status == 500:
            exceptionMessage = "Destination server is unavailable. " \
                               "Please check the remote server status."
        elif status == 503:
            exceptionMessage = "Service unavailable. You may be over your " \
                               "quota."
        elif status == 303:
            exceptionMessage = "Invalid Url for this application"
        else:
            exceptionMessage = "Unexpected status code {0}".format(str(status))
        raise Exception('[199fix] %s' % exceptionMessage)
