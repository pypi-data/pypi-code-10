import logging
import logging.config
from flask import Flask
from flask.ext.uwsgi_websocket import GeventWebSocket
from .config import load_config, load_absinthe_config
from .commands import CommandServer

config = load_config()

logging.config.dictConfig(config['logger'])

logger = logging.getLogger(__name__)

absinthe_config = load_absinthe_config()

app = Flask(__name__)
websocket = GeventWebSocket(app)

commands = CommandServer(absinthe_config)

@websocket.route('/')
def index(ws):
    while True:
        message = ws.receive()
        response = commands.process(message)
        logger.debug("Response: %s" % response)
        if response is not None:
            ws.send(str(response))
