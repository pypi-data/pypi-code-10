"""
Add logging config in your config.py

    LOGGING_CONFIG = {
        "version": 1,
        "handlers": {
            "rollbar": {
                "class": "application.extras.rollbar_logger.RollbarHandler",
                "access_token": "",
                "level": "WARN"
            }
        },
        'loggers': {
            '': {
                'handlers': ['rollbar'],
                'level': 'WARN',
            },
        }
    }

"""
import os
from webportfolio import WebPortfolio, get_env
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception, request
import logging
import logging.handlers

_env = get_env().lower()

class RollbarHandler(logging.Handler):
    def __init__(self, access_token,  *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)

        rollbar.init(

            # access token for the demo app: https://rollbar.com/demo
            access_token,

            # environment name
            _env,

            # server root directory, makes tracebacks prettier
            root=os.path.dirname(os.path.realpath(__file__)),

            # flask already sets up logging
            allow_logging_basic_config=False)

    def emit(self, record):
        if record.exc_info:
            rollbar.report_exc_info(record.exc_info)
        else:
            request = None

            rollbar.report_message(record.msg, record.levelname, request=request)

def rollbar_init_app(app):
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

WebPortfolio.bind(rollbar_init_app)


