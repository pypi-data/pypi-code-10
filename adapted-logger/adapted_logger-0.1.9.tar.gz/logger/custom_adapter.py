#__author__ = 'ismailkaboubi'


import logging
from logging.config import dictConfig
import yaml


class CustomAdapter(logging.LoggerAdapter):
    """
    This  adapter expects the passed in dict-like object to have a
    'ip' key, whose value in brackets is prepended to the log message.
    """
    def process(self, msg, kwargs):
        return '%s    %s' % (self.extra['ip'], msg), kwargs



### Exemple of usage #######################################################################
ip = "10.0.0.129"

logging_config = yaml.load(open('config/config.yml', 'r'))
dictConfig(logging_config)

logger_dashboard = logging.getLogger("retail_crm_server.dashboard_api")
logger_dashboard = CustomAdapter(logger_dashboard, {'ip': ip})

logger_core_api = logging.getLogger("retail_crm_server.core_api")
logger_core_api = CustomAdapter(logger_core_api, {'ip': ip})

for i in range(10):
    logger_core_api.info('This is a info Message', extra={'ip': "127.0.0.1"})
    logger_core_api.debug('This is a debug Message')
    logger_core_api.warning('This is a warning Message')
    logger_core_api.critical('This is a critical Message')
    logger_core_api.error('This is a error Message')
    logger_core_api.info('----------------------------------------------------------', extra={'ip': "127.0.0.1"})

    logger_dashboard.info('This is a info Message', extra={'ip': "127.0.0.1"})
    logger_dashboard.debug('This is a debug Message')
    logger_dashboard.warning('This is a warning Message')
    logger_dashboard.critical('This is a critical Message')
    logger_dashboard.error('This is a error Message')
    logger_dashboard.info('----------------------------------------------------------', extra={'ip': "127.0.0.1"})
############################################################################################