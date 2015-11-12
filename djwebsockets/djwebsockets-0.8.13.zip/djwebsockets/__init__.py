from django.conf import global_settings
from . import default_settings

global_settings.WEBSOCKET_BASE_URI = default_settings.WEBSOCKET_BASE_URI
global_settings.WEBSOCKET_HOST = default_settings.WEBSOCKET_HOST
global_settings.WEBSOCKET_PORT = default_settings.WEBSOCKET_PORT