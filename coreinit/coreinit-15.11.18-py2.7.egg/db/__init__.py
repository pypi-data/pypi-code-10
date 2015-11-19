from coreinit import settings
import importlib

cache_class = importlib.import_module(settings.DEFAULT_DB)

global Cache
Cache = cache_class.Cache()
Cache.configure()