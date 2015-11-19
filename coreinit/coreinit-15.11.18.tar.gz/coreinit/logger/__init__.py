from coreinit import settings
import importlib

logger_class = importlib.import_module(settings.DEFAULT_LOGGER)

global Logger
Logger = logger_class.Logger()